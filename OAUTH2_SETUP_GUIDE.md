# OAuth2 Email Integration Setup Guide

## Overview
This guide explains how to set up OAuth2 integration for Gmail and Outlook email services in the UniWorld platform.

## Current Status
- ✅ **Development Mode**: Currently active for testing
- ⚠️ **Production Mode**: Requires OAuth2 credentials setup

## Development Mode (Current)
The platform automatically detects development environment and uses simulated OAuth2 connections:

### Features:
- **Automatic Detection**: Detects localhost/127.0.0.1
- **Simulated Connections**: No real OAuth2 required
- **Test Credentials**: Uses demo email addresses
- **Full Functionality**: All features work for testing

### Test Accounts:
- **Gmail**: `test@gmail.com`
- **Outlook**: `test@outlook.com`

## Production Setup

### 1. Gmail OAuth2 Setup

#### Step 1: Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API

#### Step 2: Create OAuth2 Credentials
1. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
2. Application type: "Web application"
3. Name: "UniWorld Gmail Integration"
4. Authorized redirect URIs:
   - `http://yourdomain.com/oauth/gmail/callback/`
   - `https://yourdomain.com/oauth/gmail/callback/`

#### Step 3: Configure OAuth2
1. Copy the Client ID
2. Update `oauth2_config.js`:
```javascript
gmail: {
    clientId: 'your-actual-client-id.apps.googleusercontent.com',
    redirectUri: 'https://yourdomain.com/oauth/gmail/callback/',
    // ... other settings
}
```

### 2. Outlook OAuth2 Setup

#### Step 1: Azure Portal
1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" → "App registrations"
3. Click "New registration"

#### Step 2: Register Application
1. Name: "UniWorld Outlook Integration"
2. Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
3. Redirect URI: `https://yourdomain.com/oauth/outlook/callback/`

#### Step 3: Configure API Permissions
1. Go to "API permissions"
2. Add permission: "Microsoft Graph"
3. Select "Mail.Send" permission
4. Grant admin consent

#### Step 4: Get Client ID
1. Copy the Application (client) ID
2. Update `oauth2_config.js`:
```javascript
outlook: {
    clientId: 'your-actual-client-id',
    redirectUri: 'https://yourdomain.com/oauth/outlook/callback',
    // ... other settings
}
```

### 3. Backend OAuth2 Implementation

#### Django OAuth2 Views
Create OAuth2 callback handlers in `uniworld_backend/views.py`:

```python
def gmail_oauth_callback(request):
    # Handle Gmail OAuth2 callback
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    # Exchange code for access token
    # Store token securely
    # Return success response
    
def outlook_oauth_callback(request):
    # Handle Outlook OAuth2 callback
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    # Exchange code for access token
    # Store token securely
    # Return success response
```

#### URL Configuration
Add OAuth2 routes to `uniworld_backend/urls.py`:

```python
path('oauth/gmail/callback/', views.gmail_oauth_callback, name='gmail-oauth-callback'),
path('oauth/outlook/callback/', views.outlook_oauth_callback, name='outlook-oauth-callback'),
```

### 4. Environment Configuration

#### Development Environment
```javascript
// oauth2_config.js
const OAUTH2_CONFIG = {
    developmentMode: true, // Automatically enabled for localhost
    // ... other settings
};
```

#### Production Environment
```javascript
// oauth2_config.js
const OAUTH2_CONFIG = {
    developmentMode: false, // Disable for production
    gmail: {
        clientId: 'your-production-gmail-client-id',
        redirectUri: 'https://yourdomain.com/oauth/gmail/callback/',
        // ... other settings
    },
    outlook: {
        clientId: 'your-production-outlook-client-id',
        redirectUri: 'https://yourdomain.com/oauth/outlook/callback/',
        // ... other settings
    }
};
```

## Testing

### Development Testing
1. **Start Django server**: `python manage.py runserver`
2. **Open browser**: `http://127.0.0.1:8000`
3. **Login** to your account
4. **Go to Dashboard** → Email Integration
5. **Click "Connect Gmail"** or "Connect Outlook"
6. **Should see**: "Development Mode" notification
7. **Account shows**: "Connected" status

### Production Testing
1. **Deploy** to production server
2. **Configure** OAuth2 credentials
3. **Test** real OAuth2 flow
4. **Verify** email sending functionality

## Security Considerations

### OAuth2 Security
- **HTTPS Required**: All OAuth2 flows must use HTTPS in production
- **State Parameter**: Use state parameter to prevent CSRF attacks
- **Token Storage**: Store access tokens securely (encrypted)
- **Token Refresh**: Implement token refresh for long-lived access

### Data Protection
- **Minimal Scopes**: Only request necessary permissions
- **User Consent**: Always show clear consent screens
- **Token Expiration**: Handle token expiration gracefully
- **Revocation**: Allow users to revoke access

## Troubleshooting

### Common Issues

#### 1. "400. That's an error" (Gmail)
- **Cause**: Invalid client ID or redirect URI
- **Solution**: Check OAuth2 credentials in Google Cloud Console

#### 2. "Popup blocked"
- **Cause**: Browser blocking popup windows
- **Solution**: Allow popups for your domain

#### 3. "Invalid redirect URI"
- **Cause**: Redirect URI doesn't match registered URI
- **Solution**: Update redirect URI in OAuth2 configuration

#### 4. "Insufficient permissions"
- **Cause**: Missing API permissions
- **Solution**: Grant required permissions in Azure Portal

### Debug Mode
Enable debug logging in `app.js`:
```javascript
// Add to the top of app.js
const DEBUG_OAUTH2 = true;

// Add debug logs
if (DEBUG_OAUTH2) {
    console.log('OAuth2 Debug:', {
        provider: provider,
        clientId: clientId,
        redirectUri: redirectUri,
        authUrl: authUrl
    });
}
```

## Next Steps

### Immediate (Development)
1. ✅ **Test current implementation** - Development mode works
2. ✅ **Verify all features** - Email sending, settings, etc.
3. ✅ **Test user experience** - Dashboard, notifications, etc.

### Short Term (Production Ready)
1. **Set up OAuth2 credentials** - Gmail and Outlook
2. **Implement backend callbacks** - Django OAuth2 handlers
3. **Add token management** - Secure storage and refresh
4. **Test production flow** - End-to-end OAuth2

### Long Term (Advanced Features)
1. **Email templates** - Pre-built email templates
2. **Bulk email optimization** - Rate limiting, queuing
3. **Email analytics** - Track email performance
4. **Advanced filters** - Smart email filtering

## Support

### Documentation
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [OAuth2 RFC 6749](https://tools.ietf.org/html/rfc6749)

### Community
- [Google Developers Community](https://developers.google.com/community)
- [Microsoft Developer Community](https://developer.microsoft.com/en-us/community)

---

**Note**: This guide is for the UniWorld platform OAuth2 email integration. Always follow security best practices when implementing OAuth2 in production.
