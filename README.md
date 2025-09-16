# UniWorld - Master's Program Search Platform

A comprehensive platform for students to search for master's programs in European universities, starting with Italy. The platform provides free access to browse university and program information, with premium features for sending emails directly to coordinators.

## 🌟 Features

### Free Features
- ✅ Browse universities and programs
- ✅ Search and filter by country, field of study, degree level, university, language
- ✅ View detailed program information
- ✅ Add programs to favorites
- ✅ User registration and authentication
- ✅ User dashboard with profile management

### Premium Features (Subscription Required)
- 🔒 Send emails directly to coordinators through the platform
- 🔒 Access coordinator contact information
- 🔒 Use professional email templates
- 🔒 Send bulk emails to multiple coordinators
- 🔒 Advanced email tracking and history

### Subscription Plans
- **Free Plan**: Browse and search only
- **Premium Plan**: 50 emails/month + all free features
- **Pro Plan**: 200 emails/month + bulk email + all features

## 🛠️ Technology Stack

- **Backend**: Django 5.2 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Styling**: Tailwind CSS
- **Authentication**: JWT tokens
- **Payments**: Stripe integration
- **API Documentation**: Swagger/OpenAPI with drf-spectacular

## 📁 Project Structure

```
uniworld/
├── accounts/                 # User management and authentication
├── universities/            # University, program, and coordinator models
├── payments/               # Subscription and payment management
├── uniworld_backend/       # Django project settings and views
├── csv_templates/          # CSV templates for data import
├── frontend.html          # Main frontend interface
├── app.js                 # Frontend JavaScript logic
├── styles.css             # Custom CSS styles
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

## 🗄️ Database Schema

### Core Models
1. **User** - Django's built-in user model with extended functionality
2. **University** - University information with unique IDs
3. **Program** - Master's programs with requirements and details
4. **Coordinator** - Program coordinators with contact information
5. **Subscription** - User subscription management with Stripe integration
6. **Payment** - Payment transaction records
7. **EmailLog** - Track emails sent through the platform

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
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

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Import sample data (optional)**
   ```bash
   python manage.py import_csv universities.csv
   python manage.py import_csv programs.csv
   python manage.py import_csv coordinators.csv
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/api/docs/

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/change-password/` - Change password

### Universities & Programs
- `GET /api/universities/` - List universities
- `GET /api/programs/` - List programs
- `GET /api/coordinators/` - List coordinators
- `GET /api/search/` - Advanced search with filters
- `GET /api/countries/` - List countries
- `GET /api/fields-of-study/` - List fields of study

### Email & Communication
- `POST /api/send-email/` - Send individual email
- `POST /api/send-bulk-email/` - Send bulk emails

### Payments & Subscriptions
- `POST /api/create-payment-session/` - Create Stripe payment session
- `POST /api/stripe-webhook/` - Stripe webhook handler
- `GET /api/user-subscription/<user_id>/` - Get user subscription

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe (for production)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 📊 Data Import

### CSV Templates
The project includes CSV templates for importing data:

1. **universities.csv** - University information
2. **programs.csv** - Program details
3. **coordinators.csv** - Coordinator contact information

### Import Commands
```bash
python manage.py import_csv universities.csv
python manage.py import_csv programs.csv
python manage.py import_csv coordinators.csv
```

## 🎯 Usage Examples

### Search for Programs
```bash
curl "http://localhost:8000/api/search/?country=Italy&field_of_study=Computer Science&degree_level=master"
```

### User Registration
```bash
curl -X POST "http://localhost:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### User Login
```bash
curl -X POST "http://localhost:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

## 🔒 Security Features

- **Subscription-based email access** - Only premium users can send emails
- **Email limits** - Monthly email quotas for premium users
- **Input validation** - All user inputs are validated
- **CSRF protection** - Django's built-in CSRF protection
- **Secure authentication** - JWT token-based authentication

## 🎨 Frontend Features

- **Responsive design** - Works on desktop, tablet, and mobile
- **Modern UI** - Clean and professional interface
- **Real-time search** - Instant search results
- **Pagination** - Efficient data loading
- **Modal dialogs** - Smooth user interactions
- **Notifications** - User feedback system
- **Favorites system** - Save preferred programs

## 🧪 Testing

### Manual Testing
1. **User Registration/Login** - Test authentication flow
2. **Program Search** - Test search filters and results
3. **Subscription Flow** - Test plan selection and payment
4. **Email Features** - Test email sending (premium users)
5. **Favorites** - Test adding/removing favorites

### API Testing
Use the provided API endpoints with tools like Postman or curl to test the backend functionality.

## 🚀 Deployment

### Production Setup
1. **Configure PostgreSQL** - Replace SQLite with PostgreSQL
2. **Set up environment variables** - Configure production settings
3. **Collect static files** - `python manage.py collectstatic`
4. **Set up web server** - Configure Nginx/Apache
5. **Set up WSGI** - Configure Gunicorn/uWSGI
6. **Configure Stripe** - Set up production Stripe keys

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🔮 Future Development

### Planned Features
- **React/Next.js frontend** - Modern frontend framework
- **Mobile app** - React Native or Flutter
- **Expand coverage** - All European countries
- **Advanced analytics** - User behavior tracking
- **University rankings** - Integration with ranking systems
- **Application tracking** - Track application status
- **Social features** - User reviews and ratings

### API Extensions
- **Real-time notifications** - WebSocket integration
- **File uploads** - Document submission
- **AI-powered search** - Intelligent program recommendations
- **Social integration** - Share programs with friends
- **University API** - Direct integration with university systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and API docs
- **Issues**: Create an issue in the repository
- **Discussions**: Use GitHub Discussions for questions

### Common Issues
- **Database errors**: Run migrations with `python manage.py migrate`
- **Import errors**: Install dependencies with `pip install -r requirements.txt`
- **Email not working**: Check subscription status and email limits
- **Search not working**: Verify data is imported correctly

## 📞 Contact

For support and questions:
- **Email**: [your-email@example.com]
- **GitHub**: [your-github-username]
- **LinkedIn**: [your-linkedin-profile]

---

**Made with ❤️ for students seeking their perfect master's program in Europe**