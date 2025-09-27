#!/usr/bin/env python3
"""
Test script to verify data variability in AI analysis methods
"""
import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def login():
    """Login and get access token"""
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_direct_endpoints(token):
    """Test the direct GET endpoints that return the actual analysis objects"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("=== TESTING DIRECT ENDPOINTS (GET) ===\n")
    
    # Test projects 1, 2, 3
    for project_id in [1, 2, 3]:
        print(f"--- PROJECT {project_id} ---")
        
        # Test risk assessment
        print(f"Risk Assessment for Project {project_id}:")
        response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/risk-assessment", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"  Risk Score: {data.get('overall_risk_score', 'N/A')}")
            print(f"  Risk Factors: {len(data.get('risk_factors', []))}")
            print(f"  Critical Issues: {len(data.get('critical_issues', []))}")
            print(f"  Recommendations: {len(data.get('recommendations', []))}")
        else:
            print(f"  Error: {response.status_code}")
        
        # Test progress prediction
        print(f"Progress Prediction for Project {project_id}:")
        response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/progress-prediction", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"  Completion Date: {data.get('predicted_completion_date', 'N/A')}")
            print(f"  Confidence: {data.get('confidence_level', 'N/A')}")
            print(f"  Completion Probability: {data.get('completion_probability', 'N/A')}")
            print(f"  Factors: {len(data.get('factors_affecting_timeline', []))}")
        else:
            print(f"  Error: {response.status_code}")
        
        # Test team performance
        print(f"Team Performance for Project {project_id}:")
        response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/team-performance", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"  Team Velocity: {data.get('team_velocity', 'N/A')}")
            print(f"  Efficiency Score: {data.get('team_efficiency_score', 'N/A')}")
            print(f"  Bottlenecks: {len(data.get('bottlenecks', []))}")
            print(f"  Individual Performance: {len(data.get('individual_performance', []))}")
        else:
            print(f"  Error: {response.status_code}")
        
        print()

def test_analyze_endpoints(token):
    """Test the POST /analyze endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("=== TESTING ANALYZE ENDPOINTS (POST) ===\n")
    
    # Test projects 1, 2, 3
    for project_id in [1, 2, 3]:
        print(f"--- PROJECT {project_id} ---")
        
        # Test risk analysis
        print(f"Risk Analysis for Project {project_id}:")
        response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/analyze/risk", headers=headers)
        if response.status_code == 200:
            data = response.json()
            insights = data.get('insights', [])
            if insights:
                insight = insights[0]
                analysis_data = insight.get('analysis_data', {})
                print(f"  Risk Score: {analysis_data.get('overall_risk_score', 'N/A')}")
                print(f"  Risk Factors: {len(analysis_data.get('risk_factors', []))}")
                print(f"  Critical Issues: {len(analysis_data.get('critical_issues', []))}")
                print(f"  Title: {insight.get('title', 'N/A')}")
        else:
            print(f"  Error: {response.status_code}")
        
        # Test progress analysis
        print(f"Progress Analysis for Project {project_id}:")
        response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/analyze/progress", headers=headers)
        if response.status_code == 200:
            data = response.json()
            insights = data.get('insights', [])
            if insights:
                insight = insights[0]
                analysis_data = insight.get('analysis_data', {})
                print(f"  Completion Date: {analysis_data.get('predicted_completion_date', 'N/A')}")
                print(f"  Confidence: {analysis_data.get('confidence_level', 'N/A')}")
                print(f"  Factors: {len(analysis_data.get('factors_affecting_timeline', []))}")
                print(f"  Title: {insight.get('title', 'N/A')}")
        else:
            print(f"  Error: {response.status_code}")
        
        # Test team analysis
        print(f"Team Analysis for Project {project_id}:")
        response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/analyze/team", headers=headers)
        if response.status_code == 200:
            data = response.json()
            insights = data.get('insights', [])
            if insights:
                insight = insights[0]
                analysis_data = insight.get('analysis_data', {})
                print(f"  Team Velocity: {analysis_data.get('team_velocity', 'N/A')}")
                print(f"  Efficiency Score: {analysis_data.get('team_efficiency_score', 'N/A')}")
                print(f"  Bottlenecks: {len(analysis_data.get('bottlenecks', []))}")
                print(f"  Title: {insight.get('title', 'N/A')}")
        else:
            print(f"  Error: {response.status_code}")
        
        print()

def main():
    print("Testing AI Analysis Data Variability")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("Failed to login")
        sys.exit(1)
    
    print(f"Login successful at {datetime.now()}\n")
    
    # Test direct endpoints
    test_direct_endpoints(token)
    
    # Test analyze endpoints
    test_analyze_endpoints(token)
    
    print("Testing completed!")

if __name__ == "__main__":
    main()