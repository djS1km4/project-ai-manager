#!/usr/bin/env python3
"""
Test script to verify project progress calculation
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
PROJECTS_URL = f"{BASE_URL}/projects/"

def test_projects_progress():
    """Test projects endpoint to verify progress calculation"""
    
    print("🔐 Logging in as admin...")
    
    # Login as admin
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    login_response = requests.post(LOGIN_URL, json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    print("✅ Login successful")
    
    # Get access token
    token_data = login_response.json()
    access_token = token_data["access_token"]
    
    # Test projects endpoint
    print(f"\n📊 Testing projects endpoint...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    projects_response = requests.get(PROJECTS_URL, headers=headers)
    
    if projects_response.status_code == 200:
        print(f"Status Code: {projects_response.status_code}")
        print("✅ Projects retrieved successfully!")
        
        projects_data = projects_response.json()
        
        print(f"\n📈 Projects with Progress:")
        for project in projects_data:
            print(f"  - {project.get('name', 'Unknown')}")
            print(f"    Status: {project.get('status', 'Unknown')}")
            print(f"    Task Count: {project.get('task_count', 0)}")
            print(f"    Completed Tasks: {project.get('completed_tasks', 0)}")
            print(f"    Progress: {project.get('progress_percentage', 0):.1f}%")
            print()
        
        print(f"📋 Full Response:")
        print(json.dumps(projects_data, indent=2))
    else:
        print(f"❌ Failed to get projects: {projects_response.status_code}")
        print(f"Response: {projects_response.text}")

if __name__ == "__main__":
    test_projects_progress()