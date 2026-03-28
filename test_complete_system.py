#!/usr/bin/env python3
"""
Complete System Test Script for AutoGrow-AI
This script tests all major functionality of the application.
"""

import os
import sys
import requests
import time
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_reset():
    """Test database reset functionality"""
    print("=== Testing Database Reset ===")
    try:
        import reset_database
        reset_database.reset_database()
        print("✓ Database reset completed successfully")
        return True
    except Exception as e:
        print(f"✗ Database reset failed: {e}")
        return False

def test_flask_app():
    """Test Flask application startup and basic routes"""
    print("=== Testing Flask Application ===")
    try:
        from app import create_app
        app = create_app()
        print("✓ Flask app created successfully")
        
        # Test app context
        with app.app_context():
            from app.models import User, Post, AutoReply, AutoMode, ChatLog
            print("✓ All models imported successfully")
            
            # Test database connection
            from app import db
            db.create_all()
            print("✓ Database tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def test_routes():
    """Test all routes are accessible"""
    print("=== Testing Routes ===")
    try:
        from app import create_app
        app = create_app()
        client = app.test_client()
        
        # Test dashboard
        response = client.get('/dashboard')
        if response.status_code == 200:
            print("✓ Dashboard route accessible")
        else:
            print(f"✗ Dashboard route failed with status {response.status_code}")
            return False
            
        # Test create post
        response = client.get('/create-post')
        if response.status_code == 200:
            print("✓ Create post route accessible")
        else:
            print(f"✗ Create post route failed with status {response.status_code}")
            return False
            
        # Test auto reply
        response = client.get('/auto-reply')
        if response.status_code == 200:
            print("✓ Auto reply route accessible")
        else:
            print(f"✗ Auto reply route failed with status {response.status_code}")
            return False
            
        # Test AI caption
        response = client.get('/ai-caption')
        if response.status_code == 200:
            print("✓ AI caption route accessible")
        else:
            print(f"✗ AI caption route failed with status {response.status_code}")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Routes test failed: {e}")
        return False

def test_models():
    """Test database models and relationships"""
    print("=== Testing Models ===")
    try:
        from app import create_app, db
        from app.models import User, Post, AutoReply, AutoMode, ChatLog
        
        app = create_app()
        with app.app_context():
            # Test User model
            user = User.query.filter_by(id=1).first()
            if not user:
                user = User(id=1, username='testuser', email='test@example.com')
                user.set_password('testpass')
                db.session.add(user)
                db.session.commit()
            print("✓ User model working")
            
            # Test Post model
            post = Post(caption="Test post")
            db.session.add(post)
            db.session.commit()
            print("✓ Post model working")
            
            # Test AutoReply model
            auto_reply = AutoReply(keyword="hello", reply_text="Hi there!", user_id=1)
            db.session.add(auto_reply)
            db.session.commit()
            print("✓ AutoReply model working")
            
            # Test AutoMode model
            auto_mode = AutoMode(user_id=1, is_enabled=True)
            auto_mode.save()
            print("✓ AutoMode model working")
            
            # Test ChatLog model
            chat_log = ChatLog(user_message="Hello", bot_reply="Hi", user_id=1)
            db.session.add(chat_log)
            db.session.commit()
            print("✓ ChatLog model working")
            
        return True
    except Exception as e:
        print(f"✗ Models test failed: {e}")
        return False

def test_scheduler():
    """Test scheduler functionality"""
    print("=== Testing Scheduler ===")
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            from app.routes import scheduler
            if scheduler.running:
                print("✓ Scheduler is running")
                return True
            else:
                print("✗ Scheduler is not running")
                return False
    except Exception as e:
        print(f"✗ Scheduler test failed: {e}")
        return False

def test_functions():
    """Test key functions"""
    print("=== Testing Functions ===")
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            from app.routes import generate_caption, get_smart_reply, check_access, increment_usage
            
            # Test caption generation
            caption = generate_caption("gym")
            if caption and len(caption) > 0:
                print("✓ Caption generation working")
            else:
                print("✗ Caption generation failed")
                return False
                
            # Test smart reply
            reply = get_smart_reply("hello")
            if reply and len(reply) > 0:
                print("✓ Smart reply working")
            else:
                print("✗ Smart reply failed")
                return False
                
            # Test access check
            has_access = check_access(1, 'post')
            print(f"✓ Access check working (has access: {has_access})")
            
        return True
    except Exception as e:
        print(f"✗ Functions test failed: {e}")
        return False

def test_static_files():
    """Test static files and templates"""
    print("=== Testing Static Files ===")
    try:
        # Check if static directory exists
        static_dir = Path("static")
        if static_dir.exists():
            print("✓ Static directory exists")
        else:
            print("✗ Static directory missing")
            return False
            
        # Check if uploads directory exists
        uploads_dir = Path("static/uploads")
        if uploads_dir.exists():
            print("✓ Uploads directory exists")
        else:
            print("✗ Uploads directory missing")
            return False
            
        # Check if templates directory exists
        templates_dir = Path("app/templates")
        if templates_dir.exists():
            print("✓ Templates directory exists")
        else:
            print("✗ Templates directory missing")
            return False
            
        # Check key template files
        key_templates = ['base.html', 'dashboard_safe.html', 'create_post.html', 'auto_reply.html', 'ai_caption.html']
        for template in key_templates:
            template_path = templates_dir / template
            if template_path.exists():
                print(f"✓ Template {template} exists")
            else:
                print(f"✗ Template {template} missing")
                return False
                
        return True
    except Exception as e:
        print(f"✗ Static files test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧪 AutoGrow-AI Complete System Test")
    print("=" * 50)
    
    tests = [
        ("Database Reset", test_database_reset),
        ("Flask Application", test_flask_app),
        ("Routes", test_routes),
        ("Models", test_models),
        ("Scheduler", test_scheduler),
        ("Functions", test_functions),
        ("Static Files", test_static_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print("-" * 30)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 50)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   Then visit: http://localhost:5000/dashboard")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)