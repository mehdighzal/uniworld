from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import stripe
from django.conf import settings
from .models import Subscription, Payment, EmailLog
from .serializers import (
    SubscriptionSerializer, PaymentSerializer, EmailLogSerializer,
    CreateSubscriptionSerializer, SendEmailSerializer, StripeWebhookSerializer
)


class SubscriptionListView(generics.ListAPIView):
    """View for listing user subscriptions"""
    
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class PaymentListView(generics.ListAPIView):
    """View for listing user payments"""
    
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class EmailLogListView(generics.ListAPIView):
    """View for listing user email logs"""
    
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EmailLog.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_subscription_view(request):
    """View for creating a new subscription"""
    
    serializer = CreateSubscriptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    plan_type = serializer.validated_data['plan_type']
    payment_method_id = serializer.validated_data['payment_method_id']
    amount = serializer.context['amount']
    
    try:
        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Create Stripe customer if not exists
        if not hasattr(user, 'stripe_customer_id') or not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}".strip() or user.username
            )
            user.stripe_customer_id = customer.id
            user.save()
        
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='eur',
            customer=user.stripe_customer_id,
            payment_method=payment_method_id,
            confirm=True,
            return_url=settings.FRONTEND_URL + '/payment/success'
        )
        
        if payment_intent.status == 'succeeded':
            # Calculate end date
            if plan_type == 'monthly':
                end_date = timezone.now() + timedelta(days=30)
            else:  # yearly
                end_date = timezone.now() + timedelta(days=365)
            
            # Create subscription
            subscription = Subscription.objects.create(
                user=user,
                plan_type=plan_type,
                status='active',
                amount=amount,
                currency='EUR',
                end_date=end_date,
                stripe_customer_id=user.stripe_customer_id
            )
            
            # Create payment record
            Payment.objects.create(
                user=user,
                subscription=subscription,
                amount=amount,
                currency='EUR',
                status='success',
                stripe_payment_intent_id=payment_intent.id,
                stripe_charge_id=payment_intent.charges.data[0].id
            )
            
            # Update user premium status
            user.is_premium = True
            user.save()
            
            return Response({
                'subscription': SubscriptionSerializer(subscription).data,
                'message': 'Subscription created successfully'
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'error': 'Payment failed',
                'payment_intent': payment_intent
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except stripe.error.StripeError as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_email_view(request):
    """View for sending emails to coordinators"""
    
    if not request.user.can_send_emails:
        return Response({
            'error': 'Premium subscription required to send emails'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = SendEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    coordinator_ids = serializer.validated_data['coordinator_ids']
    subject = serializer.validated_data['subject']
    body = serializer.validated_data['body']
    email_provider = serializer.validated_data['email_provider']
    
    # Import here to avoid circular imports
    from universities.models import Coordinator
    
    coordinators = Coordinator.objects.filter(id__in=coordinator_ids, is_active=True)
    email_logs = []
    
    for coordinator in coordinators:
        # Create email log
        email_log = EmailLog.objects.create(
            user=request.user,
            coordinator=coordinator,
            subject=subject,
            body=body,
            email_provider=email_provider,
            status='pending'
        )
        email_logs.append(email_log)
        
        # TODO: Implement actual email sending logic based on provider
        # This would integrate with Gmail/Outlook APIs using OAuth2 tokens
        # For now, we'll just mark as sent
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
    
    return Response({
        'message': f'Emails queued for {len(email_logs)} coordinators',
        'email_logs': EmailLogSerializer(email_logs, many=True).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook_view(request):
    """View for handling Stripe webhooks"""
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return Response({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=400)
    
    # Handle different event types
    if event['type'] == 'payment_intent.succeeded':
        # Handle successful payment
        payment_intent = event['data']['object']
        # Update payment status in database
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.status = 'success'
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        # Handle failed payment
        payment_intent = event['data']['object']
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.status = 'failed'
            payment.failure_reason = payment_intent.get('last_payment_error', {}).get('message', '')
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscription_status_view(request):
    """View for checking subscription status"""
    
    user = request.user
    active_subscription = user.subscriptions.filter(
        status='active',
        end_date__gt=timezone.now()
    ).first()
    
    return Response({
        'is_premium': user.is_premium,
        'has_active_subscription': user.has_active_subscription,
        'can_send_emails': user.can_send_emails,
        'active_subscription': SubscriptionSerializer(active_subscription).data if active_subscription else None
    })