#!/usr/bin/env python3
"""
Script para probar la creación de proyectos y tareas y diagnosticar errores 422
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8001/api/v1"

def login():
    """Login y obtener token"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login exitoso")
        return token
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def test_project_creation(token):
    """Probar creación de proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    
    project_data = {
        "name": "Proyecto de Prueba",
        "description": "Descripción del proyecto de prueba",
        "start_date": "2024-01-15",
        "end_date": "2024-06-15",
        "budget": 50000,
        "status": "planning"
    }
    
    print("\n🔍 Probando creación de proyecto...")
    print(f"Datos enviados: {json.dumps(project_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 422:
        print("❌ Error 422 - Datos no válidos")
        try:
            error_detail = response.json()
            print(f"Detalles del error: {json.dumps(error_detail, indent=2)}")
        except:
            print("No se pudo parsear el error JSON")
    elif response.status_code in [200, 201]:
        print("✅ Proyecto creado exitosamente")
        return response.json()
    else:
        print(f"❌ Error inesperado: {response.status_code}")
    
    return None

def test_task_creation(token):
    """Probar creación de tarea"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primero obtener proyectos disponibles
    projects_response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    if projects_response.status_code == 200:
        projects = projects_response.json()
        if projects:
            project_id = projects[0]["id"]
            print(f"Usando proyecto ID: {project_id}")
        else:
            print("❌ No hay proyectos disponibles")
            return None
    else:
        print("❌ Error al obtener proyectos")
        return None
    
    task_data = {
        "title": "Tarea de Prueba",
        "description": "Descripción de la tarea de prueba",
        "project_id": project_id,
        "priority": "medium",
        "status": "todo",
        "due_date": "2024-02-15",
        "estimated_hours": 8
    }
    
    print("\n🔍 Probando creación de tarea...")
    print(f"Datos enviados: {json.dumps(task_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 422:
        print("❌ Error 422 - Datos no válidos")
        try:
            error_detail = response.json()
            print(f"Detalles del error: {json.dumps(error_detail, indent=2)}")
        except:
            print("No se pudo parsear el error JSON")
    elif response.status_code in [200, 201]:
        print("✅ Tarea creada exitosamente")
        return response.json()
    else:
        print(f"❌ Error inesperado: {response.status_code}")
    
    return None

def main():
    print("🚀 Iniciando pruebas de creación...")
    
    # Login
    token = login()
    if not token:
        return
    
    # Probar creación de proyecto
    project = test_project_creation(token)
    
    # Probar creación de tarea
    task = test_task_creation(token)
    
    print("\n📋 Resumen de pruebas:")
    print(f"Proyecto: {'✅ Creado' if project else '❌ Error'}")
    print(f"Tarea: {'✅ Creada' if task else '❌ Error'}")

if __name__ == "__main__":
    main()