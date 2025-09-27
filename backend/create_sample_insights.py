#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
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

def create_insight(token, project_id, insight_data):
    """Create an AI insight"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/ai-insights/project/{project_id}/insights", 
                           json=insight_data, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Created insight: {insight_data['title']}")
        return response.json()
    else:
        print(f"✗ Error creating insight: {response.text}")
        return None

def main():
    print("Creating sample AI insights...")
    
    # Get access token
    token = get_access_token()
    if not token:
        return
    
    project_id = 1
    
    # Sample insights
    insights = [
        {
            "project_id": project_id,
            "insight_type": "progress_prediction",
            "priority": "medium",
            "title": "Predicción de Progreso del Proyecto",
            "description": "Basado en el ritmo actual, el proyecto se completará en 3 semanas",
            "recommendations": "Mantener el ritmo actual de desarrollo",
            "confidence_score": 0.75
        },
        {
            "project_id": project_id,
            "insight_type": "team_performance",
            "priority": "low",
            "title": "Análisis de Rendimiento del Equipo",
            "description": "El equipo muestra alta productividad con buena colaboración",
            "recommendations": "Continuar con las prácticas actuales de trabajo en equipo",
            "confidence_score": 0.90
        },
        {
            "project_id": project_id,
            "insight_type": "budget_forecast",
            "priority": "high",
            "title": "Pronóstico de Presupuesto",
            "description": "El proyecto está 15% por encima del presupuesto planificado",
            "recommendations": "Revisar gastos y optimizar recursos para los próximos sprints",
            "confidence_score": 0.80
        },
        {
            "project_id": project_id,
            "insight_type": "deadline_alert",
            "priority": "critical",
            "title": "Alerta de Fecha Límite",
            "description": "Riesgo alto de no cumplir con la fecha límite del proyecto",
            "recommendations": "Considerar agregar recursos adicionales o ajustar el alcance",
            "confidence_score": 0.95
        }
    ]
    
    # Create insights
    created_insights = []
    for insight_data in insights:
        result = create_insight(token, project_id, insight_data)
        if result:
            created_insights.append(result)
    
    print(f"\n✓ Successfully created {len(created_insights)} insights")
    
    # Test dashboard again
    print("\nTesting dashboard with new insights...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/ai-insights/dashboard/insights", headers=headers)
    
    if response.status_code == 200:
        dashboard_data = response.json()
        print(f"Dashboard insights: {dashboard_data['summary']['total_insights']} total")
        print(f"Risk alerts: {dashboard_data['summary']['risk_alerts']}")
        print(f"Recommendations: {dashboard_data['summary']['recommendations']}")
        print(f"Predictions: {dashboard_data['summary']['predictions']}")
    else:
        print(f"Error getting dashboard: {response.text}")

if __name__ == "__main__":
    main()