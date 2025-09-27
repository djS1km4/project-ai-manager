#!/usr/bin/env python3
"""
Script to debug the specific validation error causing 422 responses
"""
import requests
import json

def test_project_creation_validation():
    """Test project creation with various data to identify validation issues"""
    # Login first
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("🔐 Logging in...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Test different project creation scenarios
    test_cases = [
        {
            "name": "Test Case 1: Basic project",
            "data": {
                "name": "Basic Test Project",
                "description": "A basic test project",
                "status": "planning"
            }
        },
        {
            "name": "Test Case 2: Project with budget",
            "data": {
                "name": "Budget Test Project",
                "description": "Project with budget",
                "status": "planning",
                "budget": 1000.50
            }
        },
        {
            "name": "Test Case 3: Project with dates",
            "data": {
                "name": "Date Test Project",
                "description": "Project with dates",
                "status": "planning",
                "start_date": "2025-01-25",
                "end_date": "2025-02-25"
            }
        },
        {
            "name": "Test Case 4: Full project data",
            "data": {
                "name": "Full Test Project",
                "description": "Complete project data",
                "status": "active",
                "priority": "high",
                "budget": 5000.75,
                "start_date": "2025-01-25",
                "end_date": "2025-03-25"
            }
        },
        {
            "name": "Test Case 5: Project with datetime format",
            "data": {
                "name": "DateTime Test Project",
                "description": "Project with datetime format",
                "status": "planning",
                "start_date": "2025-01-25T10:00:00",
                "end_date": "2025-02-25T18:00:00"
            }
        }
    ]
    
    projects_url = "http://localhost:8000/api/v1/projects/"
    
    for test_case in test_cases:
        print(f"\n🧪 {test_case['name']}")
        print(f"📤 Data: {json.dumps(test_case['data'], indent=2)}")
        
        response = requests.post(projects_url, json=test_case['data'], headers=headers)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ Success!")
            result = response.json()
            print(f"📥 Created project ID: {result.get('id')}")
        else:
            print("❌ Failed!")
            print(f"📥 Response: {response.text}")
            
            # Try to parse the error details
            try:
                error_data = response.json()
                print(f"📋 Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("📋 Could not parse error response as JSON")

def test_project_update_validation():
    """Test project update with various data to identify validation issues"""
    # Login first
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("\n🔐 Logging in for update tests...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    token = login_response.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get first project
    projects_response = requests.get("http://localhost:8000/api/v1/projects/", headers=headers)
    if projects_response.status_code != 200:
        print("❌ Could not get projects for update test")
        return
    
    projects = projects_response.json()
    if not projects:
        print("❌ No projects available for update test")
        return
    
    project_id = projects[0]["id"]
    print(f"📋 Testing updates on project ID: {project_id}")
    
    # Test different update scenarios
    update_test_cases = [
        {
            "name": "Update Test 1: Name only",
            "data": {
                "name": "Updated Project Name"
            }
        },
        {
            "name": "Update Test 2: Budget only",
            "data": {
                "budget": 2500.25
            }
        },
        {
            "name": "Update Test 3: Status and priority",
            "data": {
                "status": "active",
                "priority": "high"
            }
        },
        {
            "name": "Update Test 4: Dates",
            "data": {
                "start_date": "2025-01-26",
                "end_date": "2025-03-26"
            }
        }
    ]
    
    for test_case in update_test_cases:
        print(f"\n🧪 {test_case['name']}")
        print(f"📤 Data: {json.dumps(test_case['data'], indent=2)}")
        
        update_url = f"http://localhost:8000/api/v1/projects/{project_id}"
        response = requests.put(update_url, json=test_case['data'], headers=headers)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
        else:
            print("❌ Failed!")
            print(f"📥 Response: {response.text}")
            
            # Try to parse the error details
            try:
                error_data = response.json()
                print(f"📋 Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("📋 Could not parse error response as JSON")

if __name__ == "__main__":
    print("🚀 Starting validation error debugging...")
    test_project_creation_validation()
    test_project_update_validation()
    print("\n✅ Debugging complete!")