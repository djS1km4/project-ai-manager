#!/usr/bin/env python3
"""
Script completo para probar múltiples ediciones consecutivas de proyectos
Verifica que todos los campos se guarden correctamente
"""
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

def login_as_admin():
    """Login as admin and return token"""
    login_data = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login exitoso como administrador")
        return token
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None

def get_project_by_id(token, project_id):
    """Get project details by ID"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error obteniendo proyecto: {response.status_code} - {response.text}")
        return None

def update_project(token, project_id, update_data):
    """Update project with given data"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(f"{BASE_URL}/projects/{project_id}", 
                          headers=headers, 
                          json=update_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error actualizando proyecto: {response.status_code} - {response.text}")
        return None

def test_multiple_consecutive_edits():
    """Test multiple consecutive edits on all project fields"""
    print("🧪 Iniciando prueba de múltiples ediciones consecutivas...")
    
    # Login
    token = login_as_admin()
    if not token:
        return False
    
    # Get first project
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/projects", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Error obteniendo proyectos: {response.status_code}")
        return False
    
    projects = response.json()
    if not projects:
        print("❌ No hay proyectos disponibles para probar")
        return False
    
    project = projects[0]
    project_id = project["id"]
    print(f"📋 Probando con proyecto: {project['name']} (ID: {project_id})")
    
    # Store original data
    original_data = get_project_by_id(token, project_id)
    if not original_data:
        return False
    
    print(f"📊 Datos originales:")
    print(f"   - Nombre: {original_data.get('name')}")
    print(f"   - Descripción: {original_data.get('description')}")
    print(f"   - Presupuesto: {original_data.get('budget')}")
    print(f"   - Fecha inicio: {original_data.get('start_date')}")
    print(f"   - Fecha fin: {original_data.get('end_date')}")
    print(f"   - Estado: {original_data.get('status')}")
    print(f"   - Prioridad: {original_data.get('priority')}")
    
    # Test data for multiple edits
    test_edits = [
        {
            "name": "PRUEBA EDIT 1 - Proyecto Actualizado",
            "description": "Descripción actualizada en la primera edición",
            "budget": 15000.50,
            "start_date": "2024-01-15T10:00:00",
            "end_date": "2024-06-15T18:00:00",
            "status": "in_progress",
            "priority": "high"
        },
        {
            "name": "PRUEBA EDIT 2 - Segundo Cambio",
            "description": "Segunda descripción modificada con más detalles",
            "budget": 25000.75,
            "start_date": "2024-02-01T09:30:00",
            "end_date": "2024-07-01T17:30:00",
            "status": "planning",
            "priority": "medium"
        },
        {
            "name": "PRUEBA EDIT 3 - Tercer Cambio",
            "description": "Tercera descripción con cambios importantes",
            "budget": 35000.99,
            "start_date": "2024-03-01T08:00:00",
            "end_date": "2024-08-01T16:00:00",
            "status": "completed",
            "priority": "low"
        },
        {
            "name": "PRUEBA EDIT 4 - Cuarto Cambio",
            "description": "Cuarta descripción final de pruebas",
            "budget": 45000.25,
            "start_date": "2024-04-01T11:00:00",
            "end_date": "2024-09-01T19:00:00",
            "status": "on_hold",
            "priority": "high"
        }
    ]
    
    # Perform multiple consecutive edits
    for i, edit_data in enumerate(test_edits, 1):
        print(f"\n🔄 EDICIÓN {i}:")
        print(f"   Enviando datos: {json.dumps(edit_data, indent=2)}")
        
        # Update project
        updated_project = update_project(token, project_id, edit_data)
        if not updated_project:
            print(f"❌ Falló la edición {i}")
            return False
        
        # Verify the update
        current_project = get_project_by_id(token, project_id)
        if not current_project:
            print(f"❌ No se pudo verificar la edición {i}")
            return False
        
        print(f"✅ Edición {i} aplicada. Verificando campos...")
        
        # Check each field
        errors = []
        
        if current_project.get('name') != edit_data['name']:
            errors.append(f"Nombre: esperado '{edit_data['name']}', obtenido '{current_project.get('name')}'")
        
        if current_project.get('description') != edit_data['description']:
            errors.append(f"Descripción: esperado '{edit_data['description']}', obtenido '{current_project.get('description')}'")
        
        if current_project.get('budget') != edit_data['budget']:
            errors.append(f"Presupuesto: esperado {edit_data['budget']}, obtenido {current_project.get('budget')}")
        
        if current_project.get('status') != edit_data['status']:
            errors.append(f"Estado: esperado '{edit_data['status']}', obtenido '{current_project.get('status')}'")
        
        if current_project.get('priority') != edit_data['priority']:
            errors.append(f"Prioridad: esperado '{edit_data['priority']}', obtenido '{current_project.get('priority')}'")
        
        # Check dates (convert to compare)
        if current_project.get('start_date'):
            current_start = current_project['start_date'][:19]  # Remove timezone info for comparison
            if current_start != edit_data['start_date']:
                errors.append(f"Fecha inicio: esperado '{edit_data['start_date']}', obtenido '{current_start}'")
        
        if current_project.get('end_date'):
            current_end = current_project['end_date'][:19]  # Remove timezone info for comparison
            if current_end != edit_data['end_date']:
                errors.append(f"Fecha fin: esperado '{edit_data['end_date']}', obtenido '{current_end}'")
        
        if errors:
            print(f"❌ ERRORES en edición {i}:")
            for error in errors:
                print(f"   - {error}")
            return False
        else:
            print(f"✅ Todos los campos de la edición {i} se guardaron correctamente")
            print(f"   - Nombre: {current_project.get('name')}")
            print(f"   - Descripción: {current_project.get('description')}")
            print(f"   - Presupuesto: {current_project.get('budget')}")
            print(f"   - Fecha inicio: {current_project.get('start_date')}")
            print(f"   - Fecha fin: {current_project.get('end_date')}")
            print(f"   - Estado: {current_project.get('status')}")
            print(f"   - Prioridad: {current_project.get('priority')}")
    
    # Restore original data
    print(f"\n🔄 Restaurando datos originales...")
    restore_data = {
        "name": original_data["name"],
        "description": original_data["description"],
        "budget": original_data["budget"],
        "start_date": original_data["start_date"],
        "end_date": original_data["end_date"],
        "status": original_data["status"],
        "priority": original_data["priority"]
    }
    
    restored_project = update_project(token, project_id, restore_data)
    if restored_project:
        print(f"✅ Datos originales restaurados correctamente")
    else:
        print(f"❌ Error restaurando datos originales")
    
    return True

if __name__ == "__main__":
    success = test_multiple_consecutive_edits()
    if success:
        print(f"\n🎉 PRUEBA EXITOSA: Todas las ediciones consecutivas funcionaron correctamente")
        print(f"✅ Todos los campos se guardan y persisten correctamente")
        print(f"✅ El problema de múltiples ediciones ha sido resuelto")
    else:
        print(f"\n❌ PRUEBA FALLIDA: Hay problemas con las ediciones consecutivas")
    
    print(f"\n📋 Resumen de la prueba:")
    print(f"   - Se probaron 4 ediciones consecutivas")
    print(f"   - Se verificaron todos los campos: nombre, descripción, presupuesto, fechas, estado, prioridad")
    print(f"   - Se restauraron los datos originales")