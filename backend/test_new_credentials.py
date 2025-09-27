#!/usr/bin/env python3
"""
Script para probar las nuevas credenciales de acceso
"""

import requests
import json

def test_login(email, password, user_type):
    """Probar login con credenciales específicas"""
    
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/api/v1/auth/login"
    
    # Datos de login
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        print(f"\n🔐 Probando login para {user_type}:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
        # Hacer request de login
        response = requests.post(
            login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            token_type = token_data.get("token_type", "bearer")
            
            print(f"✅ Login exitoso para {user_type}")
            print(f"   Token Type: {token_type}")
            print(f"   Access Token: {access_token[:50]}...")
            
            # Probar acceso a endpoint protegido
            headers = {"Authorization": f"{token_type} {access_token}"}
            me_response = requests.get(f"{base_url}/api/v1/auth/me", headers=headers)
            
            if me_response.status_code == 200:
                user_info = me_response.json()
                print(f"   Usuario: {user_info.get('username')}")
                print(f"   Email: {user_info.get('email')}")
                print(f"   Admin: {user_info.get('is_admin')}")
                print(f"   Activo: {user_info.get('is_active')}")
            else:
                print(f"❌ Error al obtener info del usuario: {me_response.status_code}")
                
            return True
            
        else:
            print(f"❌ Error en login para {user_type}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión para {user_type}: {e}")
        return False

def main():
    """Función principal para probar todas las credenciales"""
    
    print("🚀 Probando nuevas credenciales de acceso")
    print("=" * 50)
    
    # Credenciales a probar
    credentials = [
        {
            "email": "test@example.com",
            "password": "testpassword123",
            "type": "Administrador"
        },
        {
            "email": "usuario@example.com", 
            "password": "usuario123",
            "type": "Usuario Regular"
        }
    ]
    
    results = []
    
    for cred in credentials:
        success = test_login(cred["email"], cred["password"], cred["type"])
        results.append({
            "type": cred["type"],
            "email": cred["email"],
            "success": success
        })
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    for result in results:
        status = "✅ EXITOSO" if result["success"] else "❌ FALLIDO"
        print(f"{result['type']}: {status}")
        print(f"   Email: {result['email']}")
    
    print("\n🎯 Credenciales listas para usar:")
    print("-" * 30)
    for cred in credentials:
        print(f"{cred['type']}:")
        print(f"   Email: {cred['email']}")
        print(f"   Password: {cred['password']}")
        print()

if __name__ == "__main__":
    main()