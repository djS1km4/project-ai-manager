#!/usr/bin/env python3
"""
Script to test project creation with frontend field structure
"""
import requests
import json

def test_frontend_project_creation():
    """Test project creation with frontend field structure"""
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
        
        # Test project creation with frontend structure
        headers = {"Authorization": f"Bearer {token}"}
        project_url = "http://localhost:8001/api/v1/projects/"
        
        # This mimics the exact structure sent by the frontend
        project_data = {
            "name": "Frontend Test Project",
            "description": "A test project with frontend field structure",
            "start_date": "2025-09-25",
            "end_date": "2025-10-25",  # Using end_date instead of due_date
            "budget": 1500,
            "status": "planning"
        }
        
        print(f"Sending project data: {json.dumps(project_data, indent=2)}")
        
        project_response = requests.post(project_url, json=project_data, headers=headers)
        print(f"Project creation status: {project_response.status_code}")
        print(f"Project creation response: {project_response.text}")
        
        if project_response.status_code in [200, 201]:
            print("✅ Project created successfully with frontend field structure!")
            project = project_response.json()
            print(f"Project ID: {project.get('id')}")
            print(f"Project Name: {project.get('name')}")
            print(f"Project Status: {project.get('status')}")
            print(f"Start Date: {project.get('start_date')}")
            print(f"End Date: {project.get('end_date')}")
        else:
            print("❌ Project creation failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_frontend_project_creation()