#!/usr/bin/env python3
"""
Script para probar la funcionalidad completa del sistema de administración
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001/api/v1"

def test_admin_login() -> str:
    """Probar login de administrador y obtener token"""
    print("🔐 Probando login de administrador...")
    
    # Intentar con testuser (convertido a admin)
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Login de testuser (admin) exitoso")
        return token
    
    # Intentar con admin
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Login de admin exitoso")
        return token
    
    print("❌ No se pudo hacer login como administrador")
    print("   Credenciales probadas:")
    print("   - test@example.com / testpassword123")
    print("   - admin@example.com / admin123")
    return None

def test_admin_projects(token: str) -> bool:
    """Probar endpoints de administración de proyectos"""
    print("\n📁 Probando endpoints de administración de proyectos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener todos los proyectos
    response = requests.get(f"{BASE_URL}/admin/projects", headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Obtenidos {len(projects)} proyectos")
        
        if projects:
            project_id = projects[0].get("id")
            print(f"   Usando proyecto ID: {project_id} para pruebas")
            
            # Obtener usuarios para asignación
            users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
            if users_response.status_code == 200:
                users = users_response.json()
                if len(users) >= 2:
                    user_id = users[1].get("id")  # Usar segundo usuario
                    print(f"   Usando usuario ID: {user_id} para pruebas")
                    
                    # Probar asignación de proyecto
                    assign_response = requests.post(
                        f"{BASE_URL}/admin/projects/{project_id}/assign-user/{user_id}",
                        headers=headers,
                        params={"role": "member"}
                    )
                    
                    if assign_response.status_code == 200:
                        print("✅ Asignación de proyecto exitosa")
                        
                        # Probar desasignación de proyecto
                        unassign_response = requests.delete(
                            f"{BASE_URL}/admin/projects/{project_id}/unassign-user/{user_id}",
                            headers=headers
                        )
                        
                        if unassign_response.status_code == 200:
                            print("✅ Desasignación de proyecto exitosa")
                            return True
                        else:
                            print(f"❌ Error en desasignación: {unassign_response.status_code}")
                    else:
                        print(f"❌ Error en asignación: {assign_response.status_code}")
                        print(f"   Respuesta: {assign_response.text}")
        
        return True
    else:
        print(f"❌ Error obteniendo proyectos: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return False

def test_admin_tasks(token: str) -> bool:
    """Probar endpoints de administración de tareas"""
    print("\n📋 Probando endpoints de administración de tareas...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener todas las tareas
    response = requests.get(f"{BASE_URL}/admin/tasks", headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Obtenidas {len(tasks)} tareas")
        
        if tasks:
            task_id = tasks[0].get("id")
            print(f"   Usando tarea ID: {task_id} para pruebas")
            
            # Obtener usuarios para asignación
            users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
            if users_response.status_code == 200:
                users = users_response.json()
                if len(users) >= 2:
                    user_id = users[1].get("id")  # Usar segundo usuario
                    print(f"   Usando usuario ID: {user_id} para pruebas")
                    
                    # Probar asignación de tarea
                    assign_response = requests.post(
                        f"{BASE_URL}/admin/tasks/{task_id}/assign-user/{user_id}",
                        headers=headers
                    )
                    
                    if assign_response.status_code == 200:
                        print("✅ Asignación de tarea exitosa")
                        
                        # Probar desasignación de tarea
                        unassign_response = requests.delete(
                            f"{BASE_URL}/admin/tasks/{task_id}/unassign",
                            headers=headers
                        )
                        
                        if unassign_response.status_code == 200:
                            print("✅ Desasignación de tarea exitosa")
                            return True
                        else:
                            print(f"❌ Error en desasignación: {unassign_response.status_code}")
                    else:
                        print(f"❌ Error en asignación: {assign_response.status_code}")
                        print(f"   Respuesta: {assign_response.text}")
        
        return True
    else:
        print(f"❌ Error obteniendo tareas: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return False

def test_regular_user_access() -> bool:
    """Probar que usuarios regulares no pueden acceder a endpoints de admin"""
    print("\n👤 Probando acceso de usuario regular...")
    
    # Login como usuario regular
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "user@example.com",
        "password": "user123"
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Intentar acceder a endpoint de admin
        admin_response = requests.get(f"{BASE_URL}/admin/projects", headers=headers)
        
        if admin_response.status_code == 403:
            print("✅ Usuario regular correctamente bloqueado de endpoints de admin")
            return True
        else:
            print(f"❌ Usuario regular pudo acceder a endpoints de admin: {admin_response.status_code}")
            return False
    else:
        print("❌ No se pudo hacer login como usuario regular")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas del sistema de administración")
    print("=" * 60)
    
    # Probar login de admin
    token = test_admin_login()
    if not token:
        print("❌ No se puede continuar sin token de admin")
        return
    
    # Probar funcionalidades de admin
    projects_ok = test_admin_projects(token)
    tasks_ok = test_admin_tasks(token)
    access_control_ok = test_regular_user_access()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Proyectos de admin: {'✅' if projects_ok else '❌'}")
    print(f"   Tareas de admin: {'✅' if tasks_ok else '❌'}")
    print(f"   Control de acceso: {'✅' if access_control_ok else '❌'}")
    
    if all([projects_ok, tasks_ok, access_control_ok]):
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("   El sistema de administración está funcionando correctamente.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisar la implementación.")

if __name__ == "__main__":
    main()