#!/usr/bin/env python3
"""
AI Integration Test Script for UniWorld Platform
This script tests the AI integration setup and functionality.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniworld_backend.settings')
django.setup()

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        'ai_services/__init__.py',
        'ai_services/email_suggestions.py',
        'ai_services/views.py',
        'ai_services/urls.py',
        'ai_services/templates.py',
        'uniworld_backend/settings.py',
        'uniworld_backend/urls.py',
        'app.js',
        'frontend.html',
        'requirements.txt',
        'config.env',
        '.env'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_django_setup():
    """Test Django configuration"""
    print("\n🔍 Testing Django setup...")
    
    try:
        from django.conf import settings
        from django.urls import reverse
        
        # Check if ai_services is in INSTALLED_APPS
        if 'ai_services' in settings.INSTALLED_APPS:
            print("✅ ai_services is in INSTALLED_APPS")
        else:
            print("❌ ai_services not found in INSTALLED_APPS")
            return False
        
        # Check if rest_framework is in INSTALLED_APPS
        if 'rest_framework' in settings.INSTALLED_APPS:
            print("✅ rest_framework is in INSTALLED_APPS")
        else:
            print("❌ rest_framework not found in INSTALLED_APPS")
            return False
        
        # Check OpenAI configuration
        if hasattr(settings, 'OPENAI_API_KEY'):
            print("✅ OPENAI_API_KEY is configured")
        else:
            print("❌ OPENAI_API_KEY not configured")
            return False
        
        if hasattr(settings, 'OPENAI_MODEL'):
            print("✅ OPENAI_MODEL is configured")
        else:
            print("❌ OPENAI_MODEL not configured")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

def test_module_imports():
    """Test that all modules can be imported"""
    print("\n🔍 Testing module imports...")
    
    try:
        # Test AI services imports
        from ai_services.email_suggestions import EmailSuggestionService, get_email_suggestions
        print("✅ ai_services.email_suggestions imported successfully")
        
        from ai_services.views import generate_email_suggestions, generate_subject_options
        print("✅ ai_services.views imported successfully")
        
        from ai_services.templates import AITemplateGenerator, get_ai_template
        print("✅ ai_services.templates imported successfully")
        
        # Test OpenAI import
        try:
            import openai
            print("✅ openai package imported successfully")
        except ImportError:
            print("❌ openai package not installed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Module import error: {e}")
        return False

def test_fallback_functionality():
    """Test fallback functionality when AI is not available"""
    print("\n🔍 Testing fallback functionality...")
    
    try:
        from ai_services.email_suggestions import EmailSuggestionService
        
        # Create service instance
        service = EmailSuggestionService()
        
        # Test fallback subject generation
        fallback_subject = service._fallback_subject(
            "Computer Science", "MIT", "inquiry"
        )
        if fallback_subject and "Computer Science" in fallback_subject:
            print("✅ Fallback subject generation works")
        else:
            print("❌ Fallback subject generation failed")
            return False
        
        # Test fallback content generation
        fallback_content = service._fallback_content(
            "Computer Science", "MIT", "Dr. Smith", "inquiry"
        )
        if fallback_content and "Dr. Smith" in fallback_content:
            print("✅ Fallback content generation works")
        else:
            print("❌ Fallback content generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback functionality error: {e}")
        return False

def test_api_endpoints():
    """Test that API endpoints are properly configured"""
    print("\n🔍 Testing API endpoints...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test AI endpoints exist
        endpoints = [
            'ai_services:generate_suggestions',
            'ai_services:generate_subjects',
            'ai_services:enhance_content',
            'ai_services:get_templates',
        ]
        
        for endpoint in endpoints:
            try:
                url = reverse(endpoint)
                print(f"✅ {endpoint} -> {url}")
            except Exception as e:
                print(f"❌ {endpoint} not found: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints error: {e}")
        return False

def test_configuration():
    """Test configuration files"""
    print("\n🔍 Testing configuration...")
    
    try:
        # Test config.env
        if os.path.exists('config.env'):
            with open('config.env', 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY' in content:
                    print("✅ config.env contains OPENAI_API_KEY")
                else:
                    print("❌ config.env missing OPENAI_API_KEY")
                    return False
        else:
            print("❌ config.env file not found")
            return False
        
        # Test .env
        if os.path.exists('.env'):
            print("✅ .env file exists")
        else:
            print("❌ .env file not found")
            return False
        
        # Test requirements.txt
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                content = f.read()
                if 'openai' in content and 'python-dotenv' in content:
                    print("✅ requirements.txt contains AI dependencies")
                else:
                    print("❌ requirements.txt missing AI dependencies")
                    return False
        else:
            print("❌ requirements.txt not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Integration Tests for UniWorld Platform")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_django_setup,
        test_module_imports,
        test_fallback_functionality,
        test_api_endpoints,
        test_configuration,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI integration is ready to use.")
        print("\n📋 Next steps:")
        print("1. Get your OpenAI API key from https://platform.openai.com/")
        print("2. Add it to config.env: OPENAI_API_KEY=sk-your-key-here")
        print("3. Copy config.env to .env: cp config.env .env")
        print("4. Install dependencies: pip install openai python-dotenv")
        print("5. Start Django server: python manage.py runserver")
        print("6. Test AI features in the browser!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("- Install missing packages: pip install openai python-dotenv")
        print("- Check file paths and permissions")
        print("- Verify Django settings configuration")
        print("- Ensure all required files exist")

if __name__ == "__main__":
    main()
