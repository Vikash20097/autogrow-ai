# AutoGrow-AI - Complete Social Media Management Suite

A comprehensive Flask-based social media management application with AI-powered automation, auto-reply bots, scheduling, and subscription management.

## 🚀 Features

### Core Features
- **Smart Dashboard** - Modern dark theme with real-time analytics and statistics
- **Post Management** - Create, schedule, and manage social media posts
- **Auto Reply Bot** - WhatsApp-style chatbot with smart keyword matching
- **AI Caption Generator** - Fake AI system for generating engaging captions
- **Auto Mode** - Full automation with scheduled content generation
- **Subscription System** - Free/pro tier with trial limits and usage tracking

### Advanced Features
- **Real-time Scheduler** - Background job scheduler for automated posting
- **Smart Reply System** - Intelligent keyword-based responses with comma-separated keywords
- **Usage Tracking** - Monitor trial usage for posts, captions, and replies
- **Database Management** - Clean database reset and migration tools
- **Error Handling** - Robust error handling and safe template rendering

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python reset_database.py
   ```

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Visit the application:**
   Open your browser and go to `http://localhost:5000/dashboard`

## 📁 Project Structure

```
AutoGrow-AI/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (User, Post, AutoReply, etc.)
│   ├── routes.py            # All route handlers and business logic
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template with dark theme
│   │   ├── dashboard_safe.html  # Safe dashboard template
│   │   ├── create_post.html # Post creation form
│   │   ├── auto_reply.html  # Auto-reply bot management
│   │   └── ai_caption.html  # AI caption generator
│   └── static/              # CSS, JS, and uploaded files
│       ├── css/style.css    # Dark theme styles
│       └── js/main.js       # Interactive JavaScript
├── instance/                # Database files
├── static/uploads/          # User uploaded images
├── test_complete_system.py  # Comprehensive test suite
├── reset_database.py        # Database reset utility
└── app.py                   # Main application entry point
```

## 🎯 Usage Guide

### Dashboard
- View post statistics and analytics
- Quick access to all features
- Real-time usage tracking
- Auto mode status and controls

### Creating Posts
1. Go to **Create Post** from the dashboard
2. Add a caption (required)
3. Upload an image (optional)
4. Set a scheduled time (optional)
5. Click **Create Post** to schedule

### Auto Reply Bot
1. Go to **Auto Reply** from the dashboard
2. Add keyword-reply pairs
3. Use comma-separated keywords for multiple triggers
4. Test responses in the chat interface
5. Toggle rules on/off as needed

### AI Caption Generator
1. Go to **AI Caption** from the dashboard
2. Select a niche (gym, health, business, etc.)
3. Generate captions with one click
4. Copy and use in your posts

### Auto Mode
1. Toggle **Full Auto Mode** on/off
2. System will automatically generate and schedule posts
3. Monitor activity in the dashboard
4. Set usage limits and track consumption

### Subscription Management
- **Free Plan**: 5 posts, 5 captions, 5 replies per month
- **Pro Plan**: Unlimited access
- Usage tracked automatically
- Upgrade prompts when limits reached

## 🧪 Testing

Run the comprehensive test suite to verify all functionality:

```bash
python test_complete_system.py
```

This will test:
- Database reset functionality
- Flask application startup
- All route accessibility
- Database models and relationships
- Scheduler functionality
- Key functions and utilities
- Static files and templates

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Database
The application uses SQLite by default. Database files are stored in the `instance/` directory.

### Scheduler
The application includes a background scheduler that:
- Checks for posts to publish every 30 seconds
- Automatically updates post status from "pending" to "posted"
- Runs in the background when the app starts

## 🐛 Troubleshooting

### Common Issues

1. **Dashboard shows errors:**
   - Run `python reset_database.py` to reset the database
   - Check that all dependencies are installed

2. **Routes not accessible:**
   - Ensure Flask app is running
   - Check terminal for error messages
   - Verify port 5000 is not in use

3. **Database errors:**
   - Delete the `instance/` directory and rerun reset script
   - Check file permissions

4. **Static files not loading:**
   - Ensure `static/` directory exists
   - Check browser console for 404 errors

### Debug Mode
To enable debug mode, set in `.env`:
```env
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📊 Database Schema

### Tables
- **users**: User accounts with subscription status
- **posts**: Scheduled and posted content
- **auto_replies**: Keyword-reply rules for chatbot
- **auto_modes**: Auto mode status per user
- **chat_logs**: Conversation history

### Key Fields
- `user_id`: Links all records to users (default user_id = 1)
- `trial_*_used`: Tracks usage for free tier limits
- `is_pro`: Subscription status
- `status`: Post status (pending/posted)
- `scheduled_time`: When posts should be published

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection for forms
- Input validation and sanitization
- Safe template rendering with error handling
- Database isolation and proper relationships

## 🚀 Deployment

### Production Setup
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure a reverse proxy (Nginx)
4. Set up proper SSL certificates
5. Use a production database (PostgreSQL, MySQL)

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/autogrow
```

## 📈 Performance Optimization

- Database queries optimized with proper indexing
- Background scheduler for non-blocking operations
- Efficient template rendering
- Minimal JavaScript for fast loading
- Optimized CSS with dark theme variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework for the web application
- SQLAlchemy for database management
- APScheduler for background tasks
- Chart.js for analytics visualization
- FontAwesome for icons

## 📞 Support

For support and questions:
- Check the troubleshooting section above
- Review the test output for specific errors
- Ensure all dependencies are properly installed
- Verify database permissions and file access

---

**AutoGrow-AI** - Your complete social media management solution with AI-powered automation!