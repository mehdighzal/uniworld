from rest_framework import serializers
from .models import Subscription, Payment, EmailLog


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model"""
    
    is_active = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Subscription
        fields = (
            'id', 'user', 'plan_type', 'status', 'amount', 'currency',
            'start_date', 'end_date', 'is_active', 'days_remaining',
            'stripe_subscription_id', 'stripe_customer_id',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    
    is_successful = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    
    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'subscription', 'amount', 'currency', 'payment_method',
            'status', 'stripe_payment_intent_id', 'stripe_charge_id',
            'payment_date', 'description', 'failure_reason',
            'is_successful', 'is_pending', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class EmailLogSerializer(serializers.ModelSerializer):
    """Serializer for EmailLog model"""
    
    coordinator_name = serializers.CharField(source='coordinator.name', read_only=True)
    coordinator_email = serializers.CharField(source='coordinator.public_email', read_only=True)
    university_name = serializers.CharField(source='coordinator.university.name', read_only=True)
    program_name = serializers.CharField(source='coordinator.program.name', read_only=True)
    
    class Meta:
        model = EmailLog
        fields = (
            'id', 'user', 'coordinator', 'coordinator_name', 'coordinator_email',
            'university_name', 'program_name', 'subject', 'body', 'email_provider',
            'status', 'sent_at', 'error_message', 'message_id', 'created_at'
        )
        read_only_fields = ('id', 'user', 'created_at')


class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer for creating a new subscription"""
    
    plan_type = serializers.ChoiceField(choices=Subscription.PLAN_CHOICES)
    payment_method_id = serializers.CharField(max_length=200)
    
    def validate_plan_type(self, value):
        # Define pricing based on plan type
        pricing = {
            'monthly': 9.99,
            'yearly': 99.99
        }
        self.context['amount'] = pricing.get(value)
        if not self.context['amount']:
            raise serializers.ValidationError("Invalid plan type")
        return value


class SendEmailSerializer(serializers.Serializer):
    """Serializer for sending emails to coordinators"""
    
    coordinator_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=50
    )
    subject = serializers.CharField(max_length=500)
    body = serializers.CharField()
    email_provider = serializers.ChoiceField(choices=EmailLog.EMAIL_PROVIDER_CHOICES)
    
    def validate_coordinator_ids(self, value):
        from universities.models import Coordinator
        coordinators = Coordinator.objects.filter(id__in=value, is_active=True)
        if len(coordinators) != len(value):
            raise serializers.ValidationError("Some coordinators are invalid or inactive")
        return value


class StripeWebhookSerializer(serializers.Serializer):
    """Serializer for Stripe webhook events"""
    
    id = serializers.CharField()
    object = serializers.CharField()
    type = serializers.CharField()
    data = serializers.JSONField()
