#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "testpassword123"

def get_access_token():
    """Get access token"""
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def create_ai_insight(token, project_id):
    """Create an AI insight"""
    headers = {"Authorization": f"Bearer {token}"}
    
    insight_data = {
        "project_id": project_id,
        "insight_type": "risk_analysis",
        "priority": "high",
        "title": "Análisis de Riesgo del Proyecto",
        "description": "Evaluación de riesgos potenciales basada en el progreso actual",
        "recommendations": "Revisar cronograma y asignar recursos adicionales",
        "confidence_score": 0.85
    }
    
    response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/insights", 
                           json=insight_data, headers=headers)
    
    print(f"Create insight response: {response.status_code}")
    if response.status_code == 200:
        print("Insight created successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def get_project_insights(token, project_id):
    """Get insights for a project"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/ai-insights/project/{project_id}/insights", 
                          headers=headers)
    
    print(f"\nGet insights response: {response.status_code}")
    if response.status_code == 200:
        insights = response.json()
        print(f"Found {len(insights)} insights:")
        for insight in insights:
            print(f"- {insight['title']} ({insight['insight_type']}) - {insight['priority']}")
    else:
        print(f"Error: {response.text}")
    
    return response

def test_ai_insights_generation(token, project_id):
    """Test AI insights generation endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/generate", 
                           headers=headers)
    
    print(f"\nGenerate insights response: {response.status_code}")
    if response.status_code == 200:
        print("AI insights generated successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    return response

def main():
    print("Testing AI Insights functionality...")
    
    # Get access token
    token = get_access_token()
    if not token:
        return
    
    project_id = 1
    
    # Test creating an insight
    print(f"\n1. Creating AI insight for project {project_id}...")
    create_ai_insight(token, project_id)
    
    # Test getting insights
    print(f"\n2. Getting insights for project {project_id}...")
    get_project_insights(token, project_id)
    
    # Test AI insights generation
    print(f"\n3. Testing AI insights generation for project {project_id}...")
    test_ai_insights_generation(token, project_id)

if __name__ == "__main__":
    main()