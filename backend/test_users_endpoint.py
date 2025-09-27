#!/usr/bin/env python3
"""
Script para probar el endpoint de usuarios después de corregir el error del atributo 'role'
"""

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def login():
    """Login para obtener token de acceso"""
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    print("🔐 Iniciando sesión...")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login exitoso")
        return data["access_token"]
    else:
        print(f"❌ Error en login: {response.text}")
        return None

def get_users(token):
    """Obtener lista de usuarios"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📥 GET /auth/users")
    response = requests.get(f"{BASE_URL}/auth/users", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Usuarios obtenidos: {len(users)}")
        for user in users:
            print(f"  - {user['full_name']} (ID: {user['id']}, Email: {user['email']}, Admin: {user['is_admin']})")
        return True
    else:
        print(f"❌ Error obteniendo usuarios: {response.text}")
        return False

def main():
    """Función principal"""
    print("🧪 Probando endpoint de usuarios después de corrección")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        return
    
    # Probar obtener usuarios
    success = get_users(token)
    
    if success:
        print("\n✅ Prueba del endpoint de usuarios completada exitosamente")
    else:
        print("\n❌ Prueba del endpoint de usuarios falló")

if __name__ == "__main__":
    main()