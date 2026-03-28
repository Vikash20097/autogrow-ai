#!/usr/bin/env python3
"""
Test script to verify the AutoGrow-AI application functionality
"""

import requests
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_application():
    """Test the Flask application functionality"""
    print("🧪 Testing AutoGrow-AI Application")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://127.0.0.1:5000/login', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:5000")
        return False
    
    # Test 2: Check if signup page loads
    try:
        response = requests.get('http://127.0.0.1:5000/signup', timeout=5)
        if response.status_code == 200 and 'Create Account' in response.text:
            print("✅ Signup page loads correctly")
        else:
            print("❌ Signup page not loading properly")
            return False
    except:
        print("❌ Cannot access signup page")
        return False
    
    # Test 3: Check if dashboard redirects properly for unauthenticated users
    try:
        response = requests.get('http://127.0.0.1:5000/dashboard', allow_redirects=False)
        if response.status_code == 302:
            print("✅ Dashboard properly redirects unauthenticated users")
        else:
            print("❌ Dashboard not redirecting properly")
            return False
    except:
        print("❌ Cannot test dashboard redirect")
        return False
    
    print("\n🎉 All basic tests passed!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Try signing up with a new account")
    print("3. Log in with the created account")
    print("4. Verify you're redirected to the dashboard")
    print("5. Test the logout functionality")
    
    return True

if __name__ == "__main__":
    test_application()