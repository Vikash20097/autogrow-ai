#!/usr/bin/env python3
"""
Debug script to identify signup issues in AutoGrow-AI
"""

import requests
import time

def debug_signup():
    """Debug the signup functionality step by step"""
    print("🔍 Debugging AutoGrow-AI Signup Issues")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if signup page loads and what form fields it has
    print("1. Analyzing signup page...")
    try:
        response = requests.get(f"{base_url}/signup")
        if response.status_code == 200:
            print("✅ Signup page loads successfully")
            
            # Check for form fields
            if 'name="username"' in response.text:
                print("✅ Username field found")
            else:
                print("❌ Username field missing")
                
            if 'name="email"' in response.text:
                print("✅ Email field found")
            else:
                print("❌ Email field missing")
                
            if 'name="password"' in response.text:
                print("✅ Password field found")
            else:
                print("❌ Password field missing")
                
            if 'name="confirm_password"' in response.text:
                print("✅ Confirm password field found")
            else:
                print("❌ Confirm password field missing")
                
        else:
            print(f"❌ Signup page returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    
    # Test 2: Try signup with minimal data to see what error occurs
    print("\n2. Testing signup with minimal data...")
    
    timestamp = int(time.time())
    test_username = f"debuguser_{timestamp}"
    test_email = f"debuguser_{timestamp}@example.com"
    test_password = "debug123"
    
    signup_data = {
        'username': test_username,
        'email': test_email,
        'password': test_password,
        'confirm_password': test_password
    }
    
    try:
        response = requests.post(f"{base_url}/signup", data=signup_data, allow_redirects=False)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            print("✅ Signup successful - redirect to:", response.headers.get('Location', 'Unknown'))
            return True
        elif response.status_code == 200:
            print("⚠️  Signup page reloaded")
            # Check for error messages in the response
            if 'error' in response.text.lower():
                print("❌ Error messages found in response:")
                # Extract error messages
                import re
                error_pattern = r'flash.*?error.*?>(.*?)<'
                errors = re.findall(error_pattern, response.text, re.IGNORECASE | re.DOTALL)
                for error in errors:
                    print(f"   - {error.strip()}")
            else:
                print("No obvious error messages found")
            return False
        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during signup test: {e}")
        return False

if __name__ == "__main__":
    debug_signup()