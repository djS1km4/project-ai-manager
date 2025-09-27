#!/usr/bin/env python3
"""
Comprehensive test script for Project CRUD operations
"""
import requests
import json

def get_auth_token():
    """Get authentication token"""
    login_url = "http://localhost:8001/api/v1/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    token_data = response.json()
    return token_data.get('access_token')

def test_project_crud():
    """Test all CRUD operations for projects"""
    print("🚀 Starting Project CRUD Tests")
    print("=" * 50)
    
    try:
        # Get authentication token
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Authentication successful")
        
        # 1. CREATE - Test project creation
        print("\n📝 Testing Project Creation...")
        project_url = "http://localhost:8001/api/v1/projects/"
        new_project = {
            "name": "CRUD Test Project",
            "description": "A project to test all CRUD operations",
            "start_date": "2025-09-25",
            "end_date": "2025-12-25",
            "budget": 5000,
            "status": "planning"
        }
        
        create_response = requests.post(project_url, json=new_project, headers=headers)
        if create_response.status_code in [200, 201]:
            created_project = create_response.json()
            project_id = created_project['id']
            print(f"✅ Project created successfully! ID: {project_id}")
            print(f"   Name: {created_project['name']}")
            print(f"   Status: {created_project['status']}")
        else:
            print(f"❌ Project creation failed: {create_response.status_code} - {create_response.text}")
            return
        
        # 2. READ - Test project listing
        print("\n📋 Testing Project Listing...")
        list_response = requests.get(project_url, headers=headers)
        if list_response.status_code == 200:
            projects = list_response.json()
            print(f"✅ Projects listed successfully! Found {len(projects)} projects")
            for project in projects:
                print(f"   - {project['name']} (ID: {project['id']}, Status: {project['status']})")
        else:
            print(f"❌ Project listing failed: {list_response.status_code} - {list_response.text}")
        
        # 3. READ - Test single project retrieval
        print(f"\n🔍 Testing Single Project Retrieval (ID: {project_id})...")
        get_response = requests.get(f"{project_url}{project_id}/", headers=headers)
        if get_response.status_code == 200:
            project = get_response.json()
            print(f"✅ Project retrieved successfully!")
            print(f"   Name: {project['name']}")
            print(f"   Description: {project['description']}")
            print(f"   Budget: ${project['budget']}")
            print(f"   Start Date: {project['start_date']}")
            print(f"   End Date: {project['end_date']}")
        else:
            print(f"❌ Project retrieval failed: {get_response.status_code} - {get_response.text}")
        
        # 4. UPDATE - Test project update
        print(f"\n✏️ Testing Project Update (ID: {project_id})...")
        update_data = {
            "name": "CRUD Test Project - Updated",
            "description": "Updated description for CRUD testing",
            "status": "active",
            "budget": 7500
        }
        
        update_response = requests.put(f"{project_url}{project_id}/", json=update_data, headers=headers)
        if update_response.status_code == 200:
            updated_project = update_response.json()
            print(f"✅ Project updated successfully!")
            print(f"   New Name: {updated_project['name']}")
            print(f"   New Status: {updated_project['status']}")
            print(f"   New Budget: ${updated_project['budget']}")
        else:
            print(f"❌ Project update failed: {update_response.status_code} - {update_response.text}")
        
        # 5. DELETE - Test project deletion
        print(f"\n🗑️ Testing Project Deletion (ID: {project_id})...")
        delete_response = requests.delete(f"{project_url}{project_id}/", headers=headers)
        if delete_response.status_code in [200, 204]:
            print(f"✅ Project deleted successfully!")
        else:
            print(f"❌ Project deletion failed: {delete_response.status_code} - {delete_response.text}")
        
        # 6. Verify deletion
        print(f"\n🔍 Verifying Project Deletion (ID: {project_id})...")
        verify_response = requests.get(f"{project_url}{project_id}/", headers=headers)
        if verify_response.status_code == 404:
            print(f"✅ Project deletion verified - project no longer exists")
        else:
            print(f"❌ Project deletion verification failed: {verify_response.status_code}")
        
        print("\n🎉 All CRUD operations completed!")
        
    except Exception as e:
        print(f"❌ Error during CRUD testing: {e}")

if __name__ == "__main__":
    test_project_crud()