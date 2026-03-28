#!/usr/bin/env python3
"""
Test script to verify dashboard displays data correctly
"""

import requests
import time

def test_dashboard_content():
    """Test dashboard content display"""
    print("Testing dashboard content...")
    
    try:
        response = requests.get('http://127.0.0.1:5000/dashboard')
        print(f"Dashboard response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for key elements that should be in the dashboard
            checks = [
                ('Total Posts', 'total_posts' in content or 'Total Posts:' in content),
                ('Pending Posts', 'pending_posts' in content or 'Pending Posts:' in content),
                ('Posted Posts', 'posted_posts' in content or 'Posted Posts:' in content),
                ('Post data', 'Test caption from direct test' in content),
                ('Post count', content.count('Post') > 0)
            ]
            
            print("\nDashboard content checks:")
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"  {status} {check_name}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("\n✅ Dashboard is displaying data correctly!")
            else:
                print("\n❌ Dashboard has display issues")
                print(f"\nContent preview:\n{content[:1000]}...")
                
        else:
            print("❌ Dashboard request failed")
            
    except Exception as e:
        print(f"❌ Error during dashboard test: {e}")

if __name__ == "__main__":
    print("Starting dashboard display test...")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    test_dashboard_content()
    
    print("\n" + "=" * 50)
    print("Test completed.")