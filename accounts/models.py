from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Extended Profile Information
    nationality = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Academic Information
    degree = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Bachelor's, Master's")
    major = models.CharField(max_length=100, blank=True, null=True, help_text="Field of study")
    university = models.CharField(max_length=200, blank=True, null=True, help_text="University name")
    graduation_year = models.PositiveIntegerField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, help_text="GPA out of 4.0")
    
    # Professional Information
    current_position = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    work_experience_years = models.PositiveIntegerField(blank=True, null=True)
    
    # Additional Information
    relevant_experience = models.TextField(blank=True, null=True, help_text="Internships, projects, skills")
    interests = models.TextField(blank=True, null=True, help_text="Academic and professional interests")
    languages_spoken = models.TextField(blank=True, null=True, help_text="Languages you speak")
    linkedin_profile = models.URLField(blank=True, null=True)
    portfolio_website = models.URLField(blank=True, null=True)
    
    # Preferences
    preferred_countries = models.TextField(blank=True, null=True, help_text="Countries of interest for studies")
    budget_range = models.CharField(max_length=50, blank=True, null=True, help_text="Budget range for studies")
    
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
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def academic_background(self):
        """Get formatted academic background"""
        parts = []
        if self.degree and self.major:
            parts.append(f"{self.degree} in {self.major}")
        if self.university:
            parts.append(f"from {self.university}")
        if self.graduation_year:
            parts.append(f"graduating in {self.graduation_year}")
        return " ".join(parts) if parts else ""
    
    @property
    def profile_completeness(self):
        """Calculate profile completeness percentage"""
        fields = [
            'first_name', 'last_name', 'nationality', 'age', 'phone_number',
            'degree', 'major', 'university', 'graduation_year',
            'relevant_experience', 'interests'
        ]
        completed_fields = sum(1 for field in fields if getattr(self, field, None))
        return int((completed_fields / len(fields)) * 100)