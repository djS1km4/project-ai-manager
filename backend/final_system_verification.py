#!/usr/bin/env python3
"""
Verificación final del sistema completo
"""

import sqlite3
import os
import requests
import json

BASE_URL = "http://localhost:8001"

def check_database_integrity():
    """Verificar integridad de la base de datos"""
    print("🔍 Verificando integridad de la base de datos...")
    
    db_path = "project_manager.db"
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar proyectos huérfanos
        cursor.execute("SELECT COUNT(*) FROM projects WHERE owner_id IS NULL")
        orphan_projects = cursor.fetchone()[0]
        
        # Verificar usuarios administradores
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = cursor.fetchone()[0]
        
        # Contar totales
        cursor.execute("SELECT COUNT(*) FROM projects")
        total_projects = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        print(f"   📊 Proyectos: {total_projects} (Huérfanos: {orphan_projects})")
        print(f"   📋 Tareas: {total_tasks}")
        print(f"   👥 Usuarios: {total_users} (Admins: {admin_count})")
        
        if orphan_projects == 0 and admin_count >= 2:
            print("   ✅ Integridad de base de datos: OK")
            return True
        else:
            print("   ❌ Problemas de integridad detectados")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando base de datos: {e}")
        return False
    finally:
        conn.close()

def test_api_endpoints():
    """Probar endpoints principales de la API"""
    print("\n🌐 Verificando endpoints de la API...")
    
    try:
        # Test de salud
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint de salud: OK")
        else:
            print("   ❌ Endpoint de salud: FALLO")
            return False
            
        # Test de login de administrador
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword123"
        }, timeout=5)
        
        if login_response.status_code == 200:
            print("   ✅ Login de administrador: OK")
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test de endpoints de admin
            admin_projects = requests.get(f"{BASE_URL}/api/v1/admin/projects", headers=headers, timeout=5)
            admin_tasks = requests.get(f"{BASE_URL}/api/v1/admin/tasks", headers=headers, timeout=5)
            
            if admin_projects.status_code == 200 and admin_tasks.status_code == 200:
                print("   ✅ Endpoints de administración: OK")
                return True
            else:
                print("   ❌ Endpoints de administración: FALLO")
                return False
        else:
            print("   ❌ Login de administrador: FALLO")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error conectando a la API: {e}")
        return False

def verify_admin_functionality():
    """Verificar funcionalidad específica de administración"""
    print("\n🔐 Verificando funcionalidad de administración...")
    
    try:
        # Login como admin
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        if login_response.status_code != 200:
            print("   ❌ No se pudo autenticar como administrador")
            return False
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Verificar acceso a todos los proyectos
        projects_response = requests.get(f"{BASE_URL}/api/v1/projects", headers=headers)
        admin_projects_response = requests.get(f"{BASE_URL}/api/v1/admin/projects", headers=headers)
        
        if projects_response.status_code == 200 and admin_projects_response.status_code == 200:
            regular_projects = len(projects_response.json())
            admin_projects = len(admin_projects_response.json())
            
            print(f"   📁 Proyectos visibles (regular): {regular_projects}")
            print(f"   📁 Proyectos visibles (admin): {admin_projects}")
            
            if admin_projects >= regular_projects:
                print("   ✅ Acceso de administrador a proyectos: OK")
            else:
                print("   ❌ Acceso de administrador limitado")
                return False
        
        # Verificar acceso a todas las tareas
        tasks_response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
        admin_tasks_response = requests.get(f"{BASE_URL}/api/v1/admin/tasks", headers=headers)
        
        if tasks_response.status_code == 200 and admin_tasks_response.status_code == 200:
            regular_tasks = len(tasks_response.json())
            admin_tasks = len(admin_tasks_response.json())
            
            print(f"   📋 Tareas visibles (regular): {regular_tasks}")
            print(f"   📋 Tareas visibles (admin): {admin_tasks}")
            
            if admin_tasks >= regular_tasks:
                print("   ✅ Acceso de administrador a tareas: OK")
                return True
            else:
                print("   ❌ Acceso de administrador a tareas limitado")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando funcionalidad de admin: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 50)
    
    results = []
    
    # Verificar base de datos
    db_ok = check_database_integrity()
    results.append(("Base de datos", db_ok))
    
    # Verificar API
    api_ok = test_api_endpoints()
    results.append(("API endpoints", api_ok))
    
    # Verificar administración
    admin_ok = verify_admin_functionality()
    results.append(("Funcionalidad admin", admin_ok))
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    
    all_ok = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not result:
            all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("   Todos los componentes están operativos.")
        print("   El sistema de administración está listo para usar.")
    else:
        print("⚠️  SISTEMA CON PROBLEMAS")
        print("   Revisar los fallos reportados arriba.")
    
    return all_ok

if __name__ == "__main__":
    main()