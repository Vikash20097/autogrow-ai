from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()

def auto_post_job():
    """Background job to auto-post scheduled posts"""
    with app.app_context():
        try:
            from app.models import Post, db
            
            # Get current time
            current_time = datetime.now()
            
            # Find pending posts that should be posted
            pending_posts = Post.query.filter(
                Post.status == 'pending',
                Post.scheduled_time <= current_time
            ).all()
            
            if pending_posts:
                for post in pending_posts:
                    # Update post status to posted
                    post.status = 'posted'
                    db.session.commit()
                    print(f"Post ID {post.id} has been auto-posted")
            else:
                print("No posts to auto-post at this time")
                
        except Exception as e:
            print(f"Error in auto-post job: {e}")
            db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.models import User, Post
        # Create database tables
        from app import db
        db.create_all()
        
        # Initialize and start the scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=auto_post_job, trigger="interval", minutes=1)
        scheduler.start()
        
        # Ensure scheduler shuts down properly
        atexit.register(lambda: scheduler.shutdown())
    
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
