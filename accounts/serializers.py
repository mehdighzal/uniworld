from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    has_active_subscription = serializers.ReadOnlyField()
    can_send_emails = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    academic_background = serializers.ReadOnlyField()
    profile_completeness = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'nationality', 'age', 'phone_number',
            'degree', 'major', 'university', 'graduation_year', 'gpa',
            'current_position', 'company', 'work_experience_years',
            'relevant_experience', 'interests', 'languages_spoken',
            'linkedin_profile', 'portfolio_website',
            'preferred_countries', 'budget_range',
            'academic_background', 'profile_completeness',
            'is_premium', 'date_joined', 'has_active_subscription', 
            'can_send_emails'
        )
        read_only_fields = ('id', 'date_joined', 'is_premium', 'full_name', 'academic_background', 'profile_completeness')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'nationality', 'age', 'phone_number',
            'degree', 'major', 'university', 'graduation_year', 'gpa',
            'current_position', 'company', 'work_experience_years',
            'relevant_experience', 'interests', 'languages_spoken',
            'linkedin_profile', 'portfolio_website',
            'preferred_countries', 'budget_range'
        )
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_age(self, value):
        if value and (value < 16 or value > 100):
            raise serializers.ValidationError("Age must be between 16 and 100")
        return value
    
    def validate_gpa(self, value):
        if value and (value < 0 or value > 4.0):
            raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value
    
    def validate_graduation_year(self, value):
        current_year = timezone.now().year
        if value and (value < 1950 or value > current_year + 10):
            raise serializers.ValidationError(f"Graduation year must be between 1950 and {current_year + 10}")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
