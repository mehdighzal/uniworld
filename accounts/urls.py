from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/stats/', views.profile_stats_view, name='profile-stats'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('subscription-status/', views.user_subscription_status_view, name='subscription-status'),
]
