"""
URL configuration for uniworld_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from . import views
from .stripe_views import (
    create_payment_session, 
    stripe_webhook, 
    subscription_success, 
    subscription_cancel,
    get_user_subscription
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page (frontend)
    path('', views.home_view, name='home'),
    
    # Serve JavaScript file
    path('app.js', views.app_js_view, name='app-js'),
    
    # API welcome page
    path('api-welcome/', views.welcome_view, name='api-welcome'),
    
    # Simple authentication endpoints
    path('api/auth/register/', views.register_view, name='register'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/change-password/', views.change_password_view, name='change-password'),
    
    # API Endpoints for Frontend
    path('api/universities/', views.universities_api_view, name='universities-api'),
    path('api/programs/', views.programs_api_view, name='programs-api'),
    path('api/coordinators/', views.coordinators_api_view, name='coordinators-api'),
    path('api/countries/', views.countries_api_view, name='countries-api'),
    path('api/fields-of-study/', views.fields_of_study_api_view, name='fields-of-study-api'),
    path('api/search/', views.search_api_view, name='search-api'),
    path('api/send-email/', views.send_email_api_view, name='send-email-api'),
    path('api/send-bulk-email/', views.send_bulk_email_api_view, name='send-bulk-email-api'),
    
    # Stripe Payment Endpoints
    path('api/create-payment-session/', create_payment_session, name='create-payment-session'),
    path('api/stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('api/user-subscription/<int:user_id>/', get_user_subscription, name='user-subscription'),
    path('subscription/success/', subscription_success, name='subscription-success'),
    path('subscription/cancel/', subscription_cancel, name='subscription-cancel'),
    
    # API Documentation (temporarily disabled)
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints (temporarily disabled)
    # path('api/auth/', include('accounts.urls')),
    # path('api/', include('universities.urls')),
    # path('api/payments/', include('payments.urls')),
]
