#!/usr/bin/env python3
"""
Test script to verify that specific analysis endpoints generate distinct and relevant results
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

def test_analysis_endpoint(token, project_id, analysis_type, endpoint_suffix):
    """Test a specific analysis endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/ai-insights/project/{project_id}/analyze/{endpoint_suffix}"
    
    print(f"\n🔍 Testing {analysis_type} analysis...")
    print(f"URL: {url}")
    
    response = requests.post(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ {analysis_type} analysis failed: {response.status_code}")
        print(response.text)
        return None
    
    result = response.json()
    print(f"✅ {analysis_type} analysis successful!")
    
    # Print key information about the result
    if "analysis_type" in result:
        print(f"   Analysis Type: {result['analysis_type']}")
    
    if "summary" in result:
        print(f"   Summary: {result['summary'][:100]}...")
    
    if "confidence" in result:
        print(f"   Confidence: {result['confidence']}%")
    
    # Print specific fields based on analysis type
    if analysis_type == "Risk":
        if "risk_score" in result:
            print(f"   Risk Score: {result['risk_score']}")
        if "risk_factors" in result:
            print(f"   Risk Factors: {len(result['risk_factors'])} found")
    
    elif analysis_type == "Progress":
        if "predicted_completion" in result:
            print(f"   Predicted Completion: {result['predicted_completion']}")
        if "days_remaining" in result:
            print(f"   Days Remaining: {result['days_remaining']}")
    
    elif analysis_type == "Team":
        if "team_velocity" in result:
            print(f"   Team Velocity: {result['team_velocity']}")
        if "individual_performance" in result:
            print(f"   Team Members Analyzed: {len(result['individual_performance'])}")
    
    return result

def main():
    print("🚀 Testing Specific AI Analysis Endpoints")
    print("=" * 50)
    
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
    
    # Test all three specific analysis endpoints
    analysis_tests = [
        ("Risk", "risk"),
        ("Progress", "progress"), 
        ("Team", "team")
    ]
    
    results = {}
    
    for analysis_type, endpoint_suffix in analysis_tests:
        result = test_analysis_endpoint(token, project_id, analysis_type, endpoint_suffix)
        if result:
            results[analysis_type] = result
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY OF RESULTS")
    print("=" * 50)
    
    for analysis_type in ["Risk", "Progress", "Team"]:
        if analysis_type in results:
            result = results[analysis_type]
            print(f"\n✅ {analysis_type} Analysis:")
            print(f"   Type: {result.get('analysis_type', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}%")
            
            # Check for type-specific fields
            if analysis_type == "Risk" and "risk_score" in result:
                print(f"   Risk Score: {result['risk_score']}")
            elif analysis_type == "Progress" and "predicted_completion" in result:
                print(f"   Completion Date: {result['predicted_completion']}")
            elif analysis_type == "Team" and "team_velocity" in result:
                print(f"   Team Velocity: {result['team_velocity']}")
        else:
            print(f"\n❌ {analysis_type} Analysis: FAILED")
    
    # Verify that results are different
    print(f"\n🔍 VERIFICATION:")
    if len(results) == 3:
        # Check if analysis types are different
        types = [results[key].get("analysis_type") for key in results]
        if len(set(types)) == 3:
            print("✅ All three analysis types return different analysis_type values")
        else:
            print("⚠️  Some analysis types return the same analysis_type value")
        
        # Check if summaries are different
        summaries = [results[key].get("summary", "")[:50] for key in results]
        if len(set(summaries)) == 3:
            print("✅ All three analysis types return different summaries")
        else:
            print("⚠️  Some analysis types return similar summaries")
    else:
        print(f"❌ Only {len(results)}/3 analysis endpoints worked correctly")

if __name__ == "__main__":
    main()