#!/usr/bin/env python3
"""
Script para probar la API de proyectos directamente
"""
import requests
import json

def test_login_and_projects():
    """Probar login y obtener proyectos"""
    base_url = "http://localhost:8001/api/v1"
    
    # 1. Probar login
    print("🔐 Probando login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Status login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ Login exitoso. Token obtenido.")
            
            # 2. Probar obtener proyectos
            print("\n📁 Probando obtener proyectos...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            projects_response = requests.get(f"{base_url}/projects/", headers=headers)
            print(f"Status proyectos: {projects_response.status_code}")
            
            if projects_response.status_code == 200:
                projects = projects_response.json()
                print(f"✅ Proyectos obtenidos: {len(projects)} proyectos")
                
                # Mostrar algunos proyectos
                for i, project in enumerate(projects[:5]):
                    print(f"  {i+1}. {project.get('name')} (Estado: {project.get('status')})")
                
                if len(projects) > 5:
                    print(f"  ... y {len(projects) - 5} proyectos más")
                    
            else:
                print(f"❌ Error al obtener proyectos: {projects_response.text}")
                
        else:
            print(f"❌ Error en login: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está el backend ejecutándose en puerto 8001?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_login_and_projects()