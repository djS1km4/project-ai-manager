#!/usr/bin/env python3

import requests
import json

def test_ai_endpoints():
    """Test AI endpoints functionality"""
    
    # Login
    login_data = {'email': 'admin@example.com', 'password': 'admin123'}
    response = requests.post('http://localhost:8000/api/v1/auth/login', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return False
    
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test AI insights for project 39 (admin owned)
    project_id = 39
    print(f'🧪 Testing AI insights for project {project_id}...')
    
    # Test project analysis (comprehensive)
    print("\n1. Testing comprehensive project analysis...")
    response = requests.post(f'http://localhost:8000/api/v1/ai-insights/analyze-project/{project_id}', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        insights = data.get('insights', [])
        print(f'   ✅ Insights found: {len(insights)}')
        for insight in insights[:3]:  # Show first 3
            insight_type = insight.get('type', 'Unknown')
            insight_title = insight.get('title', 'No title')
            print(f'      - {insight_type}: {insight_title}')
    else:
        print(f'   ❌ Error: {response.text}')
    
    # Test risk analysis (GET endpoint)
    print("\n2. Testing risk assessment...")
    response = requests.get(f'http://localhost:8000/api/v1/ai-insights/project/{project_id}/risk-assessment', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        risk_score = data.get('risk_score', 'N/A')
        print(f'   ✅ Risk score: {risk_score}')
        print(f'   Risk factors: {len(data.get("risk_factors", []))}')
    else:
        print(f'   ❌ Error: {response.text}')
    
    # Test progress prediction (GET endpoint)
    print("\n3. Testing progress prediction...")
    response = requests.get(f'http://localhost:8000/api/v1/ai-insights/project/{project_id}/progress-prediction', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        completion_date = data.get('predicted_completion_date', 'N/A')
        confidence = data.get('confidence', 'N/A')
        print(f'   ✅ Predicted completion: {completion_date}')
        print(f'   Confidence: {confidence}')
    else:
        print(f'   ❌ Error: {response.text}')
    
    # Test team performance (GET endpoint)
    print("\n4. Testing team performance...")
    response = requests.get(f'http://localhost:8000/api/v1/ai-insights/project/{project_id}/team-performance', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        team_velocity = data.get('team_velocity', 'N/A')
        bottlenecks = data.get('bottlenecks', [])
        print(f'   ✅ Team velocity: {team_velocity}')
        print(f'   Bottlenecks: {len(bottlenecks)}')
    else:
        print(f'   ❌ Error: {response.text}')
    
    # Test specific risk analysis (POST endpoint)
    print("\n5. Testing specific risk analysis...")
    response = requests.post(f'http://localhost:8000/api/v1/ai-insights/project/{project_id}/analyze/risk', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        insights = data.get('insights', [])
        print(f'   ✅ Risk analysis completed: {len(insights)} insights')
    else:
        print(f'   ❌ Error: {response.text}')

if __name__ == "__main__":
    test_ai_endpoints()