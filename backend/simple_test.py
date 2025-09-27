#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
PROJECTS_URL = f"{BASE_URL}/api/v1/projects"

def login():
    login_data = {"email": "admin@example.com", "password": "admin123"}
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_budget_update():
    token = login()
    if not token:
        print("❌ Error de login")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener proyectos
    response = requests.get(PROJECTS_URL, headers=headers)
    projects = response.json()
    
    if not projects:
        print("❌ No hay proyectos")
        return
    
    project = projects[0]
    project_id = project["id"]
    
    print(f"🎯 Proyecto: {project['name']}")
    print(f"💰 Presupuesto original: {project.get('budget', 'N/A')}")
    
    # Test 1: Actualizar solo presupuesto
    update_data = {
        "name": project["name"],
        "description": project.get("description", ""),
        "start_date": project.get("start_date", "2025-01-01"),
        "end_date": project.get("end_date", "2025-12-31"),
        "budget": 99999.99,
        "status": project.get("status", "active")
    }
    
    print(f"\n📤 Enviando presupuesto: {update_data['budget']}")
    
    response = requests.put(f"{PROJECTS_URL}/{project_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        updated = response.json()
        print(f"📥 Presupuesto recibido: {updated.get('budget', 'N/A')}")
        
        # Verificar en DB
        response2 = requests.get(f"{PROJECTS_URL}/{project_id}", headers=headers)
        if response2.status_code == 200:
            fresh = response2.json()
            print(f"🔍 Presupuesto en DB: {fresh.get('budget', 'N/A')}")
            
            if fresh.get('budget') == update_data['budget']:
                print("✅ Presupuesto se guardó correctamente")
            else:
                print("❌ Presupuesto NO se guardó correctamente")
        else:
            print("❌ Error al verificar en DB")
    else:
        print(f"❌ Error en actualización: {response.status_code}")
        print(f"❌ Respuesta: {response.text}")

if __name__ == "__main__":
    test_budget_update()