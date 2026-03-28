#!/usr/bin/env python3
"""
Test script to verify form submission and database functionality
"""

import requests
import time

def test_form_submission():
    """Test the create-post form submission"""
    print("Testing form submission...")
    
    # Test data
    test_data = {
        'caption': 'Test post from script',
        'scheduled_time': '2026-03-28T15:00'
    }
    
    try:
        # Submit form
        response = requests.post('http://127.0.0.1:5000/create-post', data=test_data)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 302:  # Redirect to dashboard
            print("✅ Form submission successful - redirect to dashboard")
        else:
            print("❌ Form submission failed")
            
    except Exception as e:
        print(f"❌ Error during form submission: {e}")

def test_dashboard():
    """Test dashboard data display"""
    print("\nTesting dashboard...")
    
    try:
        response = requests.get('http://127.0.0.1:5000/dashboard')
        print(f"Dashboard response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if 'Total Posts:' in content:
                print("✅ Dashboard showing post count")
            else:
                print("❌ Dashboard not showing expected content")
        else:
            print("❌ Dashboard request failed")
            
    except Exception as e:
        print(f"❌ Error during dashboard test: {e}")

if __name__ == "__main__":
    print("Starting form submission tests...")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    test_form_submission()
    test_dashboard()
    
    print("\n" + "=" * 50)
    print("Test completed. Check terminal output for results.")