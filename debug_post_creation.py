#!/usr/bin/env python3
"""
Debug script to test post creation step by step
"""

import sys
import os
sys.path.append('.')

from app import create_app, db
from app.models import Post, User
from datetime import datetime

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        app = create_app()
        with app.app_context():
            # Test if we can query the database
            users = User.query.all()
            print(f"✅ Database connection successful. Found {len(users)} users.")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_user_creation():
    """Test creating default user"""
    print("\nTesting user creation...")
    try:
        app = create_app()
        with app.app_context():
            # Check if default user exists
            user = User.query.filter_by(id=1).first()
            if not user:
                user = User(id=1, username='default', email='default@example.com')
                user.set_password('default')
                db.session.add(user)
                db.session.commit()
                print("✅ Default user created successfully")
            else:
                print("✅ Default user already exists")
            return True
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return False

def test_post_creation():
    """Test creating a post directly"""
    print("\nTesting post creation...")
    try:
        app = create_app()
        with app.app_context():
            # Create a test post
            new_post = Post(
                caption="Test post from debug script",
                image=None,
                status="pending",
                scheduled_time=datetime.now(),
                user_id=1
            )
            
            db.session.add(new_post)
            db.session.commit()
            print("✅ Post created successfully")
            print(f"Post ID: {new_post.id}")
            return True
    except Exception as e:
        print(f"❌ Post creation failed: {e}")
        return False

def test_post_query():
    """Test querying posts"""
    print("\nTesting post query...")
    try:
        app = create_app()
        with app.app_context():
            posts = Post.query.all()
            print(f"✅ Found {len(posts)} posts in database")
            for post in posts:
                print(f"  - Post {post.id}: {post.caption[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Post query failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting debug tests...")
    print("=" * 50)
    
    success = True
    success &= test_database_connection()
    success &= test_user_creation()
    success &= test_post_creation()
    success &= test_post_query()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")