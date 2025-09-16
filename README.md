"# UniWorld - Master's Program Search Platform

A comprehensive platform for students to search for master's programs in European universities, starting with Italy. The platform provides free access to browse university and program information, with premium features for sending emails directly to coordinators.

## Features

### Free Features
- Browse universities and programs
- Search and filter by country, field of study, degree level, etc.
- View detailed program information including requirements and fees
- Access coordinator contact information (public emails only)

### Premium Features (Subscription Required)
- Send emails directly to coordinators through the platform
- Use your own Gmail/Outlook account via OAuth2
- Send bulk emails to multiple coordinators
- Advanced filtering and search capabilities

## Technology Stack

- **Backend**: Django 5.2 with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Payments**: Stripe integration
- **Email**: OAuth2 integration with Gmail/Outlook
- **API Documentation**: Swagger/OpenAPI with drf-spectacular

## Project Structure

```
uniworld/
├── accounts/                 # User management and authentication
├── universities/            # University, program, and coordinator models
├── payments/               # Subscription and payment management
├── uniworld_backend/       # Django project settings
├── requirements.txt        # Python dependencies
├── config.env             # Environment configuration template
└── manage.py              # Django management script
```

## Database Schema

### Core Models
1. **User** - Extended Django user with premium features and OAuth2 tokens
2. **University** - University information and details
3. **Program** - Master's programs with requirements and details
4. **Coordinator** - Program coordinators with contact information
5. **Subscription** - User subscription management
6. **Payment** - Payment transaction records
7. **EmailLog** - Track emails sent through the platform

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mehdighzal/uniworld.git
   cd uniworld
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE uniworld_db;
   CREATE USER uniworld_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE uniworld_db TO uniworld_user;
   ```

5. **Configure environment variables**
   ```bash
   cp config.env .env
   # Edit .env with your actual values
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Populate sample data**
   ```bash
   python manage.py populate_sample_data
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Universities & Programs
- `GET /api/universities/` - List universities
- `GET /api/universities/{id}/` - University details
- `GET /api/programs/` - List programs
- `GET /api/programs/{id}/` - Program details
- `GET /api/coordinators/` - List coordinators
- `GET /api/search/` - Advanced search
- `GET /api/countries/` - List countries
- `GET /api/fields-of-study/` - List fields of study

### Payments & Subscriptions
- `GET /api/payments/subscriptions/` - User subscriptions
- `POST /api/payments/subscriptions/create/` - Create subscription
- `GET /api/payments/payments/` - Payment history
- `POST /api/payments/emails/send/` - Send emails (premium)
- `GET /api/payments/emails/` - Email logs

### API Documentation
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc documentation
- `GET /api/schema/` - OpenAPI schema

## Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# Database
DB_NAME=uniworld_db
DB_USER=uniworld_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Google OAuth2
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback/
```

## Usage Examples

### Search for Programs
```bash
curl "http://localhost:8000/api/search/?country=Italy&field_of_study=Computer Science&degree_level=master"
```

### Create User Account
```bash
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

## Future Development

### Planned Features
- React/Next.js web frontend
- React Native mobile app
- Expand to all European countries
- Advanced analytics and reporting
- University ranking integration
- Application tracking system

### API Extensions
- Real-time notifications
- File upload for documents
- Advanced search with AI
- Social features and reviews
- Integration with university systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository." 
