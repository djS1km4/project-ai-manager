#!/usr/bin/env python3
"""
Script para debuggear errores de validación 422 en la creación de tareas
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
TASKS_URL = f"{BASE_URL}/tasks/"
PROJECTS_URL = f"{BASE_URL}/projects/"

def login():
    """Login y obtener token"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access_token')
            print(f"✅ Login exitoso. Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión en login: {e}")
        return None

def get_projects(token):
    """Obtener proyectos disponibles"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(PROJECTS_URL, headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Proyectos obtenidos: {len(projects)}")
            for project in projects[:3]:
                print(f"  - ID: {project['id']}, Nombre: {project['name']}")
            return projects
        else:
            print(f"❌ Error obteniendo proyectos: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión obteniendo proyectos: {e}")
        return []

def test_task_creation_scenarios(token, projects):
    """Probar diferentes escenarios de creación de tareas"""
    headers = {"Authorization": f"Bearer {token}"}
    
    if not projects:
        print("❌ No hay proyectos disponibles para probar")
        return
    
    project_id = projects[0]['id']
    
    # Escenario 1: Datos mínimos requeridos
    print("\n🧪 Escenario 1: Datos mínimos requeridos")
    task_data_minimal = {
        "title": "Tarea mínima",
        "project_id": project_id
    }
    test_single_task_creation(headers, task_data_minimal, "Mínimos")
    
    # Escenario 2: Datos completos como frontend
    print("\n🧪 Escenario 2: Datos completos como frontend")
    task_data_complete = {
        "title": "Tarea completa frontend",
        "description": "Descripción de la tarea",
        "project_id": project_id,
        "priority": "medium",
        "status": "todo",
        "due_date": "2024-12-31",
        "estimated_hours": 5
    }
    test_single_task_creation(headers, task_data_complete, "Completos")
    
    # Escenario 3: Con assignee_id null
    print("\n🧪 Escenario 3: Con assignee_id null")
    task_data_null_assignee = {
        "title": "Tarea con assignee null",
        "project_id": project_id,
        "assignee_id": None
    }
    test_single_task_creation(headers, task_data_null_assignee, "Assignee null")
    
    # Escenario 4: Con campos undefined/vacíos
    print("\n🧪 Escenario 4: Con campos vacíos")
    task_data_empty = {
        "title": "Tarea con campos vacíos",
        "description": "",
        "project_id": project_id,
        "assignee_id": None,
        "due_date": "",
        "estimated_hours": None
    }
    test_single_task_creation(headers, task_data_empty, "Campos vacíos")
    
    # Escenario 5: Fecha en formato ISO
    print("\n🧪 Escenario 5: Fecha en formato ISO")
    task_data_iso_date = {
        "title": "Tarea con fecha ISO",
        "project_id": project_id,
        "due_date": "2024-12-31T23:59:59Z"
    }
    test_single_task_creation(headers, task_data_iso_date, "Fecha ISO")
    
    # Escenario 6: estimated_hours como float
    print("\n🧪 Escenario 6: estimated_hours como float")
    task_data_float_hours = {
        "title": "Tarea con horas float",
        "project_id": project_id,
        "estimated_hours": 5.5
    }
    test_single_task_creation(headers, task_data_float_hours, "Horas float")

def test_single_task_creation(headers, task_data, scenario_name):
    """Probar creación de una sola tarea"""
    print(f"📤 Enviando datos ({scenario_name}):")
    print(json.dumps(task_data, indent=2))
    
    try:
        response = requests.post(TASKS_URL, json=task_data, headers=headers)
        
        print(f"📥 Respuesta:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"✅ Éxito - Tarea creada")
            result = response.json()
            print(f"ID: {result.get('id')}, Título: {result.get('title')}")
        else:
            print(f"❌ Error - {response.status_code}")
            try:
                error_data = response.json()
                print(f"Detalle del error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Respuesta de error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("-" * 50)

def main():
    print("🔍 Debuggeando errores de validación 422 en tareas")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        return
    
    # Obtener proyectos
    projects = get_projects(token)
    
    # Probar diferentes escenarios
    test_task_creation_scenarios(token, projects)
    
    print("\n✅ Debugging completado")

if __name__ == "__main__":
    main()