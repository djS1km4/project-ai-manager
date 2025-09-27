#!/usr/bin/env python3
"""
Script to test login endpoint
"""
import requests
import json

def test_login():
    """Test login with existing user"""
    url = "http://localhost:8001/api/v1/auth/login"
    
    # Test with the existing user
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(url, json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"Login successful! Token: {token[:50]}...")
            
            # Test authenticated request
            headers = {"Authorization": f"Bearer {token}"}
            projects_response = requests.get("http://localhost:8001/api/v1/projects/", headers=headers)
            print(f"Projects request status: {projects_response.status_code}")
            print(f"Projects response: {projects_response.text}")
            
        else:
            print("Login failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()