#!/usr/bin/env python3
"""
Simple test to check if the create-post route works
"""

import sys
import os
sys.path.append('.')

from app import create_app, db
from app.models import Post
from datetime import datetime

def test_route_directly():
    """Test the create-post route directly"""
    print("Testing create-post route directly...")
    try:
        app = create_app()
        with app.test_client() as client:
            # Test POST request
            response = client.post('/create-post', data={
                'caption': 'Test caption from direct test',
                'scheduled_time': '2026-03-28T15:00'
            })
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 302:
                print("✅ Redirect successful!")
                print(f"Redirect location: {response.location}")
            else:
                print("❌ No redirect - checking response content...")
                content = response.get_data(as_text=True)
                print(f"Content preview: {content[:500]}...")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_database_after_route():
    """Check database after route test"""
    print("\nChecking database after route test...")
    try:
        app = create_app()
        with app.app_context():
            posts = Post.query.all()
            print(f"✅ Found {len(posts)} posts in database")
            for post in posts:
                print(f"  - Post {post.id}: {post.caption[:50]}...")
    except Exception as e:
        print(f"❌ Database query failed: {e}")

if __name__ == "__main__":
    print("Starting simple route test...")
    print("=" * 50)
    
    test_route_directly()
    test_database_after_route()
    
    print("\n" + "=" * 50)
    print("Test completed.")