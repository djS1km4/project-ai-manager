#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
DASHBOARD_URL = f"{BASE_URL}/api/v1/dashboard/stats"

def test_dashboard_stats():
    """Test dashboard stats endpoint"""
    
    # Login as admin
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    print("🔐 Logging in as admin...")
    login_response = requests.post(LOGIN_URL, json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    # Get token
    token_data = login_response.json()
    token = token_data.get("access_token")
    
    if not token:
        print("❌ No access token received")
        return
    
    print("✅ Login successful")
    
    # Test dashboard stats
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📊 Testing dashboard stats...")
    stats_response = requests.get(DASHBOARD_URL, headers=headers)
    
    print(f"Status Code: {stats_response.status_code}")
    
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        print("✅ Dashboard stats retrieved successfully!")
        print("\n📈 Dashboard Statistics:")
        print(f"  Total Projects: {stats_data.get('totalProjects', 0)}")
        print(f"  Active Projects: {stats_data.get('activeProjects', 0)}")
        print(f"  Completed Projects: {stats_data.get('completedProjects', 0)}")
        print(f"  Planning Projects: {stats_data.get('planningProjects', 0)}")
        print(f"  On Hold Projects: {stats_data.get('onHoldProjects', 0)}")
        print(f"  Total Tasks: {stats_data.get('totalTasks', 0)}")
        print(f"  Completed Tasks: {stats_data.get('completedTasks', 0)}")
        print(f"  Pending Tasks: {stats_data.get('pendingTasks', 0)}")
        print(f"  Overdue Tasks: {stats_data.get('overdueTasks', 0)}")
        print(f"  Total Budget: ${stats_data.get('totalBudget', 0):,.2f}")
        print(f"  Used Budget: ${stats_data.get('usedBudget', 0):,.2f}")
        
        print(f"\n📋 Full Response:")
        print(json.dumps(stats_data, indent=2))
    else:
        print(f"❌ Failed to get dashboard stats: {stats_response.status_code}")
        print(f"Response: {stats_response.text}")

if __name__ == "__main__":
    test_dashboard_stats()