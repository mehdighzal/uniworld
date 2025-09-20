from django.db import models
from django.utils import timezone
from django.conf import settings


class Subscription(models.Model):
    """Model representing a user's subscription"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Subscription period
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    # Pricing
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    
    # Stripe information
    stripe_subscription_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.plan_type} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        return (
            self.status == 'active' and 
            self.end_date > timezone.now()
        )
    
    @property
    def days_remaining(self):
        """Get number of days remaining in subscription"""
        if self.is_active:
            delta = self.end_date - timezone.now()
            return delta.days
        return 0


class Payment(models.Model):
    """Model representing a payment transaction"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe information
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Timestamps
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional information
    description = models.TextField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency} ({self.status})"
    
    @property
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'success'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.status == 'pending'


class EmailLog(models.Model):
    """Model to track emails sent through the platform"""
    
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    EMAIL_PROVIDER_CHOICES = [
        ('gmail', 'Gmail'),
        ('outlook', 'Outlook'),
        ('yahoo', 'Yahoo'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_logs')
    coordinator = models.ForeignKey('universities.Coordinator', on_delete=models.CASCADE, related_name='email_logs')
    
    # Email details
    subject = models.CharField(max_length=500)
    body = models.TextField()
    email_provider = models.CharField(max_length=20, choices=EMAIL_PROVIDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Additional information
    error_message = models.TextField(blank=True, null=True)
    message_id = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        db_table = 'email_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} -> {self.coordinator.public_email} ({self.status})"