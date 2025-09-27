#!/usr/bin/env python3
"""
Script para probar la creación de tareas y verificar la estructura de datos
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
TASKS_URL = f"{BASE_URL}/tasks/"
PROJECTS_URL = f"{BASE_URL}/projects/"
USERS_URL = f"{BASE_URL}/auth/users"

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

def get_projects(token):
    """Obtener lista de proyectos"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROJECTS_URL, headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Proyectos obtenidos: {len(projects)}")
        return projects
    else:
        print(f"❌ Error obteniendo proyectos: {response.status_code} - {response.text}")
        return []

def get_users(token):
    """Obtener lista de usuarios"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(USERS_URL, headers=headers)
    
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Usuarios obtenidos: {len(users)}")
        return users
    else:
        print(f"❌ Error obteniendo usuarios: {response.status_code} - {response.text}")
        return []

def test_task_creation(token, project_id, assignee_id=None):
    """Probar creación de tarea"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Datos de la tarea según el esquema del backend
    task_data = {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea de prueba para verificar la API",
        "project_id": project_id,
        "priority": "medium",
        "status": "todo",
        "due_date": "2024-12-31",
        "estimated_hours": 5.0
    }
    
    # Agregar assignee_id solo si se proporciona
    if assignee_id:
        task_data["assignee_id"] = assignee_id
    
    print(f"\n📤 Enviando datos de tarea:")
    print(json.dumps(task_data, indent=2))
    
    response = requests.post(TASKS_URL, json=task_data, headers=headers)
    
    print(f"\n📥 Respuesta del servidor:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200 or response.status_code == 201:
        print("✅ Tarea creada exitosamente")
        return response.json()
    else:
        print("❌ Error creando tarea")
        return None

def main():
    print("🚀 Iniciando prueba de creación de tareas...\n")
    
    # 1. Login
    token = login()
    if not token:
        return
    
    # 2. Obtener proyectos
    projects = get_projects(token)
    if not projects:
        print("❌ No hay proyectos disponibles")
        return
    
    project_id = projects[0]["id"]
    print(f"📁 Usando proyecto: {projects[0]['name']} (ID: {project_id})")
    
    # 3. Obtener usuarios
    users = get_users(token)
    assignee_id = None
    if users:
        assignee_id = users[0]["id"]
        print(f"👤 Usando asignado: {users[0].get('name', users[0]['email'])} (ID: {assignee_id})")
    
    # 4. Probar creación de tarea
    print(f"\n🧪 Probando creación de tarea...")
    task = test_task_creation(token, project_id, assignee_id)
    
    if task:
        print(f"\n✅ Prueba completada exitosamente")
        print(f"Tarea creada con ID: {task.get('id')}")
    else:
        print(f"\n❌ Prueba fallida")

if __name__ == "__main__":
    main()