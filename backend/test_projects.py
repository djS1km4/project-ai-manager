#!/usr/bin/env python3
"""
Script para probar la funcionalidad de proyectos
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
PROJECTS_URL = f"{BASE_URL}/projects/"

def login():
    """Login y obtener token"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login exitoso")
        return token
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None

def test_get_projects(token):
    """Probar obtener lista de proyectos"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROJECTS_URL, headers=headers)
    
    print(f"\n📥 GET /projects/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Proyectos obtenidos: {len(projects)}")
        for project in projects:
            print(f"  - {project['name']} (ID: {project['id']}, Status: {project['status']})")
        return projects
    else:
        print(f"❌ Error obteniendo proyectos: {response.text}")
        return []

def test_create_project(token):
    """Probar creación de proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    
    project_data = {
        "name": "Proyecto de Prueba API",
        "description": "Este es un proyecto de prueba creado desde la API",
        "status": "active",
        "priority": "medium",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "budget": 50000.0
    }
    
    print(f"\n📤 POST /projects/")
    print(f"Enviando datos: {json.dumps(project_data, indent=2)}")
    
    response = requests.post(PROJECTS_URL, json=project_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200 or response.status_code == 201:
        print("✅ Proyecto creado exitosamente")
        return response.json()
    else:
        print("❌ Error creando proyecto")
        return None

def test_update_project(token, project_id):
    """Probar actualización de proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "description": "Descripción actualizada desde la API",
        "status": "on_hold"
    }
    
    print(f"\n📤 PUT /projects/{project_id}/")
    print(f"Enviando datos: {json.dumps(update_data, indent=2)}")
    
    response = requests.put(f"{PROJECTS_URL}{project_id}/", json=update_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Proyecto actualizado exitosamente")
        return response.json()
    else:
        print("❌ Error actualizando proyecto")
        return None

def main():
    print("🚀 Iniciando prueba de funcionalidad de proyectos...\n")
    
    # 1. Login
    token = login()
    if not token:
        return
    
    # 2. Obtener proyectos existentes
    existing_projects = test_get_projects(token)
    
    # 3. Crear nuevo proyecto
    new_project = test_create_project(token)
    
    if new_project:
        project_id = new_project["id"]
        
        # 4. Actualizar proyecto
        updated_project = test_update_project(token, project_id)
        
        # 5. Verificar cambios obteniendo proyectos nuevamente
        print(f"\n🔍 Verificando cambios...")
        final_projects = test_get_projects(token)
        
        print(f"\n✅ Prueba de proyectos completada exitosamente")
    else:
        print(f"\n❌ Prueba de proyectos fallida")

if __name__ == "__main__":
    main()