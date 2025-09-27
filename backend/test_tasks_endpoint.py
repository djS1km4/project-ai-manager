#!/usr/bin/env python3
"""
Script para probar específicamente el endpoint de tareas
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_tasks_endpoint():
    """Probar el endpoint de tareas con ambas cuentas"""
    print("🧪 Probando endpoint de tareas")
    print("=" * 50)
    
    # Credenciales de prueba
    accounts = [
        {
            "name": "Administrador",
            "email": "test@example.com",
            "password": "testpassword123"
        },
        {
            "name": "Usuario Regular",
            "email": "usuario@example.com",
            "password": "usuario123"
        }
    ]
    
    for account in accounts:
        print(f"\n🔐 Probando con {account['name']}:")
        print(f"   Email: {account['email']}")
        
        # Login
        login_data = {
            "email": account["email"],
            "password": account["password"]
        }
        
        try:
            login_response = requests.post(
                f"{BASE_URL}/auth/login", 
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code != 200:
                print(f"❌ Error en login: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                continue
                
            token_data = login_response.json()
            token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            print(f"✅ Login exitoso")
            
            # Probar endpoint de tareas
            print("📋 Probando GET /tasks/")
            tasks_response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
            
            print(f"   Status Code: {tasks_response.status_code}")
            
            if tasks_response.status_code == 200:
                tasks = tasks_response.json()
                print(f"✅ Tareas obtenidas exitosamente")
                print(f"   Total de tareas: {len(tasks)}")
                
                # Mostrar algunas tareas
                if tasks:
                    print("   Primeras 3 tareas:")
                    for i, task in enumerate(tasks[:3]):
                        print(f"     {i+1}. {task.get('title', 'Sin título')} - Estado: {task.get('status', 'N/A')}")
                else:
                    print("   No hay tareas disponibles")
            else:
                print(f"❌ Error al obtener tareas")
                print(f"   Response: {tasks_response.text}")
                
            # Probar endpoint de proyectos (para verificar que hay datos)
            print("📁 Probando GET /projects/")
            projects_response = requests.get(f"{BASE_URL}/projects/", headers=headers)
            
            print(f"   Status Code: {projects_response.status_code}")
            
            if projects_response.status_code == 200:
                projects = projects_response.json()
                print(f"✅ Proyectos obtenidos exitosamente")
                print(f"   Total de proyectos: {len(projects)}")
            else:
                print(f"❌ Error al obtener proyectos")
                print(f"   Response: {projects_response.text}")
                
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    test_tasks_endpoint()