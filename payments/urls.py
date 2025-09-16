from django.urls import path
from . import views

urlpatterns = [
    # Subscription endpoints
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/create/', views.create_subscription_view, name='create-subscription'),
    path('subscriptions/status/', views.subscription_status_view, name='subscription-status'),
    
    # Payment endpoints
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    
    # Email endpoints
    path('emails/', views.EmailLogListView.as_view(), name='email-log-list'),
    path('emails/send/', views.send_email_view, name='send-email'),
    
    # Stripe webhook
    path('webhooks/stripe/', views.stripe_webhook_view, name='stripe-webhook'),
]
