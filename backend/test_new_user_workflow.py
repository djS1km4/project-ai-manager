#!/usr/bin/env python3
"""
Prueba del flujo completo para nuevos usuarios:
- Login
- Crear proyecto
- Crear tareas en el proyecto
- Verificar que pueden ver sus datos
"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def login_user(email, password):
    """Iniciar sesión con un usuario"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        print(f"❌ Error al iniciar sesión: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def create_project(token, name, description):
    """Crear un nuevo proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/projects/", 
                           headers=headers,
                           json={
                               "name": name,
                               "description": description,
                               "status": "active"
                           })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al crear proyecto: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def create_task(token, project_id, title, description):
    """Crear una nueva tarea"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/tasks/", 
                           headers=headers,
                           json={
                               "title": title,
                               "description": description,
                               "status": "todo",  # Usar estado válido
                               "priority": "medium",
                               "project_id": project_id
                           })
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al crear tarea: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def get_user_projects(token):
    """Obtener proyectos del usuario"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al obtener proyectos: {response.status_code}")
        return []

def get_user_tasks(token):
    """Obtener tareas del usuario"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al obtener tareas: {response.status_code}")
        return []

def test_new_user_workflow():
    """Probar el flujo completo de un nuevo usuario"""
    print("🧪 Probando flujo completo de nuevo usuario")
    print("=" * 60)
    
    # Probar con user1
    print("🔐 Iniciando sesión con user1@example.com...")
    token = login_user("user1@example.com", "userpass123")
    
    if not token:
        print("❌ No se pudo autenticar el usuario")
        return False
    
    print("✅ Login exitoso")
    
    # Crear un proyecto
    print("\n📁 Creando proyecto de prueba...")
    project = create_project(token, "Proyecto de Prueba User1", "Descripción del proyecto de prueba")
    
    if not project:
        print("❌ No se pudo crear el proyecto")
        return False
    
    print(f"✅ Proyecto creado: {project['name']} (ID: {project['id']})")
    
    # Crear algunas tareas
    print("\n📝 Creando tareas de prueba...")
    tasks_data = [
        {"title": "Tarea 1", "description": "Primera tarea de prueba"},
        {"title": "Tarea 2", "description": "Segunda tarea de prueba"},
        {"title": "Tarea 3", "description": "Tercera tarea de prueba"}
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        task = create_task(token, project['id'], task_data['title'], task_data['description'])
        if task:
            created_tasks.append(task)
            print(f"✅ Tarea creada: {task['title']} (ID: {task['id']})")
        else:
            print(f"❌ No se pudo crear la tarea: {task_data['title']}")
    
    # Verificar que el usuario puede ver sus datos
    print("\n🔍 Verificando datos del usuario...")
    projects = get_user_projects(token)
    tasks = get_user_tasks(token)
    
    print(f"📁 Proyectos visibles: {len(projects)}")
    print(f"📝 Tareas visibles: {len(tasks)}")
    
    # Verificar que el proyecto creado está en la lista
    project_found = any(p['id'] == project['id'] for p in projects)
    if project_found:
        print("✅ El usuario puede ver su proyecto")
    else:
        print("❌ El usuario NO puede ver su proyecto")
        return False
    
    # Verificar que las tareas creadas están en la lista
    tasks_found = sum(1 for t in tasks if t['id'] in [ct['id'] for ct in created_tasks])
    if tasks_found == len(created_tasks):
        print(f"✅ El usuario puede ver todas sus tareas ({tasks_found}/{len(created_tasks)})")
    else:
        print(f"❌ El usuario NO puede ver todas sus tareas ({tasks_found}/{len(created_tasks)})")
        return False
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA EXITOSA: El flujo completo funciona correctamente")
    print("   - Login exitoso")
    print("   - Creación de proyecto exitosa")
    print("   - Creación de tareas exitosa")
    print("   - Visualización de datos exitosa")
    
    return True

if __name__ == "__main__":
    test_new_user_workflow()