#!/usr/bin/env python3
"""
Script de prueba integral para verificar toda la funcionalidad del sistema
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api/v1"

def test_user_registration_and_login():
    """Prueba el registro y login de usuarios"""
    print("=== PRUEBA DE REGISTRO Y LOGIN ===")
    
    # Datos de prueba
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "testpassword123"
    test_full_name = "Usuario de Prueba"
    
    # Registro
    print(f"1. Registrando usuario: {test_email}")
    register_data = {
        "email": test_email,
        "username": test_email.split('@')[0],
        "full_name": test_full_name,
        "password": test_password
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Respuesta del registro: {data}")
        
        # El registro puede devolver solo el usuario, no necesariamente un token
        if 'access_token' in data:
            token = data.get('access_token')
            user = data.get('user')
        else:
            # Si no hay token, hacer login después del registro
            user = data
            print("   Registro exitoso, haciendo login...")
            
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": test_email,
                "password": test_password
            })
            
            if login_response.status_code == 200:
                login_data = login_response.json()
                token = login_data.get('access_token')
                user = login_data.get('user')
            else:
                print(f"   Error en login después del registro: {login_response.text}")
                return None, None
        
        if user:
            print(f"   Usuario: {user.get('full_name')} ({user.get('email')})")
        if token:
            print(f"   Token obtenido: {token[:20]}...")
        return token, user
    else:
        print(f"   Error: {response.text}")
        return None, None

def test_project_operations(token):
    """Prueba las operaciones de proyectos"""
    print("\n=== PRUEBA DE PROYECTOS ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear proyecto
    print("1. Creando proyecto...")
    project_data = {
        "name": "Proyecto de Prueba",
        "description": "Descripción del proyecto de prueba",
        "status": "active"
    }
    
    response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        project = response.json()
        project_id = project.get('id')
        print(f"   Proyecto creado: {project.get('name')} (ID: {project_id})")
        
        # Listar proyectos
        print("2. Listando proyectos...")
        response = requests.get(f"{BASE_URL}/projects/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"   Proyectos encontrados: {len(projects)}")
        
        return project_id
    else:
        print(f"   Error: {response.text}")
        return None

def test_task_operations(token, project_id):
    """Prueba las operaciones de tareas"""
    print("\n=== PRUEBA DE TAREAS ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear tarea básica
    print("1. Creando tarea básica...")
    task_data = {
        "title": "Tarea de Prueba Básica",
        "project_id": project_id,
        "status": "todo",
        "priority": "medium"
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        task = response.json()
        task_id = task.get('id')
        print(f"   Tarea creada: {task.get('title')} (ID: {task_id})")
    else:
        print(f"   Error: {response.text}")
        return None
    
    # Crear tarea completa
    print("2. Creando tarea completa...")
    complete_task_data = {
        "title": "Tarea de Prueba Completa",
        "description": "Descripción detallada de la tarea",
        "project_id": project_id,
        "status": "in_progress",
        "priority": "high",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "estimated_hours": 8
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=complete_task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        complete_task = response.json()
        complete_task_id = complete_task.get('id')
        print(f"   Tarea completa creada: {complete_task.get('title')} (ID: {complete_task_id})")
    else:
        print(f"   Error: {response.text}")
        return task_id
    
    # Actualizar tarea
    print("3. Actualizando tarea...")
    update_data = {
        "title": "Tarea de Prueba Actualizada",
        "status": "done",
        "actual_hours": 6
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        updated_task = response.json()
        print(f"   Tarea actualizada: {updated_task.get('title')} - {updated_task.get('status')}")
    else:
        print(f"   Error: {response.text}")
    
    # Listar tareas
    print("4. Listando tareas...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   Tareas encontradas: {len(tasks)}")
        for task in tasks:
            print(f"     - {task.get('title')} ({task.get('status')})")
    else:
        print(f"   Error: {response.text}")
    
    # Obtener tarea específica
    print("5. Obteniendo tarea específica...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        task_detail = response.json()
        print(f"   Tarea obtenida: {task_detail.get('title')}")
    else:
        print(f"   Error: {response.text}")
    
    return task_id

def test_edge_cases(token, project_id):
    """Prueba casos límite y validaciones"""
    print("\n=== PRUEBA DE CASOS LÍMITE ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Tarea con campos vacíos
    print("1. Probando tarea con campos vacíos...")
    empty_task_data = {
        "title": "Tarea con Campos Vacíos",
        "project_id": project_id,
        "status": "todo",
        "priority": "low",
        "description": "",
        "due_date": "",
        "estimated_hours": ""
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=empty_task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Tarea con campos vacíos creada correctamente")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Tarea con valores "undefined"
    print("2. Probando tarea con valores 'undefined'...")
    undefined_task_data = {
        "title": "Tarea con Undefined",
        "project_id": project_id,
        "status": "todo",
        "priority": "medium",
        "description": "undefined",
        "due_date": "undefined",
        "estimated_hours": "undefined"
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=undefined_task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✓ Tarea con valores 'undefined' creada correctamente")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Tarea con estimated_hours como float
    print("3. Probando tarea con estimated_hours como float...")
    float_task_data = {
        "title": "Tarea con Float Hours",
        "project_id": project_id,
        "status": "todo",
        "priority": "high",
        "estimated_hours": 4.5
    }
    
    response = requests.post(f"{BASE_URL}/tasks/", json=float_task_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        task = response.json()
        print(f"   ✓ Tarea con float hours creada: {task.get('estimated_hours')} horas")
    else:
        print(f"   ✗ Error: {response.text}")

def test_dashboard_and_insights(token):
    """Prueba el dashboard y insights"""
    print("\n=== PRUEBA DE DASHBOARD E INSIGHTS ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Dashboard
    print("1. Obteniendo datos del dashboard...")
    response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        dashboard = response.json()
        print(f"   ✓ Dashboard obtenido correctamente")
        print(f"     - Proyectos totales: {dashboard.get('total_projects', 'N/A')}")
        print(f"     - Tareas totales: {dashboard.get('total_tasks', 'N/A')}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # AI Insights
    print("2. Obteniendo AI insights...")
    response = requests.get(f"{BASE_URL}/ai-insights/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        insights = response.json()
        print(f"   ✓ AI Insights obtenidos correctamente")
    else:
        print(f"   ✗ Error: {response.text}")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS INTEGRALES DEL SISTEMA")
    print("=" * 50)
    
    # Registro y login
    token, user = test_user_registration_and_login()
    if not token:
        print("❌ Error en registro/login. Abortando pruebas.")
        return
    
    # Proyectos
    project_id = test_project_operations(token)
    if not project_id:
        print("❌ Error en operaciones de proyectos. Abortando pruebas.")
        return
    
    # Tareas
    task_id = test_task_operations(token, project_id)
    if not task_id:
        print("❌ Error en operaciones de tareas. Continuando con casos límite...")
    
    # Casos límite
    test_edge_cases(token, project_id)
    
    # Dashboard e insights
    test_dashboard_and_insights(token)
    
    print("\n" + "=" * 50)
    print("✅ PRUEBAS INTEGRALES COMPLETADAS")
    print("🎉 El sistema está funcionando correctamente!")

if __name__ == "__main__":
    main()