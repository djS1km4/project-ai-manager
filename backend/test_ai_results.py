#!/usr/bin/env python3

import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def test_ai_endpoints():
    # Login first
    login_data = {'email': 'admin@example.com', 'password': 'admin123'}
    login_response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
        
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    print('=== Testing AI Insight Endpoints ===')

    # Test each endpoint for multiple projects
    endpoints = [
        '/ai-insights/project/{}/analyze/risk',
        '/ai-insights/project/{}/analyze/progress', 
        '/ai-insights/project/{}/analyze/team'
    ]
    
    projects = [1, 2, 3]  # Test multiple projects

    for project_id in projects:
        print(f'\n=== PROJECT {project_id} ===')
        
        for endpoint_template in endpoints:
            endpoint = endpoint_template.format(project_id)
            endpoint_name = endpoint.split('/')[-1]
            
            print(f'\n--- Testing {endpoint_name} for project {project_id} ---')
            try:
                response = requests.post(f'{BASE_URL}{endpoint}', headers=headers)
                print(f'Status: {response.status_code}')
                
                if response.status_code == 200:
                    data = response.json()
                    print(f'Full Response: {json.dumps(data, indent=2)[:500]}...')
                    print(f'Title: {data.get("title", "N/A")}')
                    print(f'Description: {data.get("description", "N/A")[:100]}...')
                    print(f'Confidence: {data.get("confidence_score", "N/A")}')
                    
                    # Check for specific fields based on endpoint
                    if 'risk' in endpoint:
                        print(f'Risk Level: {data.get("risk_level", "N/A")}')
                        print(f'Risk Score: {data.get("overall_risk_score", "N/A")}')
                    elif 'progress' in endpoint:
                        print(f'Completion Date: {data.get("predicted_completion_date", "N/A")}')
                        print(f'Completion Probability: {data.get("completion_probability", "N/A")}')
                    elif 'team' in endpoint:
                        print(f'Team Velocity: {data.get("team_velocity", "N/A")}')
                        print(f'Productivity Score: {data.get("productivity_score", "N/A")}')
                        
                else:
                    print(f'Error: {response.text}')
                    
            except Exception as e:
                print(f'Exception: {e}')

if __name__ == "__main__":
    test_ai_endpoints()