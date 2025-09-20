from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, ChangePasswordSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """View for user registration"""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """View for user login"""
    
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    login(request, user)
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserProfileSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile management"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserUpdateSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """View for changing user password"""
    
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_stats_view(request):
    """View for getting user profile statistics"""
    
    user = request.user
    
    stats = {
        'profile_completeness': user.profile_completeness,
        'academic_background': user.academic_background,
        'full_name': user.full_name,
        'has_complete_profile': user.profile_completeness >= 70,
        'missing_fields': []
    }
    
    # Check which important fields are missing
    important_fields = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('nationality', 'Nationality'),
        ('age', 'Age'),
        ('phone_number', 'Phone Number'),
        ('degree', 'Degree'),
        ('major', 'Major'),
        ('university', 'University'),
        ('graduation_year', 'Graduation Year'),
        ('relevant_experience', 'Relevant Experience'),
        ('interests', 'Interests')
    ]
    
    for field_name, field_display in important_fields:
        if not getattr(user, field_name, None):
            stats['missing_fields'].append(field_display)
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_subscription_status_view(request):
    """View for checking user subscription status"""
    
    user = request.user
    return Response({
        'is_premium': user.is_premium,
        'has_active_subscription': user.has_active_subscription,
        'can_send_emails': user.can_send_emails,
        'subscriptions': user.subscriptions.filter(status='active').values(
            'id', 'plan_type', 'amount', 'currency', 'end_date'
        )
    }, status=status.HTTP_200_OK)