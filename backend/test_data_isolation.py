#!/usr/bin/env python3
"""
Script para probar el aislamiento de datos entre usuarios
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def login_user(email, password):
    """Iniciar sesión con un usuario"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if response.status_code == 200:
        data = response.json()
        return data["access_token"], data["user"]
    else:
        print(f"❌ Error al iniciar sesión con {email}: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None, None

def get_user_projects(token):
    """Obtener proyectos del usuario"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al obtener proyectos: {response.status_code}")
        return []

def get_user_tasks(token):
    """Obtener tareas del usuario"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al obtener tareas: {response.status_code}")
        return []

def create_project(token, name, description):
    """Crear un proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/projects", 
                           headers=headers,
                           json={
                               "name": name,
                               "description": description,
                               "status": "planning"
                           })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al crear proyecto: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def create_task(token, project_id, title, description):
    """Crear una tarea"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/tasks", 
                           headers=headers,
                           json={
                               "title": title,
                               "description": description,
                               "project_id": project_id,
                               "status": "pending",
                               "priority": "medium"
                           })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al crear tarea: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def test_data_isolation():
    """Probar el aislamiento de datos entre usuarios"""
    print("🧪 Probando aislamiento de datos entre usuarios")
    print("=" * 60)
    
    # Usuarios de prueba
    users = [
        {"email": "test@example.com", "password": "testpassword123", "name": "Usuario 1"},
        {"email": "user1@example.com", "password": "userpass123", "name": "Usuario 2"},
        {"email": "user2@example.com", "password": "userpass123", "name": "Usuario 3"}
    ]
    
    user_data = {}
    
    # 1. Iniciar sesión con cada usuario
    print("🔐 Iniciando sesión con usuarios de prueba...")
    for user in users:
        token, user_info = login_user(user["email"], user["password"])
        if token:
            user_data[user["email"]] = {
                "token": token,
                "user_info": user_info,
                "name": user["name"]
            }
            print(f"✅ {user['name']}: Login exitoso (ID: {user_info['id']})")
        else:
            print(f"❌ {user['name']}: Login fallido")
    
    if len(user_data) < 2:
        print("❌ No se pudieron autenticar suficientes usuarios para la prueba")
        return False
    
    print()
    
    # 2. Crear proyectos para cada usuario
    print("📁 Creando proyectos para cada usuario...")
    for email, data in user_data.items():
        project_name = f"Proyecto de {data['name']}"
        project_desc = f"Proyecto exclusivo de {data['name']}"
        
        project = create_project(data["token"], project_name, project_desc)
        if project:
            data["project"] = project
            print(f"✅ {data['name']}: Proyecto creado (ID: {project['id']})")
        else:
            print(f"❌ {data['name']}: Error al crear proyecto")
    
    print()
    
    # 3. Crear tareas para cada proyecto
    print("📝 Creando tareas para cada proyecto...")
    for email, data in user_data.items():
        if "project" in data:
            task_title = f"Tarea de {data['name']}"
            task_desc = f"Tarea exclusiva de {data['name']}"
            
            task = create_task(data["token"], data["project"]["id"], task_title, task_desc)
            if task:
                data["task"] = task
                print(f"✅ {data['name']}: Tarea creada (ID: {task['id']})")
            else:
                print(f"❌ {data['name']}: Error al crear tarea")
    
    print()
    
    # 4. Verificar aislamiento de proyectos
    print("🔒 Verificando aislamiento de proyectos...")
    isolation_success = True
    
    for email, data in user_data.items():
        projects = get_user_projects(data["token"])
        user_project_ids = [p["id"] for p in projects]
        
        print(f"👤 {data['name']} ve {len(projects)} proyecto(s): {user_project_ids}")
        
        # Verificar que solo ve sus propios proyectos
        for other_email, other_data in user_data.items():
            if other_email != email and "project" in other_data:
                other_project_id = other_data["project"]["id"]
                if other_project_id in user_project_ids:
                    print(f"❌ {data['name']} puede ver el proyecto de {other_data['name']} (ID: {other_project_id})")
                    isolation_success = False
                else:
                    print(f"✅ {data['name']} NO puede ver el proyecto de {other_data['name']}")
    
    print()
    
    # 5. Verificar aislamiento de tareas
    print("🔒 Verificando aislamiento de tareas...")
    
    for email, data in user_data.items():
        tasks = get_user_tasks(data["token"])
        user_task_ids = [t["id"] for t in tasks]
        
        print(f"👤 {data['name']} ve {len(tasks)} tarea(s): {user_task_ids}")
        
        # Verificar que solo ve sus propias tareas
        for other_email, other_data in user_data.items():
            if other_email != email and "task" in other_data:
                other_task_id = other_data["task"]["id"]
                if other_task_id in user_task_ids:
                    print(f"❌ {data['name']} puede ver la tarea de {other_data['name']} (ID: {other_task_id})")
                    isolation_success = False
                else:
                    print(f"✅ {data['name']} NO puede ver la tarea de {other_data['name']}")
    
    print()
    print("=" * 60)
    
    if isolation_success:
        print("✅ PRUEBA EXITOSA: El aislamiento de datos funciona correctamente")
        print("   - Cada usuario solo puede ver sus propios proyectos")
        print("   - Cada usuario solo puede ver sus propias tareas")
        return True
    else:
        print("❌ PRUEBA FALLIDA: Se detectaron problemas de aislamiento de datos")
        return False

if __name__ == "__main__":
    success = test_data_isolation()
    exit(0 if success else 1)