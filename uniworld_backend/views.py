from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from universities.models import University, Program, Coordinator
import json
import os
import time


@require_http_methods(["GET"])
def home_view(request):
    """Home page serving the frontend HTML"""
    # Get the path to the frontend.html file
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend.html')
    
    try:
        with open(frontend_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("""
        <html>
            <head><title>UniWorld - Frontend Not Found</title></head>
            <body>
                <h1>Frontend Not Found</h1>
                <p>The frontend.html file could not be found.</p>
                <p>Please ensure the file exists in the project root directory.</p>
                <a href="/api/docs/">View API Documentation</a>
            </body>
        </html>
        """, content_type='text/html')


@require_http_methods(["GET"])
def app_js_view(request):
    """Serve the app.js file"""
    js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.js')
    
    try:
        with open(js_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return HttpResponse(content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("console.error('app.js not found');", content_type='application/javascript')


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """Simple registration endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Simple login endpoint that accepts email or username"""
    try:
        data = json.loads(request.body)
        username_or_email = data.get('username') or data.get('email')
        password = data.get('password')
        
        if not username_or_email or not password:
            return JsonResponse({'error': 'Missing username/email or password'}, status=400)
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try to find user by email and authenticate with username
        if user is None:
            try:
                user_by_email = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def profile_view(request):
    """Simple profile endpoint for authenticated users"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method == 'GET':
        # Return user profile data
        user = request.user
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username
        })
    
    elif request.method == 'PUT':
        # Update user profile
        try:
            data = json.loads(request.body)
            user = request.user
            
            # Update allowed fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                # Check if email is already taken by another user
                if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                    return JsonResponse({'error': 'Email already exists'}, status=400)
                user.email = data['email']
            
            user.save()
            
            return JsonResponse({
                'message': 'Profile updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'full_name': f"{user.first_name} {user.last_name}".strip() or user.username
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            import traceback
            print(f"Profile update error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=500)


@require_http_methods(["GET"])
def welcome_view(request):
    """Welcome page for the UniWorld API"""
    return JsonResponse({
        'message': 'Welcome to UniWorld API!',
        'description': 'Master\'s Program Search Platform for European Universities',
        'version': '1.0.0',
        'endpoints': {
            'api_documentation': '/api/docs/',
            'api_redoc': '/api/redoc/',
            'universities': '/api/universities/',
            'programs': '/api/programs/',
            'search': '/api/search/',
            'authentication': '/api/auth/',
            'admin': '/admin/'
        },
        'features': [
            'Search master\'s programs in Italian universities',
            'Free access to university and program information',
            'Premium email sending to coordinators',
            'Advanced filtering and search capabilities'
        ]
    })


@csrf_exempt
@require_http_methods(["POST"])
def change_password_view(request):
    """API endpoint to change user password"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not username or not current_password or not new_password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Find user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Verify current password
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        
        # Validate new password
        if len(new_password) < 6:
            return JsonResponse({'error': 'New password must be at least 6 characters'}, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return JsonResponse({
            'message': 'Password changed successfully',
            'success': True
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# API Endpoints for Frontend
@require_http_methods(["GET"])
def universities_api_view(request):
    """API endpoint to get all universities"""
    try:
        universities = University.objects.all()
        universities_data = []
        
        for uni in universities:
            universities_data.append({
                'id': uni.id,
                'university_id': uni.university_id,
                'name': uni.name,
                'country': uni.country,
                'city': uni.city,
                'website': uni.website,
                'description': uni.description,
                'established_year': uni.established_year,
                'student_count': uni.student_count,
                'ranking_world': uni.ranking_world,
                'ranking_country': uni.ranking_country,
                'programs_count': uni.programs_count,
                'coordinators_count': uni.coordinators_count
            })
        
        return JsonResponse({
            'count': len(universities_data),
            'results': universities_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def programs_api_view(request):
    """API endpoint to get all programs"""
    try:
        programs = Program.objects.select_related('university').all()
        programs_data = []
        
        for prog in programs:
            programs_data.append({
                'id': prog.id,
                'program_id': prog.program_id,
                'university': {
                    'id': prog.university.id,
                    'university_id': prog.university.university_id,
                    'name': prog.university.name,
                    'country': prog.university.country,
                    'city': prog.university.city
                },
                'name': prog.name,
                'field_of_study': prog.field_of_study,
                'degree_level': prog.degree_level,
                'description': prog.description,
                'duration_months': prog.duration_months,
                'language': prog.language,
                'tuition_fee_euro': float(prog.tuition_fee_euro) if prog.tuition_fee_euro else None,
                'application_deadline': prog.application_deadline.isoformat() if prog.application_deadline else None,
                'start_date': prog.start_date.isoformat() if prog.start_date else None,
                'min_gpa': float(prog.min_gpa) if prog.min_gpa else None,
                'ielts_score': float(prog.ielts_score) if prog.ielts_score else None,
                'toefl_score': prog.toefl_score,
                'gre_score': prog.gre_score,
                'program_website': prog.program_website,
                'brochure_url': prog.brochure_url,
                'is_active': prog.is_active,
                'coordinators_count': prog.coordinators_count
            })
        
        return JsonResponse({
            'count': len(programs_data),
            'results': programs_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def coordinators_api_view(request):
    """API endpoint to get coordinators with optional filtering"""
    try:
        # Get filter parameters
        program_id = request.GET.get('program_id')
        
        print(f"Coordinators API called with program_id: {program_id}")
        
        # Start with all coordinators
        coordinators = Coordinator.objects.select_related('university', 'program').all()
        
        # Apply filtering if program_id is provided
        if program_id:
            coordinators = coordinators.filter(program__program_id=program_id)
            print(f"Filtered coordinators for program_id {program_id}: {coordinators.count()}")
        
        coordinators_data = []
        
        for coord in coordinators:
            coordinators_data.append({
                'id': coord.id,
                'university': {
                    'id': coord.university.id,
                    'university_id': coord.university.university_id,
                    'name': coord.university.name,
                    'country': coord.university.country,
                    'city': coord.university.city
                },
                'program': {
                    'id': coord.program.id,
                    'program_id': coord.program.program_id,
                    'name': coord.program.name,
                    'field_of_study': coord.program.field_of_study
                },
                'name': coord.name,
                'email': coord.public_email,  # Changed from public_email to email
                'role': coord.role,
                'phone': coord.phone,
                'office_location': coord.office_location,
                'office_hours': coord.office_hours,
                'title': coord.title,
                'department': coord.department,
                'bio': coord.bio,
                'is_active': coord.is_active
            })
        
        print(f"Returning {len(coordinators_data)} coordinators")
        
        return JsonResponse({
            'count': len(coordinators_data),
            'results': coordinators_data
        })
    except Exception as e:
        print(f"Error in coordinators API: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def countries_api_view(request):
    """API endpoint to get all unique countries"""
    try:
        countries = University.objects.values_list('country', flat=True).distinct().order_by('country')
        return JsonResponse({
            'count': len(countries),
            'results': list(countries)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def fields_of_study_api_view(request):
    """API endpoint to get all unique fields of study"""
    try:
        fields = Program.objects.values_list('field_of_study', flat=True).distinct().order_by('field_of_study')
        return JsonResponse({
            'count': len(fields),
            'results': list(fields)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def search_api_view(request):
    """API endpoint to search programs with filters"""
    try:
        print("=== SEARCH API CALLED ===")
        
        # Get filter parameters
        university = request.GET.get('university')
        country = request.GET.get('country')
        field_of_study = request.GET.get('field_of_study')
        degree_level = request.GET.get('degree_level')
        language = request.GET.get('language')
        
        print(f"Search API called with filters: university={university}, country={country}, field_of_study={field_of_study}")
        
        # Start with all programs
        programs = Program.objects.select_related('university').all()
        print(f"Total programs before filtering: {programs.count()}")
        
        # Apply filters
        if university:
            programs = programs.filter(university__name=university)
            print(f"After university filter: {programs.count()}")
        if country:
            programs = programs.filter(university__country=country)
            print(f"After country filter: {programs.count()}")
        if field_of_study:
            programs = programs.filter(field_of_study=field_of_study)
            print(f"After field_of_study filter: {programs.count()}")
        if degree_level:
            programs = programs.filter(degree_level=degree_level)
            print(f"After degree_level filter: {programs.count()}")
        if language:
            programs = programs.filter(language=language)
            print(f"After language filter: {programs.count()}")
        
        # Order by country first, then by university name, then by program name
        programs = programs.order_by('university__country', 'university__name', 'name')
        print(f"Final programs count: {programs.count()}")
        
        # Convert to JSON format
        programs_data = []
        for prog in programs:
            programs_data.append({
                'id': prog.id,
                'program_id': prog.program_id,
                'university': {
                    'id': prog.university.id,
                    'university_id': prog.university.university_id,
                    'name': prog.university.name,
                    'country': prog.university.country,
                    'city': prog.university.city
                },
                'name': prog.name,
                'field_of_study': prog.field_of_study,
                'degree_level': prog.degree_level,
                'description': prog.description,
                'duration_months': prog.duration_months,
                'language': prog.language,
                'tuition_fee_euro': float(prog.tuition_fee_euro) if prog.tuition_fee_euro else None,
                'application_deadline': prog.application_deadline.isoformat() if prog.application_deadline else None,
                'start_date': prog.start_date.isoformat() if prog.start_date else None,
                'min_gpa': float(prog.min_gpa) if prog.min_gpa else None,
                'ielts_score': float(prog.ielts_score) if prog.ielts_score else None,
                'toefl_score': prog.toefl_score,
                'gre_score': prog.gre_score,
                'program_website': prog.program_website,
                'brochure_url': prog.brochure_url,
                'is_active': prog.is_active,
                'coordinators_count': prog.coordinators_count
            })
        
        print(f"Returning {len(programs_data)} programs")
        print(f"First program: {programs_data[0] if programs_data else 'None'}")
        
        response_data = {
            'count': len(programs_data),
            'programs': programs_data
        }
        
        print(f"Response data: {response_data}")
        return JsonResponse(response_data)
    except Exception as e:
        print(f"Search API error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def send_email_api_view(request):
    """API endpoint to send emails to coordinators"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        # Get user from token (simplified for now)
        username = data.get('username')
        if not username:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Get email data
        coordinator_email = data.get('coordinator_id')
        program_id = data.get('program_id')
        subject = data.get('subject')
        body = data.get('body')
        email_provider = data.get('email_provider', 'gmail')
        
        if not all([coordinator_email, subject, body]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # For now, simulate email sending
        # In a real implementation, you would:
        # 1. Verify user subscription
        # 2. Check email limits
        # 3. Send email via Gmail/Outlook API
        # 4. Log the email in database
        
        # Simulate successful email sending
        email_log = {
            'id': f'email_{int(time.time())}',
            'coordinator_email': coordinator_email,
            'program_id': program_id,
            'subject': subject,
            'body': body,
            'email_provider': email_provider,
            'status': 'sent',
            'sent_at': timezone.now().isoformat(),
            'message_id': f'msg_{int(time.time())}'
        }
        
        return JsonResponse({
            'success': True,
            'message': 'Email sent successfully',
            'email_log': email_log
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def send_bulk_email_api_view(request):
    """API endpoint to send bulk emails to multiple coordinators"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        # Get user from token (simplified for now)
        username = data.get('username')
        if not username:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Get bulk email data
        programs = data.get('programs', [])
        subject = data.get('subject')
        body = data.get('body')
        email_provider = data.get('email_provider', 'gmail')
        
        if not all([programs, subject, body]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # For now, simulate bulk email sending
        # In a real implementation, you would:
        # 1. Verify user subscription (Pro only)
        # 2. Check email limits
        # 3. Send emails via Gmail/Outlook API to all coordinators
        # 4. Log all emails in database
        
        total_coordinators = sum(program.get('coordinators_count', 0) for program in programs)
        
        # Simulate successful bulk email sending
        bulk_email_log = {
            'id': f'bulk_email_{int(time.time())}',
            'programs': programs,
            'subject': subject,
            'body': body,
            'email_provider': email_provider,
            'total_coordinators': total_coordinators,
            'status': 'sent',
            'sent_at': timezone.now().isoformat(),
            'message_ids': [f'msg_{int(time.time())}_{i}' for i in range(total_coordinators)]
        }
        
        return JsonResponse({
            'success': True,
            'message': f'Bulk email sent successfully to {total_coordinators} coordinators',
            'bulk_email_log': bulk_email_log
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def test_user_profile_view(request):
    """Test endpoint for user profile functionality"""
    try:
        # Get the custom User model
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Try to get the first user or create a test user
        try:
            user = User.objects.first()
            if not user:
                # Create a test user
                user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='testpass123',
                    first_name='John',
                    last_name='Doe',
                    nationality='American',
                    age=25,
                    phone_number='+1234567890',
                    degree="Bachelor's",
                    major='Computer Science',
                    university='Test University',
                    graduation_year=2020,
                    gpa=3.8,
                    current_position='Software Developer',
                    company='Tech Corp',
                    work_experience_years=3,
                    relevant_experience='Python, Django, React development',
                    interests='Machine Learning, Web Development',
                    languages_spoken='English, Spanish',
                    linkedin_profile='https://linkedin.com/in/johndoe',
                    portfolio_website='https://johndoe.dev',
                    preferred_countries='USA, Canada, UK',
                    budget_range='$25,000 - $50,000'
                )
            
            # Test profile properties
            profile_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'nationality': user.nationality,
                'age': user.age,
                'phone_number': user.phone_number,
                'degree': user.degree,
                'major': user.major,
                'university': user.university,
                'graduation_year': user.graduation_year,
                'gpa': float(user.gpa) if user.gpa else None,
                'current_position': user.current_position,
                'company': user.company,
                'work_experience_years': user.work_experience_years,
                'relevant_experience': user.relevant_experience,
                'interests': user.interests,
                'languages_spoken': user.languages_spoken,
                'linkedin_profile': user.linkedin_profile,
                'portfolio_website': user.portfolio_website,
                'preferred_countries': user.preferred_countries,
                'budget_range': user.budget_range,
                'academic_background': user.academic_background,
                'profile_completeness': user.profile_completeness,
                'has_complete_profile': user.profile_completeness >= 70,
                'can_send_emails': user.can_send_emails,
                'has_active_subscription': user.has_active_subscription
            }
            
            return JsonResponse({
                'success': True,
                'message': 'User profile functionality working correctly',
                'user_profile': profile_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error testing user profile: {str(e)}'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'General error: {str(e)}'
        }, status=500)
