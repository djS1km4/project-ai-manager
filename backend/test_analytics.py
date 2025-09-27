import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def get_access_token():
    """Get access token for authentication"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_project_analytics(project_id=1):
    """Test project analytics endpoint"""
    token = get_access_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test project analytics endpoint
    print(f"\n=== Testing Project Analytics for Project {project_id} ===")
    response = requests.get(
        f"{BASE_URL}/ai-insights/project/{project_id}/analytics",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        analytics = response.json()
        print("Analytics data:")
        print(json.dumps(analytics, indent=2, default=str))
    else:
        print(f"Error: {response.text}")

def test_project_analytics_from_projects_endpoint(project_id=1):
    """Test project analytics from projects endpoint"""
    token = get_access_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test project analytics from projects endpoint
    print(f"\n=== Testing Project Analytics from Projects Endpoint for Project {project_id} ===")
    response = requests.get(
        f"{BASE_URL}/projects/{project_id}/analytics",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        analytics = response.json()
        print("Analytics data:")
        print(json.dumps(analytics, indent=2, default=str))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_project_analytics()
    test_project_analytics_from_projects_endpoint()