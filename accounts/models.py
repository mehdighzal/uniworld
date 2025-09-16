from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # OAuth2 tokens for email sending
    google_access_token = models.TextField(blank=True, null=True)
    google_refresh_token = models.TextField(blank=True, null=True)
    google_token_expiry = models.DateTimeField(blank=True, null=True)
    
    microsoft_access_token = models.TextField(blank=True, null=True)
    microsoft_refresh_token = models.TextField(blank=True, null=True)
    microsoft_token_expiry = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.email
    
    @property
    def has_active_subscription(self):
        """Check if user has an active subscription"""
        return self.subscriptions.filter(
            status='active',
            end_date__gt=timezone.now()
        ).exists()
    
    @property
    def can_send_emails(self):
        """Check if user can send emails (premium + active subscription)"""
        return self.is_premium and self.has_active_subscription