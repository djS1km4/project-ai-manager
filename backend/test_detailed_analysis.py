#!/usr/bin/env python3
"""
Detailed test script to examine the content of specific analysis responses
"""
import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def login():
    """Login and get access token"""
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None
    
    token_data = response.json()
    return token_data["access_token"]

def get_projects(token):
    """Get list of projects"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to get projects: {response.status_code}")
        return []
    
    return response.json()

def test_detailed_analysis(token, project_id, analysis_type, endpoint_suffix):
    """Test a specific analysis endpoint and show detailed results"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/ai-insights/project/{project_id}/analyze/{endpoint_suffix}"
    
    print(f"\n{'='*60}")
    print(f"🔍 DETAILED {analysis_type.upper()} ANALYSIS")
    print(f"{'='*60}")
    print(f"URL: {url}")
    
    response = requests.post(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ {analysis_type} analysis failed: {response.status_code}")
        print(response.text)
        return None
    
    result = response.json()
    print(f"✅ {analysis_type} analysis successful!")
    
    # Print the complete response in a formatted way
    print(f"\n📋 COMPLETE RESPONSE:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def main():
    print("🚀 Detailed Testing of Specific AI Analysis Endpoints")
    print("=" * 70)
    
    # Login
    print("🔐 Logging in...")
    token = login()
    if not token:
        sys.exit(1)
    print("✅ Login successful!")
    
    # Get projects
    print("\n📋 Getting projects...")
    projects = get_projects(token)
    if not projects:
        print("❌ No projects found!")
        sys.exit(1)
    
    print(f"✅ Found {len(projects)} projects")
    
    # Use the first project for testing
    project = projects[0]
    project_id = project["id"]
    project_name = project["name"]
    
    print(f"🎯 Testing with project: {project_name} (ID: {project_id})")
    
    # Test all three specific analysis endpoints with detailed output
    analysis_tests = [
        ("Risk", "risk"),
        ("Progress", "progress"), 
        ("Team", "team")
    ]
    
    results = {}
    
    for analysis_type, endpoint_suffix in analysis_tests:
        result = test_detailed_analysis(token, project_id, analysis_type, endpoint_suffix)
        if result:
            results[analysis_type] = result
    
    # Final comparison
    print(f"\n{'='*70}")
    print("🔍 COMPARISON OF KEY FIELDS")
    print("=" * 70)
    
    for analysis_type in ["Risk", "Progress", "Team"]:
        if analysis_type in results:
            result = results[analysis_type]
            print(f"\n{analysis_type} Analysis:")
            print(f"  - Analysis Type: {result.get('analysis_type', 'N/A')}")
            print(f"  - Confidence: {result.get('confidence', 'N/A')}")
            print(f"  - Summary (first 100 chars): {result.get('summary', 'N/A')[:100]}...")
            
            # Type-specific fields
            if analysis_type == "Risk":
                print(f"  - Risk Score: {result.get('risk_score', 'N/A')}")
                print(f"  - Risk Factors Count: {len(result.get('risk_factors', []))}")
            elif analysis_type == "Progress":
                print(f"  - Predicted Completion: {result.get('predicted_completion', 'N/A')}")
                print(f"  - Days Remaining: {result.get('days_remaining', 'N/A')}")
            elif analysis_type == "Team":
                print(f"  - Team Velocity: {result.get('team_velocity', 'N/A')}")
                print(f"  - Individual Performance Count: {len(result.get('individual_performance', []))}")

if __name__ == "__main__":
    main()