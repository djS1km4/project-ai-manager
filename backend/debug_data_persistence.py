#!/usr/bin/env python3
"""
Script para verificar la persistencia de datos en actualizaciones de proyectos
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
PROJECTS_URL = f"{BASE_URL}/api/v1/projects"

def login():
    """Iniciar sesión como administrador"""
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    print("🔐 Iniciando sesión como administrador...")
    response = requests.post(LOGIN_URL, json=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Sesión iniciada exitosamente")
        return token
    else:
        print(f"❌ Error al iniciar sesión: {response.status_code}")
        print(f"❌ Respuesta: {response.text}")
        return None

def get_project_details(token, project_id):
    """Obtener detalles completos de un proyecto"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{PROJECTS_URL}/{project_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al obtener proyecto {project_id}: {response.status_code}")
        return None

def update_project_with_all_fields(token, project_id, test_data):
    """Actualizar un proyecto con todos los campos"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{PROJECTS_URL}/{project_id}"
    
    print(f"🔄 Enviando datos de actualización:")
    print(f"   📤 Datos enviados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    response = requests.put(url, json=test_data, headers=headers)
    
    if response.status_code == 200:
        updated_data = response.json()
        print(f"✅ Proyecto actualizado exitosamente")
        print(f"   📥 Datos recibidos: {json.dumps(updated_data, indent=2, ensure_ascii=False)}")
        return updated_data
    else:
        print(f"❌ Error al actualizar proyecto: {response.status_code}")
        print(f"❌ Respuesta: {response.text}")
        return None

def compare_data(sent_data, received_data, field_name):
    """Comparar datos enviados vs recibidos"""
    sent_value = sent_data.get(field_name)
    received_value = received_data.get(field_name)
    
    if sent_value == received_value:
        print(f"   ✅ {field_name}: {sent_value} → {received_value}")
        return True
    else:
        print(f"   ❌ {field_name}: {sent_value} → {received_value} (NO COINCIDE)")
        return False

def test_data_persistence():
    """Probar la persistencia de todos los campos"""
    print("🧪 Iniciando prueba de persistencia de datos")
    print("=" * 60)
    
    # Iniciar sesión
    token = login()
    if not token:
        return
    
    # Obtener lista de proyectos
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROJECTS_URL, headers=headers)
    
    if response.status_code != 200:
        print("❌ No se pudieron obtener los proyectos")
        return
    
    projects = response.json()
    if not projects:
        print("❌ No hay proyectos para probar")
        return
    
    # Seleccionar el primer proyecto
    test_project = projects[0]
    project_id = test_project["id"]
    
    print(f"\n🎯 Proyecto seleccionado para pruebas:")
    print(f"   ID: {project_id}")
    print(f"   Nombre: {test_project.get('name', 'N/A')}")
    
    # Obtener datos originales
    print(f"\n📋 Datos originales del proyecto:")
    original_data = get_project_details(token, project_id)
    if not original_data:
        return
    
    for key, value in original_data.items():
        print(f"   {key}: {value}")
    
    # Preparar datos de prueba con todos los campos
    today = datetime.now()
    future_date = today + timedelta(days=30)
    
    test_updates = [
        {
            "name": f"Proyecto Actualizado - Test 1",
            "description": "Descripción de prueba con caracteres especiales: áéíóú ñ",
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": future_date.strftime("%Y-%m-%d"),
            "budget": 15000.50,
            "status": "active"
        },
        {
            "name": f"Proyecto Actualizado - Test 2",
            "description": "Segunda descripción de prueba",
            "start_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (future_date + timedelta(days=10)).strftime("%Y-%m-%d"),
            "budget": 25000.75,
            "status": "on_hold"
        },
        {
            "name": f"Proyecto Actualizado - Test 3",
            "description": "Tercera descripción con más texto para verificar que se guarda correctamente",
            "start_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (future_date + timedelta(days=20)).strftime("%Y-%m-%d"),
            "budget": 35000.99,
            "status": "planning"
        }
    ]
    
    # Realizar múltiples actualizaciones y verificar persistencia
    for i, test_data in enumerate(test_updates, 1):
        print(f"\n{'='*20} PRUEBA {i} {'='*20}")
        
        # Actualizar proyecto
        updated_data = update_project_with_all_fields(token, project_id, test_data)
        if not updated_data:
            print(f"❌ Falló la actualización {i}")
            continue
        
        # Verificar que los datos enviados coincidan con los recibidos
        print(f"\n🔍 Verificación de datos (Actualización {i}):")
        fields_to_check = ["name", "description", "start_date", "end_date", "budget", "status"]
        
        all_correct = True
        for field in fields_to_check:
            if not compare_data(test_data, updated_data, field):
                all_correct = False
        
        if all_correct:
            print(f"✅ Todos los campos se guardaron correctamente en actualización {i}")
        else:
            print(f"❌ Algunos campos no se guardaron correctamente en actualización {i}")
        
        # Pequeña pausa entre actualizaciones
        time.sleep(1)
        
        # Verificar persistencia obteniendo los datos nuevamente
        print(f"\n🔄 Verificando persistencia en base de datos...")
        fresh_data = get_project_details(token, project_id)
        if fresh_data:
            print(f"📊 Datos desde base de datos:")
            persistence_correct = True
            for field in fields_to_check:
                if not compare_data(test_data, fresh_data, field):
                    persistence_correct = False
            
            if persistence_correct:
                print(f"✅ Persistencia verificada correctamente")
            else:
                print(f"❌ Problemas de persistencia detectados")
        
        print(f"\n" + "-"*50)
    
    # Restaurar datos originales
    print(f"\n🔄 Restaurando datos originales...")
    restore_data = {
        "name": original_data.get("name", "Proyecto Original"),
        "description": original_data.get("description", ""),
        "start_date": original_data.get("start_date"),
        "end_date": original_data.get("end_date"),
        "budget": original_data.get("budget", 0),
        "status": original_data.get("status", "planning")
    }
    
    final_update = update_project_with_all_fields(token, project_id, restore_data)
    if final_update:
        print("✅ Datos originales restaurados")
    else:
        print("❌ Error al restaurar datos originales")

if __name__ == "__main__":
    test_data_persistence()