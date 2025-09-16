from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
import json
import stripe
from .stripe_config import (
    create_checkout_session, 
    get_subscription_status, 
    SUBSCRIPTION_PLANS
)
from payments.models import Subscription, Payment, EmailLog
from django.conf import settings

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment_session(request):
    """Create Stripe checkout session for subscription"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        plan_type = data.get('plan_type')
        user_id = data.get('user_id')
        
        if not plan_type or not user_id:
            return JsonResponse({'error': 'Missing plan_type or user_id'}, status=400)
        
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Create checkout session
        session = create_checkout_session(user, plan_type)
        
        if session:
            return JsonResponse({
                'success': True,
                'session_id': session.id,
                'checkout_url': session.url
            })
        else:
            return JsonResponse({'error': 'Failed to create checkout session'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks for subscription events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        handle_subscription_update(subscription)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancellation(subscription)
    
    return HttpResponse(status=200)

def handle_successful_payment(session):
    """Handle successful payment completion"""
    try:
        user_id = session['metadata']['user_id']
        plan_type = session['metadata']['plan_type']
        
        user = User.objects.get(id=user_id)
        
        # Create or update subscription
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            defaults={
                'plan_type': plan_type,
                'status': 'active',
                'stripe_customer_id': session['customer'],
                'stripe_subscription_id': session.get('subscription')
            }
        )
        
        if not created:
            subscription.plan_type = plan_type
            subscription.status = 'active'
            subscription.stripe_customer_id = session['customer']
            subscription.stripe_subscription_id = session.get('subscription')
            subscription.save()
        
        # Create payment record
        Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=SUBSCRIPTION_PLANS[plan_type]['price'],
            currency='EUR',
            payment_status='success',
            stripe_payment_intent_id=session.get('payment_intent')
        )
        
    except Exception as e:
        print(f"Error handling successful payment: {e}")

def handle_subscription_update(subscription):
    """Handle subscription updates"""
    try:
        stripe_subscription_id = subscription['id']
        subscription_obj = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id
        )
        
        subscription_obj.status = subscription['status']
        subscription_obj.save()
        
    except Subscription.DoesNotExist:
        print(f"Subscription not found: {stripe_subscription_id}")
    except Exception as e:
        print(f"Error handling subscription update: {e}")

def handle_subscription_cancellation(subscription):
    """Handle subscription cancellation"""
    try:
        stripe_subscription_id = subscription['id']
        subscription_obj = Subscription.objects.get(
            stripe_subscription_id=stripe_subscription_id
        )
        
        subscription_obj.status = 'cancelled'
        subscription_obj.save()
        
    except Subscription.DoesNotExist:
        print(f"Subscription not found: {stripe_subscription_id}")
    except Exception as e:
        print(f"Error handling subscription cancellation: {e}")

def subscription_success(request):
    """Handle successful subscription payment"""
    session_id = request.GET.get('session_id')
    
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            user_id = session['metadata']['user_id']
            plan_type = session['metadata']['plan_type']
            
            return render(request, 'subscription_success.html', {
                'plan_type': plan_type,
                'user_id': user_id
            })
        except Exception as e:
            print(f"Error retrieving session: {e}")
    
    return render(request, 'subscription_success.html', {
        'plan_type': 'unknown',
        'user_id': None
    })

def subscription_cancel(request):
    """Handle cancelled subscription payment"""
    return render(request, 'subscription_cancel.html')

def get_user_subscription(request, user_id):
    """Get user's current subscription status"""
    try:
        user = User.objects.get(id=user_id)
        subscription = Subscription.objects.filter(user=user, status='active').first()
        
        if subscription:
            return JsonResponse({
                'success': True,
                'subscription': {
                    'plan_type': subscription.plan_type,
                    'status': subscription.status,
                    'start_date': subscription.start_date.isoformat() if subscription.start_date else None,
                    'end_date': subscription.end_date.isoformat() if subscription.end_date else None
                }
            })
        else:
            return JsonResponse({
                'success': True,
                'subscription': {
                    'plan_type': 'free',
                    'status': 'active',
                    'start_date': None,
                    'end_date': None
                }
            })
            
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
