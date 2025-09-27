#!/usr/bin/env python3
"""
Script to test project creation with authentication
"""
import requests
import json

def test_create_project():
    """Test project creation with authentication"""
    # First login to get token
    login_url = "http://localhost:8001/api/v1/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Login
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data.get('access_token')
        print(f"Login successful! Token: {token[:50]}...")
        
        # Test project creation
        headers = {"Authorization": f"Bearer {token}"}
        project_url = "http://localhost:8001/api/v1/projects/"
        
        project_data = {
            "name": "Test Project",
            "description": "A test project created via API",
            "start_date": "2025-09-25",
            "due_date": "2025-10-25",
            "budget": 1000.0,
            "status": "planning"
        }
        
        project_response = requests.post(project_url, json=project_data, headers=headers)
        print(f"Project creation status: {project_response.status_code}")
        print(f"Project creation response: {project_response.text}")
        
        if project_response.status_code in [200, 201]:
            print("✅ Project created successfully!")
            project = project_response.json()
            print(f"Project ID: {project.get('id')}")
            print(f"Project Name: {project.get('name')}")
            print(f"Project Status: {project.get('status')}")
        else:
            print("❌ Project creation failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_create_project()