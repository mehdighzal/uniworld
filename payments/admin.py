from django.contrib import admin
from .models import Subscription, Payment, EmailLog


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for Subscription model"""
    
    list_display = ('user', 'plan_type', 'status', 'amount', 'currency', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan_type', 'status', 'currency', 'created_at')
    search_fields = ('user__email', 'user__username', 'stripe_subscription_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('user', 'plan_type', 'status', 'amount', 'currency')
        }),
        ('Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Stripe Information', {
            'fields': ('stripe_subscription_id', 'stripe_customer_id'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'is_active', 'days_remaining')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model"""
    
    list_display = ('user', 'subscription', 'amount', 'currency', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'currency', 'created_at')
    search_fields = ('user__email', 'stripe_payment_intent_id', 'stripe_charge_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('user', 'subscription', 'amount', 'currency', 'payment_method', 'status')
        }),
        ('Stripe Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('description', 'failure_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'is_successful', 'is_pending')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    """Admin configuration for EmailLog model"""
    
    list_display = ('user', 'coordinator', 'subject', 'email_provider', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'email_provider', 'created_at')
    search_fields = ('user__email', 'coordinator__public_email', 'subject', 'message_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Email Details', {
            'fields': ('user', 'coordinator', 'subject', 'body', 'email_provider', 'status')
        }),
        ('Timestamps', {
            'fields': ('sent_at', 'created_at')
        }),
        ('Additional Information', {
            'fields': ('error_message', 'message_id'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)