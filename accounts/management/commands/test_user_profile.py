from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Test user profile functionality'

    def handle(self, *args, **options):
        self.stdout.write('Testing user profile functionality...')
        
        try:
            # Create a test user with profile data
            with transaction.atomic():
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
                
                self.stdout.write(f'Created user: {user.email}')
                self.stdout.write(f'Full name: {user.full_name}')
                self.stdout.write(f'Academic background: {user.academic_background}')
                self.stdout.write(f'Profile completeness: {user.profile_completeness}%')
                
                # Test profile completeness calculation
                self.stdout.write(f'Has complete profile: {user.profile_completeness >= 70}')
                
                # Clean up
                user.delete()
                self.stdout.write('Test user deleted successfully')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            return
            
        self.stdout.write(self.style.SUCCESS('User profile functionality test completed successfully!'))
