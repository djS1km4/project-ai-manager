#!/usr/bin/env python3
"""
Script para probar la comunicación frontend-backend y diagnosticar problemas
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_auth():
    """Probar autenticación"""
    print("🔐 Probando autenticación...")
    
    # Login
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Token obtenido: {token[:50]}...")
            return token
        else:
            print(f"Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

def test_projects(token):
    """Probar endpoints de proyectos"""
    print("\n📁 Probando endpoints de proyectos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Obtener proyectos
        response = requests.get(f"{BASE_URL}/projects/", headers=headers)
        print(f"GET Projects Status: {response.status_code}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"Proyectos encontrados: {len(projects)}")
            for project in projects[:3]:  # Mostrar solo los primeros 3
                print(f"  - {project.get('name', 'Sin nombre')}")
        else:
            print(f"Error al obtener proyectos: {response.text}")
            
        # Crear proyecto de prueba
        project_data = {
            "name": "Proyecto Frontend Test",
            "description": "Proyecto creado para probar frontend",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 10000,
            "status": "planning"
        }
        
        response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        print(f"POST Project Status: {response.status_code}")
        
        if response.status_code == 200:
            new_project = response.json()
            print(f"Proyecto creado: {new_project.get('name')} (ID: {new_project.get('id')})")
            return new_project.get('id')
        else:
            print(f"Error al crear proyecto: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error en proyectos: {e}")
        return None

def test_tasks(token, project_id):
    """Probar endpoints de tareas"""
    print("\n📋 Probando endpoints de tareas...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Obtener tareas
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
        print(f"GET Tasks Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"Tareas encontradas: {len(tasks)}")
        else:
            print(f"Error al obtener tareas: {response.text}")
            
        # Crear tarea de prueba
        if project_id:
            task_data = {
                "title": "Tarea Frontend Test",
                "description": "Tarea creada para probar frontend",
                "project_id": project_id,
                "priority": "medium",
                "status": "todo",
                "due_date": "2024-12-31"
            }
            
            response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
            print(f"POST Task Status: {response.status_code}")
            
            if response.status_code == 200:
                new_task = response.json()
                print(f"Tarea creada: {new_task.get('title')} (ID: {new_task.get('id')})")
            else:
                print(f"Error al crear tarea: {response.text}")
                
    except Exception as e:
        print(f"Error en tareas: {e}")

def test_cors():
    """Probar configuración CORS"""
    print("\n🌐 Probando configuración CORS...")
    
    try:
        # Hacer una petición OPTIONS para verificar CORS
        response = requests.options(f"{BASE_URL}/projects/")
        print(f"OPTIONS Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
    except Exception as e:
        print(f"Error en CORS: {e}")

def main():
    print("🚀 Iniciando diagnóstico Frontend-Backend\n")
    
    # Probar autenticación
    token = test_auth()
    
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return
    
    # Probar proyectos
    project_id = test_projects(token)
    
    # Probar tareas
    test_tasks(token, project_id)
    
    # Probar CORS
    test_cors()
    
    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    main()