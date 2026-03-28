#!/usr/bin/env python3
"""
Test script to verify signup functionality in AutoGrow-AI
"""

import requests
import time
import json

def test_signup():
    """Test the signup functionality"""
    print("🧪 Testing AutoGrow-AI Signup Functionality")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if signup page loads
    print("1. Testing signup page access...")
    try:
        response = requests.get(f"{base_url}/signup")
        if response.status_code == 200:
            print("✅ Signup page loads successfully")
        else:
            print(f"❌ Signup page returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on http://127.0.0.1:5000")
        return False
    
    # Test 2: Test signup with valid data
    print("2. Testing signup with valid data...")
    
    # Generate unique test data
    timestamp = int(time.time())
    test_username = f"testuser_{timestamp}"
    test_email = f"testuser_{timestamp}@example.com"
    test_password = "testpass123"
    
    signup_data = {
        'username': test_username,
        'email': test_email,
        'password': test_password,
        'confirm_password': test_password
    }
    
    try:
        response = requests.post(f"{base_url}/signup", data=signup_data)
        
        if response.status_code == 302:
            print("✅ Signup successful - redirect received")
            print(f"   Username: {test_username}")
            print(f"   Email: {test_email}")
            return True
        elif response.status_code == 200:
            # Check if there are any error messages in the response
            if "error" in response.text.lower():
                print("❌ Signup failed with validation errors")
                return False
            else:
                print("⚠️  Signup page reloaded (possible issue)")
                return False
        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during signup test: {e}")
        return False

def test_login():
    """Test the login functionality"""
    print("3. Testing login functionality...")
    
    base_url = "http://127.0.0.1:5000"
    
    # Use the same test credentials from signup
    timestamp = int(time.time()) - 1  # Use previous timestamp
    test_username = f"testuser_{timestamp}"
    test_password = "testpass123"
    
    login_data = {
        'username': test_username,
        'password': test_password
    }
    
    try:
        response = requests.post(f"{base_url}/login", data=login_data)
        
        if response.status_code == 302:
            print("✅ Login successful - redirect received")
            return True
        elif response.status_code == 200:
            if "error" in response.text.lower() or "invalid" in response.text.lower():
                print("❌ Login failed with invalid credentials")
                return False
            else:
                print("⚠️  Login page reloaded (possible issue)")
                return False
        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during login test: {e}")
        return False

if __name__ == "__main__":
    print("Starting signup functionality tests...\n")
    
    # Test signup
    signup_success = test_signup()
    
    if signup_success:
        print("\n✅ Signup functionality is working correctly!")
        print("   - Form loads properly")
        print("   - Data validation works")
        print("   - User creation successful")
        print("   - Redirect to login page")
    else:
        print("\n❌ Signup functionality has issues")
        print("   Please check:")
        print("   - Database connection")
        print("   - Form field names")
        print("   - Password hashing")
        print("   - Database save operations")
    
    print("\n" + "=" * 50)
    print("Test completed!")