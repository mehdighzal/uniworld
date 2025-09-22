from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import json
import requests

User = get_user_model()


@require_http_methods(["GET"])
@csrf_exempt
def get_oauth_tokens(request):
    """Get OAuth2 tokens for the current user"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'User not authenticated'
            }, status=401)
        
        user = request.user
        
        # Return token information (without exposing actual tokens for security)
        token_info = {
            'success': True,
            'gmail': {
                'has_access_token': bool(user.google_access_token),
                'has_refresh_token': bool(user.google_refresh_token),
                'token_expiry': user.google_token_expiry.isoformat() if user.google_token_expiry else None,
                'is_expired': user.google_token_expiry < timezone.now() if user.google_token_expiry else True
            },
            'outlook': {
                'has_access_token': bool(user.microsoft_access_token),
                'has_refresh_token': bool(user.microsoft_refresh_token),
                'token_expiry': user.microsoft_token_expiry.isoformat() if user.microsoft_token_expiry else None,
                'is_expired': user.microsoft_token_expiry < timezone.now() if user.microsoft_token_expiry else True
            }
        }
        
        return JsonResponse(token_info)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error retrieving token information: {str(e)}'
        }, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def refresh_oauth_token(request):
    """Refresh OAuth2 tokens"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'User not authenticated'
            }, status=401)
        
        data = json.loads(request.body)
        provider = data.get('provider')
        
        if provider not in ['gmail', 'outlook']:
            return JsonResponse({
                'success': False,
                'error': 'Invalid provider'
            }, status=400)
        
        user = request.user
        
        if provider == 'gmail':
            if not user.google_refresh_token:
                return JsonResponse({
                    'success': False,
                    'error': 'No refresh token available'
                }, status=400)
            
            # Refresh Gmail token
            new_token_data = refresh_gmail_token(user.google_refresh_token)
            
            if new_token_data:
                user.google_access_token = new_token_data.get('access_token')
                if new_token_data.get('refresh_token'):
                    user.google_refresh_token = new_token_data.get('refresh_token')
                
                expires_in = new_token_data.get('expires_in', 3600)
                user.google_token_expiry = timezone.now() + timedelta(seconds=expires_in)
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Gmail token refreshed successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to refresh Gmail token'
                }, status=500)
        
        elif provider == 'outlook':
            if not user.microsoft_refresh_token:
                return JsonResponse({
                    'success': False,
                    'error': 'No refresh token available'
                }, status=400)
            
            # Refresh Outlook token
            new_token_data = refresh_outlook_token(user.microsoft_refresh_token)
            
            if new_token_data:
                user.microsoft_access_token = new_token_data.get('access_token')
                if new_token_data.get('refresh_token'):
                    user.microsoft_refresh_token = new_token_data.get('refresh_token')
                
                expires_in = new_token_data.get('expires_in', 3600)
                user.microsoft_token_expiry = timezone.now() + timedelta(seconds=expires_in)
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Outlook token refreshed successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to refresh Outlook token'
                }, status=500)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error refreshing token: {str(e)}'
        }, status=500)


def refresh_gmail_token(refresh_token):
    """Refresh Gmail access token using refresh token"""
    try:
        token_url = 'https://oauth2.googleapis.com/token'
        
        data = {
            'client_id': getattr(settings, 'GOOGLE_CLIENT_ID', ''),
            'client_secret': getattr(settings, 'GOOGLE_CLIENT_SECRET', ''),
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Gmail token refresh failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error refreshing Gmail token: {str(e)}")
        return None


def refresh_outlook_token(refresh_token):
    """Refresh Outlook access token using refresh token"""
    try:
        token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        
        data = {
            'client_id': getattr(settings, 'MICROSOFT_CLIENT_ID', ''),
            'client_secret': getattr(settings, 'MICROSOFT_CLIENT_SECRET', ''),
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Outlook token refresh failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error refreshing Outlook token: {str(e)}")
        return None
