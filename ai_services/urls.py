from django.urls import path
from . import views

app_name = 'ai_services'

urlpatterns = [
    path('generate-suggestions/', views.generate_email_suggestions, name='generate_suggestions'),
    path('generate-subjects/', views.generate_subject_options, name='generate_subjects'),
    path('enhance-content/', views.enhance_email_content, name='enhance_content'),
    path('templates/', views.get_ai_templates, name='get_templates'),
    path('generate-template/', views.generate_ai_template, name='generate_template'),
    path('generate-multiple-templates/', views.generate_multiple_templates, name='generate_multiple_templates'),
    path('test-gemini/', views.test_gemini_connection, name='test_gemini'),
]