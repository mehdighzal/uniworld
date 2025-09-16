import stripe
import os
from django.conf import settings

# Stripe configuration
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_your_stripe_secret_key_here')

# Stripe webhook endpoint secret
STRIPE_WEBHOOK_SECRET = getattr(settings, 'STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret_here')

# Subscription plans configuration
SUBSCRIPTION_PLANS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'stripe_price_id': None,
        'emails_limit': 0,
        'features': [
            'Browse universities and programs',
            'Basic search functionality',
            'View program details',
            'Contact information access'
        ]
    },
    'premium': {
        'name': 'Premium',
        'price': 9.99,
        'stripe_price_id': 'price_premium_monthly',  # Replace with actual Stripe price ID
        'emails_limit': 50,
        'features': [
            'Everything in Free',
            'Send 50 emails per month',
            'Priority support',
            'Advanced search filters'
        ]
    },
    'pro': {
        'name': 'Pro',
        'price': 19.99,
        'stripe_price_id': 'price_pro_monthly',  # Replace with actual Stripe price ID
        'emails_limit': 200,
        'features': [
            'Everything in Premium',
            'Send 200 emails per month',
            'Bulk email functionality',
            'Advanced analytics',
            'API access'
        ]
    }
}

def create_stripe_customer(user):
    """Create a Stripe customer for a user"""
    try:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.username,
            metadata={
                'user_id': user.id,
                'username': user.username
            }
        )
        return customer
    except stripe.error.StripeError as e:
        print(f"Error creating Stripe customer: {e}")
        return None

def create_checkout_session(user, plan_type):
    """Create a Stripe checkout session for subscription"""
    try:
        plan = SUBSCRIPTION_PLANS.get(plan_type)
        if not plan or plan_type == 'free':
            return None
            
        customer = create_stripe_customer(user)
        if not customer:
            return None
            
        session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=['card'],
            line_items=[{
                'price': plan['stripe_price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'http://127.0.0.1:8000/subscription/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'http://127.0.0.1:8000/subscription/cancel',
            metadata={
                'user_id': user.id,
                'plan_type': plan_type
            }
        )
        return session
    except stripe.error.StripeError as e:
        print(f"Error creating checkout session: {e}")
        return None

def get_subscription_status(customer_id):
    """Get subscription status from Stripe"""
    try:
        subscriptions = stripe.Subscription.list(customer=customer_id, status='active')
        if subscriptions.data:
            subscription = subscriptions.data[0]
            return {
                'status': subscription.status,
                'current_period_end': subscription.current_period_end,
                'cancel_at_period_end': subscription.cancel_at_period_end
            }
        return None
    except stripe.error.StripeError as e:
        print(f"Error getting subscription status: {e}")
        return None
