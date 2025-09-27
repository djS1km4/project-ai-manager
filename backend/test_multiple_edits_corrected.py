#!/usr/bin/env python3
"""
Test script to verify that all project fields are correctly saved and persisted
through multiple consecutive edits.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
PROJECTS_URL = f"{BASE_URL}/projects"

def login():
    """Login and get access token"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("🔐 Logging in...")
    response = requests.post(LOGIN_URL, json=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def get_headers(token):
    """Get authorization headers"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_project_data(token, project_id):
    """Get project data"""
    headers = get_headers(token)
    response = requests.get(f"{PROJECTS_URL}/{project_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get project {project_id}: {response.status_code} - {response.text}")
        return None

def update_project(token, project_id, update_data):
    """Update project with given data"""
    headers = get_headers(token)
    response = requests.put(f"{PROJECTS_URL}/{project_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to update project {project_id}: {response.status_code} - {response.text}")
        print(f"Update data: {json.dumps(update_data, indent=2)}")
        return None

def verify_field_value(project_data, field_name, expected_value, test_name):
    """Verify that a field has the expected value"""
    actual_value = project_data.get(field_name)
    
    # Special handling for date fields - API returns datetime format
    if field_name in ['start_date', 'end_date'] and actual_value and expected_value:
        # Extract just the date part from datetime string
        actual_date = actual_value.split('T')[0] if 'T' in str(actual_value) else str(actual_value)
        expected_date = str(expected_value)
        
        if actual_date == expected_date:
            print(f"✅ {test_name}: {field_name} = {actual_date}")
            return True
        else:
            print(f"❌ {test_name}: {field_name} expected {expected_date}, got {actual_date}")
            return False
    
    # Regular comparison for other fields
    if actual_value == expected_value:
        print(f"✅ {test_name}: {field_name} = {actual_value}")
        return True
    else:
        print(f"❌ {test_name}: {field_name} expected {expected_value}, got {actual_value}")
        return False

def test_multiple_consecutive_edits():
    """Test multiple consecutive edits on all project fields"""
    print("🧪 Testing multiple consecutive edits on all project fields...")
    
    # Login
    token = login()
    if not token:
        return False
    
    # Get first available project
    headers = get_headers(token)
    projects_response = requests.get(PROJECTS_URL, headers=headers)
    
    if projects_response.status_code != 200:
        print(f"❌ Failed to get projects: {projects_response.status_code}")
        return False
    
    projects = projects_response.json()
    if not projects:
        print("❌ No projects found")
        return False
    
    project_id = projects[0]["id"]
    print(f"📋 Using project ID: {project_id}")
    
    # Get original project data
    original_data = get_project_data(token, project_id)
    if not original_data:
        return False
    
    print(f"📊 Original project data: {json.dumps(original_data, indent=2)}")
    
    # Test 1: Update name and description
    print("\n🔄 Test 1: Updating name and description...")
    update_1 = {
        "name": "Test Project Updated 1",
        "description": "Updated description for test 1"
    }
    
    updated_project_1 = update_project(token, project_id, update_1)
    if not updated_project_1:
        return False
    
    # Verify Test 1
    success_1 = True
    success_1 &= verify_field_value(updated_project_1, "name", update_1["name"], "Test 1")
    success_1 &= verify_field_value(updated_project_1, "description", update_1["description"], "Test 1")
    
    # Test 2: Update budget and dates
    print("\n🔄 Test 2: Updating budget and dates...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    update_2 = {
        "budget": 15000.50,
        "start_date": tomorrow,
        "end_date": next_month
    }
    
    updated_project_2 = update_project(token, project_id, update_2)
    if not updated_project_2:
        return False
    
    # Verify Test 2
    success_2 = True
    success_2 &= verify_field_value(updated_project_2, "budget", update_2["budget"], "Test 2")
    success_2 &= verify_field_value(updated_project_2, "start_date", update_2["start_date"], "Test 2")
    success_2 &= verify_field_value(updated_project_2, "end_date", update_2["end_date"], "Test 2")
    
    # Test 3: Update status and priority
    print("\n🔄 Test 3: Updating status and priority...")
    update_3 = {
        "status": "active",
        "priority": "high"
    }
    
    updated_project_3 = update_project(token, project_id, update_3)
    if not updated_project_3:
        return False
    
    # Verify Test 3
    success_3 = True
    success_3 &= verify_field_value(updated_project_3, "status", update_3["status"], "Test 3")
    success_3 &= verify_field_value(updated_project_3, "priority", update_3["priority"], "Test 3")
    
    # Test 4: Update all fields at once
    print("\n🔄 Test 4: Updating all fields at once...")
    update_4 = {
        "name": "Final Test Project",
        "description": "Final comprehensive test description",
        "budget": 25000.75,
        "start_date": tomorrow,
        "end_date": next_month,
        "status": "completed",
        "priority": "medium"
    }
    
    updated_project_4 = update_project(token, project_id, update_4)
    if not updated_project_4:
        return False
    
    # Verify Test 4
    success_4 = True
    for field, expected_value in update_4.items():
        success_4 &= verify_field_value(updated_project_4, field, expected_value, "Test 4")
    
    # Test 5: Verify persistence by fetching fresh data
    print("\n🔄 Test 5: Verifying persistence with fresh fetch...")
    fresh_data = get_project_data(token, project_id)
    if not fresh_data:
        return False
    
    success_5 = True
    for field, expected_value in update_4.items():
        success_5 &= verify_field_value(fresh_data, field, expected_value, "Test 5 (Fresh fetch)")
    
    # Restore original data
    print("\n🔄 Restoring original project data...")
    restore_data = {
        "name": original_data["name"],
        "description": original_data["description"],
        "budget": original_data["budget"],
        "start_date": original_data["start_date"],
        "end_date": original_data["end_date"],
        "status": original_data["status"],
        "priority": original_data["priority"]
    }
    
    restored_project = update_project(token, project_id, restore_data)
    if restored_project:
        print("✅ Original data restored successfully")
    else:
        print("❌ Failed to restore original data")
    
    # Final results
    all_tests_passed = success_1 and success_2 and success_3 and success_4 and success_5
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Test 1 (Name & Description): {'✅ PASS' if success_1 else '❌ FAIL'}")
    print(f"   Test 2 (Budget & Dates): {'✅ PASS' if success_2 else '❌ FAIL'}")
    print(f"   Test 3 (Status & Priority): {'✅ PASS' if success_3 else '❌ FAIL'}")
    print(f"   Test 4 (All Fields): {'✅ PASS' if success_4 else '❌ FAIL'}")
    print(f"   Test 5 (Persistence): {'✅ PASS' if success_5 else '❌ FAIL'}")
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")
    
    return all_tests_passed

if __name__ == "__main__":
    test_multiple_consecutive_edits()