# AutoGrow-AI

A modern Flask web application with user authentication, featuring a sleek dark theme and responsive design.

## Features

### 🛡️ Security & Authentication
- **Secure Password Hashing**: Uses Werkzeug's generate_password_hash for secure password storage
- **Session Management**: Flask-Login for robust session handling
- **Input Validation**: Email format validation and password strength requirements
- **CSRF Protection**: Disabled for development (can be enabled for production)

### 🎨 Modern UI/UX
- **Dark Theme**: Sleek, modern dark color scheme with accent colors
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Gradient Accents**: Beautiful gradient backgrounds and hover effects
- **Smooth Animations**: CSS transitions and hover effects for better user experience

### 📱 User Interface
- **Login Page**: Clean authentication interface with form validation
- **Signup Page**: User registration with email and password validation
- **Dashboard**: Personalized welcome page with user information
- **Flash Messages**: Success, error, and info notifications with auto-hide

### 🔧 Technical Features
- **SQLite Database**: Lightweight database for user storage
- **Flask Blueprints**: Modular code organization
- **Template Inheritance**: Base template for consistent layout
- **Form Handling**: POST method form processing with validation

## Project Structure

```
AutoGrow-AI/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── test_app.py           # Basic functionality tests
├── README.md             # Project documentation
├── app/                  # Application package
│   ├── __init__.py       # Flask app factory
│   ├── models.py         # Database models (User)
│   ├── routes.py         # Authentication routes
│   ├── templates/        # HTML templates
│   │   ├── base.html     # Base template with layout
│   │   ├── login.html    # Login page
│   │   ├── signup.html   # Registration page
│   │   └── dashboard.html # User dashboard
│   └── static/          # Static assets
│       ├── css/
│       │   └── style.css # Modern dark theme styles
│       └── js/
└── autogrow.db          # SQLite database (created on first run)
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Application
Open your browser and navigate to: `http://127.0.0.1:5000`

## Routes

- **`/`** - Redirects to login if not authenticated, otherwise to dashboard
- **`/login`** - User login page
- **`/signup`** - User registration page
- **`/dashboard`** - User dashboard (requires authentication)
- **`/logout`** - Logout and redirect to login

## Database Schema

The application uses SQLite with a single `User` table:

```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

### Password Security
- Passwords are hashed using Werkzeug's secure hashing algorithm
- No plain text passwords are stored in the database
- Password validation requires minimum 6 characters with letters and numbers

### Session Management
- Flask-Login handles user sessions securely
- Users are automatically redirected to login when accessing protected routes
- Logout functionality properly clears the session

### Input Validation
- Email format validation using regex patterns
- Required field validation for all forms
- Username and email uniqueness enforcement

## Development Notes

### CSRF Protection
CSRF protection is disabled for development purposes by setting:
```python
app.config['WTF_CSRF_ENABLED'] = False
```

For production deployment, enable CSRF protection and use a secure secret key.

### Database Initialization
The database is automatically created on first run when accessing any route that requires the database.

### Debug Mode
The application runs in debug mode for development, providing helpful error messages and auto-reloading.

## Testing

Run the basic functionality test:
```bash
python test_app.py
```

This will verify:
- Server accessibility
- Page loading
- Authentication redirects

## Customization

### Styling
The CSS is organized with CSS custom properties (variables) for easy theming:
- `--bg-color`: Background color
- `--card-bg`: Card background color
- `--accent-color`: Primary accent color
- `--text-primary`: Primary text color

### Adding Features
To add new features:
1. Create new routes in `app/routes.py`
2. Add templates in `app/templates/`
3. Update CSS in `app/static/css/style.css` if needed
4. Consider database models in `app/models.py` for data storage

## Production Deployment

For production deployment:
1. Set `debug=False` in app.py
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Enable CSRF protection
4. Use a secure secret key
5. Configure proper database (PostgreSQL, MySQL)
6. Set up HTTPS
7. Configure proper logging

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## Support

For issues, questions, or feature requests, please create an issue in the repository.