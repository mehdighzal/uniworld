// OAuth2 Configuration for UniWorld Platform
// This file contains the OAuth2 settings for Gmail and Outlook integration

const OAUTH2_CONFIG = {
    // Gmail OAuth2 Configuration
    gmail: {
        clientId: 'your-gmail-client-id.apps.googleusercontent.com',
        redirectUri: 'http://127.0.0.1:8000/oauth/gmail/callback',
        scope: 'https://www.googleapis.com/auth/gmail.send',
        authUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
        tokenUrl: 'https://oauth2.googleapis.com/token',
        // For development, you can use these test credentials
        // clientId: '123456789-abcdefghijklmnop.apps.googleusercontent.com',
        // redirectUri: 'http://localhost:8000/oauth/gmail/callback'
    },
    
    // Outlook OAuth2 Configuration
    outlook: {
        clientId: 'your-outlook-client-id',
        redirectUri: 'http://127.0.0.1:8000/oauth/outlook/callback',
        scope: 'https://graph.microsoft.com/Mail.Send',
        authUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
        tokenUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        // For development, you can use these test credentials
        // clientId: '12345678-1234-1234-1234-123456789012',
        // redirectUri: 'http://localhost:8000/oauth/outlook/callback'
    },
    
    // Development Mode - Set to true for testing without real OAuth2
    developmentMode: true,
    
    // Development credentials (for testing only)
    development: {
        gmail: {
            email: 'test@gmail.com',
            accessToken: 'dev-gmail-token-12345'
        },
        outlook: {
            email: 'test@outlook.com',
            accessToken: 'dev-outlook-token-67890'
        }
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OAUTH2_CONFIG;
}
