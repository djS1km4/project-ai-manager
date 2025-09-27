#!/usr/bin/env python3
"""
Script para probar los endpoints de tareas y diagnosticar problemas
"""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_login(email, password):
    """Probar login y obtener token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login exitoso para {email}")
            return token_data.get("access_token")
        else:
            print(f"❌ Error en login para {email}: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión en login: {e}")
        return None

def test_tasks_endpoint(token, user_type):
    """Probar endpoint de tareas"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Probar endpoint de tareas
        response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
        
        print(f"\n🔍 Probando endpoint de tareas para {user_type}:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"   ✅ Tareas obtenidas: {len(tasks)} tareas")
            if tasks:
                print(f"   📋 Primera tarea: {tasks[0].get('title', 'Sin título')}")
        else:
            print(f"   ❌ Error: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error de conexión en tareas: {e}")
        return False

def test_admin_tasks_endpoint(token):
    """Probar endpoint de tareas de admin"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Probar endpoint de tareas de admin
        response = requests.get(f"{BASE_URL}/api/v1/admin/tasks", headers=headers)
        
        print(f"\n🔍 Probando endpoint de tareas de admin:")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"   ✅ Tareas de admin obtenidas: {len(tasks)} tareas")
        else:
            print(f"   ❌ Error: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error de conexión en tareas de admin: {e}")
        return False

def main():
    print("🧪 Probando endpoints de tareas...")
    
    # Probar con usuario regular
    print("\n👤 Probando con usuario regular:")
    regular_token = test_login("test@example.com", "testpassword123")
    if regular_token:
        test_tasks_endpoint(regular_token, "usuario regular")
    
    # Probar con administrador
    print("\n🔐 Probando con administrador:")
    admin_token = test_login("admin@example.com", "adminpassword123")
    if admin_token:
        test_tasks_endpoint(admin_token, "administrador")
        test_admin_tasks_endpoint(admin_token)
    
    print("\n📊 Pruebas completadas")

if __name__ == "__main__":
    main()