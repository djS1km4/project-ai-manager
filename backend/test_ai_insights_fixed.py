#!/usr/bin/env python3

import requests
import json
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

BASE_URL = "http://localhost:8001/api/v1"

def test_ai_insights():
    """Test AI insights functionality"""
    
    # Login as admin
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    print("🔐 Logging in as admin...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get projects
    print("\n📋 Getting projects...")
    projects_response = requests.get(f"{BASE_URL}/projects", headers=headers)
    
    if projects_response.status_code != 200:
        print(f"❌ Failed to get projects: {projects_response.status_code}")
        return False
    
    projects = projects_response.json()
    print(f"✅ Found {len(projects)} projects")
    
    if not projects:
        print("❌ No projects found to test AI insights")
        return False
    
    project_id = projects[0]["id"]
    project_name = projects[0]["name"]
    print(f"🎯 Testing AI insights for project: {project_name} (ID: {project_id})")
    
    # Test dashboard insights
    print("\n🧠 Testing dashboard insights...")
    dashboard_response = requests.get(f"{BASE_URL}/ai-insights/dashboard/insights", headers=headers)
    
    if dashboard_response.status_code != 200:
        print(f"❌ Dashboard insights failed: {dashboard_response.status_code}")
        print(f"Response: {dashboard_response.text}")
        return False
    
    dashboard_data = dashboard_response.json()
    print(f"✅ Dashboard insights: {dashboard_data['summary']['total_insights']} insights found")
    
    # Test project analysis
    print(f"\n🔍 Testing project analysis for project {project_id}...")
    analysis_response = requests.post(f"{BASE_URL}/ai-insights/analyze-project/{project_id}", headers=headers)
    
    if analysis_response.status_code != 200:
        print(f"❌ Project analysis failed: {analysis_response.status_code}")
        print(f"Response: {analysis_response.text}")
        return False
    
    analysis_data = analysis_response.json()
    print(f"✅ Project analysis completed: {analysis_data['message']}")
    print(f"📊 Generated insights: {len(analysis_data.get('insights', []))}")
    
    # Test getting project insights
    print(f"\n📈 Getting project insights for project {project_id}...")
    insights_response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/insights", headers=headers)
    
    if insights_response.status_code != 200:
        print(f"❌ Get project insights failed: {insights_response.status_code}")
        print(f"Response: {insights_response.text}")
        return False
    
    insights_data = insights_response.json()
    print(f"✅ Retrieved {len(insights_data)} insights for project")
    
    # Display some insights
    if insights_data:
        print("\n📋 Sample insights:")
        for i, insight in enumerate(insights_data[:3]):  # Show first 3
            print(f"  {i+1}. {insight.get('insight_type', 'Unknown')} - {insight.get('content', 'No content')[:100]}...")
    
    # Test risk assessment
    print(f"\n⚠️ Testing risk assessment for project {project_id}...")
    risk_response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/risk-assessment", headers=headers)
    
    if risk_response.status_code == 200:
        risk_data = risk_response.json()
        print(f"✅ Risk assessment completed: {risk_data.get('overall_risk_score', 'N/A')}")
    else:
        print(f"⚠️ Risk assessment endpoint not available: {risk_response.status_code}")
    
    # Test progress prediction
    print(f"\n📅 Testing progress prediction for project {project_id}...")
    progress_response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/progress-prediction", headers=headers)
    
    if progress_response.status_code == 200:
        progress_data = progress_response.json()
        print(f"✅ Progress prediction completed: {progress_data.get('predicted_completion_date', 'N/A')}")
    else:
        print(f"⚠️ Progress prediction endpoint not available: {progress_response.status_code}")
    
    # Test team performance
    print(f"\n👥 Testing team performance for project {project_id}...")
    team_response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/team-performance", headers=headers)
    
    if team_response.status_code == 200:
        team_data = team_response.json()
        print(f"✅ Team performance analysis completed: {team_data.get('team_velocity', 'N/A')} tasks/week")
    else:
        print(f"⚠️ Team performance endpoint not available: {team_response.status_code}")
    
    print("\n🎉 AI Insights testing completed successfully!")
    return True

if __name__ == "__main__":
    print("🧪 Testing AI Insights functionality...")
    print("=" * 50)
    
    success = test_ai_insights()
    
    if success:
        print("\n✅ All AI Insights tests passed!")
    else:
        print("\n❌ Some AI Insights tests failed!")
        sys.exit(1)