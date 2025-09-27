#!/usr/bin/env python3
"""
Script para diagnosticar el error 403 en la página de tareas
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001/api/v1"

def login_user(email, password):
    """Login y obtener token"""
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None

def debug_user_access(email, password):
    """Diagnosticar acceso de usuario"""
    print(f"\n🔍 Diagnosticando acceso para: {email}")
    
    # Login
    token = login_user(email, password)
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Verificar información del usuario
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Usuario: {user_info['email']} (ID: {user_info['id']}, Role: {user_info.get('role', 'N/A')})")
    else:
        print(f"❌ Error obteniendo info del usuario: {response.status_code}")
        return
    
    # 2. Verificar proyectos
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Proyectos accesibles: {len(projects)}")
        for project in projects:
            print(f"   - {project['name']} (ID: {project['id']})")
    else:
        print(f"❌ Error obteniendo proyectos: {response.status_code} - {response.text}")
        return
    
    # 3. Verificar tareas
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tareas accesibles: {len(tasks)}")
        for task in tasks:
            print(f"   - {task['title']} (ID: {task['id']}, Project: {task['project_id']})")
    else:
        print(f"❌ Error obteniendo tareas: {response.status_code} - {response.text}")
    
    # 4. Verificar membresías de proyecto (si es admin)
    if user_info.get('role') == 'admin':
        print("\n🔧 Verificando membresías de proyecto (como admin):")
        for project in projects:
            response = requests.get(f"{BASE_URL}/projects/{project['id']}/members", headers=headers)
            if response.status_code == 200:
                members = response.json()
                print(f"   Proyecto '{project['name']}': {len(members)} miembros")
                for member in members:
                    print(f"     - {member.get('email', 'N/A')} (Role: {member.get('role', 'N/A')})")
            else:
                print(f"   ❌ Error obteniendo miembros del proyecto {project['id']}")

def main():
    print("🚀 Iniciando diagnóstico de acceso a tareas")
    
    # Usuarios de prueba
    test_users = [
        ("admin@example.com", "adminpass123"),
        ("user1@example.com", "userpass123"),
        ("user2@example.com", "userpass123")
    ]
    
    for email, password in test_users:
        debug_user_access(email, password)
        print("-" * 60)

if __name__ == "__main__":
    main()