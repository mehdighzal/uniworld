from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_premium', 'is_active', 'date_joined')
    list_filter = ('is_premium', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Premium Features', {'fields': ('is_premium',)}),
        ('OAuth2 Tokens', {
            'fields': (
                'google_access_token', 'google_refresh_token', 'google_token_expiry',
                'microsoft_access_token', 'microsoft_refresh_token', 'microsoft_token_expiry'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')