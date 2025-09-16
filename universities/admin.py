from django.contrib import admin
from .models import University, Program, Coordinator


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin configuration for University model"""
    
    list_display = ('name', 'country', 'city', 'programs_count', 'coordinators_count', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('name', 'city', 'country')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'country', 'city', 'website', 'description')
        }),
        ('Additional Information', {
            'fields': ('established_year', 'student_count', 'ranking_world', 'ranking_country'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('logo',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'programs_count', 'coordinators_count')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Admin configuration for Program model"""
    
    list_display = ('name', 'university', 'field_of_study', 'degree_level', 'language', 'is_active')
    list_filter = ('degree_level', 'language', 'is_active', 'university__country')
    search_fields = ('name', 'field_of_study', 'university__name')
    ordering = ('university__name', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('university', 'name', 'field_of_study', 'degree_level', 'description')
        }),
        ('Program Details', {
            'fields': ('duration_months', 'language', 'tuition_fee_euro', 'application_deadline', 'start_date')
        }),
        ('Requirements', {
            'fields': ('min_gpa', 'ielts_score', 'toefl_score', 'gre_score'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('program_website', 'brochure_url', 'is_active')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'coordinators_count')


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    """Admin configuration for Coordinator model"""
    
    list_display = ('name', 'university', 'program', 'role', 'public_email', 'is_active')
    list_filter = ('role', 'is_active', 'university__country')
    search_fields = ('name', 'public_email', 'university__name', 'program__name')
    ordering = ('university__name', 'program__name', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('university', 'program', 'name', 'public_email', 'role')
        }),
        ('Contact Information', {
            'fields': ('phone', 'office_location', 'office_hours'),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': ('title', 'department', 'bio'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')