#!/usr/bin/env python3
"""
Test script to debug AI Insights endpoints
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "testpassword123"

def get_access_token():
    """Get access token"""
    print("🔐 Obteniendo token de acceso...")
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Token obtenido exitosamente")
            return token
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión en login: {e}")
        return None

def get_projects(token):
    """Get user projects"""
    print("\n📋 Obteniendo proyectos del usuario...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Se encontraron {len(projects)} proyectos")
            return projects
        else:
            print(f"❌ Error obteniendo proyectos: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión obteniendo proyectos: {e}")
        return []

def test_ai_endpoint(endpoint, token, project_id, method="GET", data=None):
    """Test a specific AI endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/ai-insights/{endpoint}".replace("{project_id}", str(project_id))
    
    print(f"\n🧪 Probando endpoint: {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data or {})
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta exitosa")
            print(f"📄 Contenido: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
            return True, result
        else:
            print(f"❌ Error: {response.text}")
            return False, response.text
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False, str(e)

def check_openai_config():
    """Check OpenAI configuration"""
    print("\n🔧 Verificando configuración de OpenAI...")
    
    # Check if .env file exists
    env_path = ".env"
    if os.path.exists(env_path):
        print("✅ Archivo .env encontrado")
        with open(env_path, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=your-openai-api-key-here" in content:
                print("⚠️  OPENAI_API_KEY no está configurada (valor por defecto)")
                return False
            elif "OPENAI_API_KEY=" in content:
                print("✅ OPENAI_API_KEY está configurada")
                return True
            else:
                print("❌ OPENAI_API_KEY no encontrada en .env")
                return False
    else:
        print("❌ Archivo .env no encontrado")
        return False

def main():
    print("🚀 Iniciando pruebas de endpoints de IA...")
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"👤 Usuario: {EMAIL}")
    
    # Check OpenAI configuration
    openai_configured = check_openai_config()
    
    # Get access token
    token = get_access_token()
    if not token:
        print("❌ No se pudo obtener el token. Terminando pruebas.")
        return
    
    # Get projects
    projects = get_projects(token)
    if not projects:
        print("❌ No se encontraron proyectos. Terminando pruebas.")
        return
    
    # Use first project for testing
    project_id = projects[0]["id"]
    project_name = projects[0]["name"]
    print(f"\n🎯 Usando proyecto: {project_name} (ID: {project_id})")
    
    # Test AI endpoints
    ai_endpoints = [
        ("analyze-project/{project_id}", "POST", {"analysis_type": "comprehensive"}),
        ("analyze-project/{project_id}", "POST", {"analysis_type": "risk"}),
        ("analyze-project/{project_id}", "POST", {"analysis_type": "progress"}),
        ("analyze-project/{project_id}", "POST", {"analysis_type": "team"}),
        ("project/{project_id}/risk-assessment", "GET", None),
        ("project/{project_id}/progress-prediction", "GET", None),
        ("project/{project_id}/team-performance", "GET", None),
    ]
    
    results = {}
    
    for endpoint, method, data in ai_endpoints:
        success, result = test_ai_endpoint(endpoint, token, project_id, method, data)
        results[endpoint] = {"success": success, "result": result}
    
    # Summary
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    print(f"🔧 OpenAI configurado: {'✅ Sí' if openai_configured else '❌ No'}")
    print(f"🔐 Autenticación: {'✅ Exitosa' if token else '❌ Fallida'}")
    print(f"📋 Proyectos encontrados: {len(projects)}")
    
    print("\n🧪 Resultados de endpoints de IA:")
    for endpoint, result in results.items():
        status = "✅ Exitoso" if result["success"] else "❌ Fallido"
        print(f"  {endpoint}: {status}")
    
    successful_tests = sum(1 for r in results.values() if r["success"])
    total_tests = len(results)
    print(f"\n📈 Pruebas exitosas: {successful_tests}/{total_tests}")
    
    if not openai_configured:
        print("\n⚠️  RECOMENDACIÓN: Configurar OPENAI_API_KEY en el archivo .env para habilitar funcionalidades de IA")
    
    if successful_tests == 0:
        print("\n🔍 DIAGNÓSTICO: Todos los endpoints de IA fallaron. Posibles causas:")
        print("   1. OPENAI_API_KEY no configurada")
        print("   2. Problemas de conectividad con OpenAI")
        print("   3. Errores en el servicio de IA")
        print("   4. Datos insuficientes en el proyecto")

if __name__ == "__main__":
    main()