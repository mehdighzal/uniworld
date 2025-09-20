from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'nationality', 'degree', 'university', 'profile_completeness_display', 'is_premium', 'is_active', 'date_joined')
    list_filter = ('is_premium', 'is_active', 'is_staff', 'is_superuser', 'nationality', 'degree', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'nationality', 'university', 'major')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'nationality', 'age', 'phone_number')}),
        ('Academic Information', {
            'fields': ('degree', 'major', 'university', 'graduation_year', 'gpa'),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': ('current_position', 'company', 'work_experience_years', 'relevant_experience'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('interests', 'languages_spoken', 'linkedin_profile', 'portfolio_website'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('preferred_countries', 'budget_range'),
            'classes': ('collapse',)
        }),
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
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view"""
        return super().get_queryset(request).select_related()
    
    def profile_completeness_display(self, obj):
        """Display profile completeness percentage"""
        return f"{obj.profile_completeness}%"
    profile_completeness_display.short_description = 'Profile Complete'
    
    def academic_background_display(self, obj):
        """Display academic background"""
        return obj.academic_background or "Not specified"
    academic_background_display.short_description = 'Academic Background'