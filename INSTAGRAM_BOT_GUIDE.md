# Instagram Auto-Poster Bot

A Python automation system that uses Selenium WebDriver to automatically post images and captions to Instagram.

## 🚀 Features

- **Automatic Login**: Securely logs into Instagram using provided credentials
- **Database Integration**: Fetches latest pending posts from existing SQLite database
- **Smart Upload**: Automatically uploads images with captions and hashtags
- **Human-like Behavior**: Random delays and retry logic to avoid detection
- **Error Handling**: Comprehensive error handling and logging
- **Status Tracking**: Updates database to mark posts as completed

## 📋 Requirements

### Python Dependencies
```bash
pip install -r bot_requirements.txt
```

### System Requirements
- Chrome browser installed
- Python 3.7+
- Access to Instagram account (not using API)

## 🔧 Configuration

### 1. Update Credentials
Edit `bot.py` and replace the Instagram credentials:

```python
INSTAGRAM_USERNAME = "your_instagram_username"
INSTAGRAM_PASSWORD = "your_instagram_password"
```

### 2. Database Setup
The bot automatically connects to your existing AutoGrow-AI database:
- Database path: `instance/autogrow.db`
- Table: `post`
- Status: Looks for posts with `status = 'pending'`

### 3. Image Storage
Images are expected to be in: `static/uploads/`
- Bot fetches image filename from database
- Constructs full path: `static/uploads/{image_filename}`

## 🎯 Usage

### Basic Usage
```bash
python bot.py
```

### Headless Mode
For automated runs without browser window:
```python
bot = InstagramBot(
    username="your_username",
    password="your_password",
    headless=True  # Set to True for headless mode
)
```

## 📊 Database Schema

The bot works with the existing Post model:

```sql
CREATE TABLE post (
    id INTEGER PRIMARY KEY,
    caption TEXT NOT NULL,
    image VARCHAR(255),
    platform VARCHAR(50),
    category VARCHAR(50),
    priority VARCHAR(50),
    schedule_time DATETIME,
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Bot Workflow

1. **Initialize WebDriver**: Setup Chrome with anti-detection measures
2. **Login to Instagram**: Enter credentials and handle popups
3. **Fetch Post**: Get latest pending post from database
4. **Upload Image**: Click create button, upload file, click next
5. **Add Caption**: Enter caption with auto-generated hashtags
6. **Post**: Click share and wait for completion
7. **Update Status**: Mark post as 'posted' in database

## 🏷️ Hashtag Generation

The bot automatically adds relevant hashtags based on post category:

| Category | Hashtags |
|----------|----------|
| gym | `#gym #fitness #workout #motivation #fitlife` |
| salon | `#salon #beauty #hair #makeup #style #glamour` |
| cafe | `#cafe #coffee #food #lunch #brunch #foodie` |
| business | `#business #entrepreneur #startup #success #motivation #hustle` |
| fashion | `#fashion #style #outfit #trending #ootd #fashionista` |
| travel | `#travel #wanderlust #adventure #explore #vacation #travelgram` |
| tech | `#tech #technology #innovation #gadgets #programming #coding` |
| health | `#health #wellness #lifestyle #fit #nutrition #healthy` |
| education | `#education #learning #knowledge #study #school #university` |
| general | `#instagood #photooftheday #instadaily #picoftheday #instamood` |

## ⚠️ Important Notes

### Instagram Terms of Service
- This bot uses Selenium automation, not official API
- May violate Instagram's Terms of Service
- Use at your own risk
- Consider rate limiting and human-like behavior

### Best Practices
- Use realistic delays (2-5 seconds between actions)
- Don't run too frequently (Instagram may flag automation)
- Monitor logs for errors and issues
- Test with a test account first

### Security
- Never commit credentials to version control
- Use environment variables for production
- Consider using app passwords if available

## 🐛 Troubleshooting

### Common Issues

**ChromeDriver Issues**:
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager
```

**Login Failures**:
- Check credentials are correct
- Instagram may require additional verification
- Try manual login first to ensure account is accessible

**Element Not Found**:
- Instagram may have updated their UI
- Check selectors in bot.py match current Instagram layout
- Update XPath selectors if needed

**Image Upload Failures**:
- Verify image path is correct
- Check image file exists in `static/uploads/`
- Ensure image format is supported by Instagram

### Logs
Check `instagram_bot.log` for detailed error information:
```bash
tail -f instagram_bot.log
```

## 🔗 Integration with AutoGrow-AI

This bot integrates seamlessly with your existing AutoGrow-AI system:

1. **Create Posts**: Use the web interface to create posts in the dashboard
2. **Schedule Posts**: Set status to 'pending' for automation
3. **Run Bot**: Execute `python bot.py` to post pending content
4. **Track Status**: Posts automatically marked as 'posted' after completion

## 🚀 Advanced Usage

### Custom Hashtags
Modify the `get_hashtags_for_category()` method to add custom hashtags:

```python
def get_hashtags_for_category(self, caption, category):
    custom_hashtags = "#yourbrand #customhashtag"
    return f"{caption}\n\n{custom_hashtags}"
```

### Multiple Accounts
Create multiple bot instances for different accounts:

```python
accounts = [
    {"username": "account1", "password": "pass1"},
    {"username": "account2", "password": "pass2"}
]

for account in accounts:
    bot = InstagramBot(account["username"], account["password"])
    bot.run()
```

### Scheduled Execution
Use cron (Linux/Mac) or Task Scheduler (Windows) for automated runs:

```bash
# Run every hour
0 * * * * /usr/bin/python3 /path/to/bot.py
```

## 📈 Monitoring

The bot provides comprehensive logging:
- **INFO**: General operation flow
- **WARNING**: Non-critical issues and retries
- **ERROR**: Critical failures
- **DEBUG**: Detailed operation information

Monitor logs to ensure smooth operation and catch issues early.

## 🤖 Future Enhancements

Potential improvements:
- Story posting capability
- Reel upload support
- Comment automation
- Analytics integration
- Multi-platform support (Facebook, Twitter)
- Image editing and watermarking
- A/B testing for captions and hashtags

---

**⚠️ Disclaimer**: This tool is for educational purposes. Use responsibly and in compliance with Instagram's terms of service.