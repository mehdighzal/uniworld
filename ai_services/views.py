"""
AI-powered email suggestion API endpoints for UniWorld platform
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
import openai

from ai_services.email_suggestions import (
    get_email_suggestions, 
    get_multiple_subject_options,
    EmailSuggestionService
)
from universities.models import Program, Coordinator

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def generate_email_suggestions(request):
    """
    Generate AI-powered email subject and content suggestions
    
    Expected payload:
    {
        "program_id": int,
        "coordinator_id": int,
        "email_type": "inquiry|admission|scholarship",
        "student_profile": {
            "background": "Computer Science",
            "interests": "AI and Machine Learning",
            "experience": "2 years software development"
        },
        "custom_requirements": ["specific question 1", "specific question 2"]
    }
    """
    try:
        data = json.loads(request.body)
        program_id = data.get('program_id')
        coordinator_id = data.get('coordinator_id')
        email_type = data.get('email_type', 'inquiry')
        student_profile = data.get('student_profile', {})
        custom_requirements = data.get('custom_requirements', [])
        
        if not program_id or not coordinator_id:
            return JsonResponse({
                'error': 'program_id and coordinator_id are required'
            }, status=400)
        
        # Get program and coordinator data
        try:
            program = Program.objects.get(id=program_id)
            coordinator = Coordinator.objects.get(id=coordinator_id, is_active=True)
        except (Program.DoesNotExist, Coordinator.DoesNotExist):
            return JsonResponse({
                'error': 'Program or coordinator not found'
            }, status=404)
        
        # Generate AI suggestions
        suggestions = get_email_suggestions(
            program_name=program.name,
            university_name=program.university.name,
            coordinator_name=coordinator.name,
            coordinator_role=coordinator.role,
            email_type=email_type,
            student_profile=student_profile
        )
        
        # Add custom requirements to content if provided
        if custom_requirements:
            service = EmailSuggestionService()
            enhanced_content = service.generate_email_content(
                program_name=program.name,
                university_name=program.university.name,
                coordinator_name=coordinator.name,
                coordinator_role=coordinator.role,
                email_type=email_type,
                student_profile=student_profile,
                custom_requirements=custom_requirements
            )
            suggestions['content'] = enhanced_content
        
        return JsonResponse({
            'success': True,
            'suggestions': suggestions,
            'program_info': {
                'name': program.name,
                'university': program.university.name,
                'field_of_study': program.field_of_study
            },
            'coordinator_info': {
                'name': coordinator.name,
                'role': coordinator.role,
                'email': coordinator.public_email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error generating email suggestions: {str(e)}")
        return JsonResponse({
            'error': 'Failed to generate email suggestions',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_subject_options(request):
    """
    Generate multiple AI-powered email subject line options
    
    Expected payload:
    {
        "program_id": int,
        "coordinator_id": int,
        "email_type": "inquiry|admission|scholarship",
        "count": 3
    }
    """
    try:
        data = json.loads(request.body)
        program_id = data.get('program_id')
        coordinator_id = data.get('coordinator_id')
        email_type = data.get('email_type', 'inquiry')
        count = data.get('count', 3)
        
        if not program_id or not coordinator_id:
            return JsonResponse({
                'error': 'program_id and coordinator_id are required'
            }, status=400)
        
        # Get program and coordinator data
        try:
            program = Program.objects.get(id=program_id)
            coordinator = Coordinator.objects.get(id=coordinator_id, is_active=True)
        except (Program.DoesNotExist, Coordinator.DoesNotExist):
            return JsonResponse({
                'error': 'Program or coordinator not found'
            }, status=404)
        
        # Generate multiple subject options
        subject_options = get_multiple_subject_options(
            program_name=program.name,
            university_name=program.university.name,
            coordinator_name=coordinator.name,
            email_type=email_type,
            count=count
        )
        
        return JsonResponse({
            'success': True,
            'subject_options': subject_options,
            'program_info': {
                'name': program.name,
                'university': program.university.name
            },
            'coordinator_info': {
                'name': coordinator.name,
                'role': coordinator.role
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error generating subject options: {str(e)}")
        return JsonResponse({
            'error': 'Failed to generate subject options',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def enhance_email_content(request):
    """
    Enhance existing email content with AI suggestions
    
    Expected payload:
    {
        "program_id": int,
        "coordinator_id": int,
        "current_content": "existing email content",
        "email_type": "inquiry|admission|scholarship",
        "enhancement_type": "improve|personalize|shorten|expand"
    }
    """
    try:
        data = json.loads(request.body)
        program_id = data.get('program_id')
        coordinator_id = data.get('coordinator_id')
        current_content = data.get('current_content', '')
        email_type = data.get('email_type', 'inquiry')
        enhancement_type = data.get('enhancement_type', 'improve')
        
        if not program_id or not coordinator_id or not current_content:
            return JsonResponse({
                'error': 'program_id, coordinator_id, and current_content are required'
            }, status=400)
        
        # Get program and coordinator data
        try:
            program = Program.objects.get(id=program_id)
            coordinator = Coordinator.objects.get(id=coordinator_id, is_active=True)
        except (Program.DoesNotExist, Coordinator.DoesNotExist):
            return JsonResponse({
                'error': 'Program or coordinator not found'
            }, status=404)
        
        # Generate enhanced content
        service = EmailSuggestionService()
        enhanced_content = service.enhance_email_content(
            current_content=current_content,
            program_name=program.name,
            university_name=program.university.name,
            coordinator_name=coordinator.name,
            coordinator_role=coordinator.role,
            enhancement_type=enhancement_type
        )
        
        return JsonResponse({
            'success': True,
            'enhanced_content': enhanced_content,
            'original_content': current_content,
            'enhancement_type': enhancement_type
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error enhancing email content: {str(e)}")
        return JsonResponse({
            'error': 'Failed to enhance email content',
            'details': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_ai_templates(request):
    """
    Get AI-powered email templates for different scenarios
    """
    try:
        from ai_services.templates import get_template_categories
        
        email_type = request.GET.get('type', 'inquiry')
        categories = get_template_categories()
        
        return JsonResponse({
            'success': True,
            'templates': categories.get(email_type, categories['inquiry']),
            'available_types': list(categories.keys()),
            'all_categories': categories
        })
        
    except Exception as e:
        logger.error(f"Error getting AI templates: {str(e)}")
        return JsonResponse({
            'error': 'Failed to get AI templates',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_ai_template(request):
    """
    Generate AI-powered email template for specific scenario
    
    Expected payload:
    {
        "program_id": int,
        "coordinator_id": int,
        "template_type": "inquiry|admission|scholarship|research|career",
        "student_profile": {
            "background": "Computer Science",
            "interests": "AI and Machine Learning",
            "experience": "2 years software development"
        }
    }
    """
    try:
        from ai_services.templates import get_ai_template
        
        data = json.loads(request.body)
        program_id = data.get('program_id')
        coordinator_id = data.get('coordinator_id')
        template_type = data.get('template_type', 'inquiry')
        student_profile = data.get('student_profile', {})
        
        if not program_id or not coordinator_id:
            return JsonResponse({
                'error': 'program_id and coordinator_id are required'
            }, status=400)
        
        # Get program and coordinator data
        try:
            program = Program.objects.get(id=program_id)
            coordinator = Coordinator.objects.get(id=coordinator_id, is_active=True)
        except (Program.DoesNotExist, Coordinator.DoesNotExist):
            return JsonResponse({
                'error': 'Program or coordinator not found'
            }, status=404)
        
        # Generate AI template
        template = get_ai_template(
            template_type=template_type,
            program_name=program.name,
            university_name=program.university.name,
            coordinator_name=coordinator.name,
            coordinator_role=coordinator.role,
            student_profile=student_profile
        )
        
        return JsonResponse({
            'success': True,
            'template': template,
            'program_info': {
                'name': program.name,
                'university': program.university.name,
                'field_of_study': program.field_of_study
            },
            'coordinator_info': {
                'name': coordinator.name,
                'role': coordinator.role,
                'email': coordinator.public_email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error generating AI template: {str(e)}")
        return JsonResponse({
            'error': 'Failed to generate AI template',
            'details': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_multiple_templates(request):
    """
    Generate multiple AI-powered email templates
    
    Expected payload:
    {
        "program_id": int,
        "coordinator_id": int,
        "template_types": ["inquiry", "admission", "scholarship"],
        "student_profile": {
            "background": "Computer Science",
            "interests": "AI and Machine Learning",
            "experience": "2 years software development"
        }
    }
    """
    try:
        from ai_services.templates import get_multiple_ai_templates
        
        data = json.loads(request.body)
        program_id = data.get('program_id')
        coordinator_id = data.get('coordinator_id')
        template_types = data.get('template_types', ['inquiry', 'admission', 'scholarship'])
        student_profile = data.get('student_profile', {})
        
        if not program_id or not coordinator_id:
            return JsonResponse({
                'error': 'program_id and coordinator_id are required'
            }, status=400)
        
        # Get program and coordinator data
        try:
            program = Program.objects.get(id=program_id)
            coordinator = Coordinator.objects.get(id=coordinator_id, is_active=True)
        except (Program.DoesNotExist, Coordinator.DoesNotExist):
            return JsonResponse({
                'error': 'Program or coordinator not found'
            }, status=404)
        
        # Generate multiple AI templates
        templates = get_multiple_ai_templates(
            program_name=program.name,
            university_name=program.university.name,
            coordinator_name=coordinator.name,
            coordinator_role=coordinator.role,
            template_types=template_types,
            student_profile=student_profile
        )
        
        return JsonResponse({
            'success': True,
            'templates': templates,
            'program_info': {
                'name': program.name,
                'university': program.university.name,
                'field_of_study': program.field_of_study
            },
            'coordinator_info': {
                'name': coordinator.name,
                'role': coordinator.role,
                'email': coordinator.public_email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error generating multiple templates: {str(e)}")
        return JsonResponse({
            'error': 'Failed to generate multiple templates',
            'details': str(e)
        }, status=500)