#!/usr/bin/env python3
"""
Script to list all projects and verify project creation
"""
import requests
import json

def list_all_projects():
    """List all projects to verify creation"""
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
        print(f"Login successful!")
        
        # List projects
        headers = {"Authorization": f"Bearer {token}"}
        projects_url = "http://localhost:8001/api/v1/projects/"
        
        projects_response = requests.get(projects_url, headers=headers)
        print(f"Projects list status: {projects_response.status_code}")
        
        if projects_response.status_code == 200:
            projects = projects_response.json()
            print(f"\n📋 Found {len(projects)} projects:")
            print("=" * 50)
            
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.get('name')}")
                print(f"   ID: {project.get('id')}")
                print(f"   Status: {project.get('status')}")
                print(f"   Description: {project.get('description')}")
                print(f"   Start Date: {project.get('start_date')}")
                print(f"   End Date: {project.get('end_date')}")
                print(f"   Budget: ${project.get('budget')}")
                print(f"   Created: {project.get('created_at')}")
                print("-" * 30)
                
        else:
            print(f"Failed to list projects: {projects_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_all_projects()