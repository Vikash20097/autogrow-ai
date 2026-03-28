#!/usr/bin/env python3
"""
Database Reset Script for AutoGrow-AI
This script will delete the old database and create a fresh one with all tables.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Post, AutoReply, AutoMode, ChatLog

def reset_database():
    """Reset the database by deleting old file and creating new tables"""
    app = create_app()
    
    with app.app_context():
        # Delete old database file if it exists
        db_path = Path("instance/autogrow.db")
        if db_path.exists():
            print(f"Deleting old database: {db_path}")
            db_path.unlink()
        
        # Create all tables
        print("Creating new database tables...")
        db.create_all()
        
        # Create default user if it doesn't exist
        default_user = User.query.filter_by(id=1).first()
        if not default_user:
            print("Creating default user...")
            default_user = User(
                id=1,
                username='default',
                email='default@example.com'
            )
            default_user.set_password('default')
            db.session.add(default_user)
            db.session.commit()
            print("Default user created successfully!")
        
        print("Database reset completed successfully!")
        print(f"Database location: {db_path.absolute()}")

if __name__ == "__main__":
    reset_database()