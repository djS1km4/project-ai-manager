#!/usr/bin/env python3
"""
Script para verificar las credenciales de usuarios en la base de datos
"""

import sqlite3
import os

def check_user_credentials():
    """Verificar credenciales de usuarios"""
    db_path = "project_manager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todos los usuarios
        cursor.execute("""
            SELECT id, email, username, full_name, is_admin, is_active 
            FROM users 
            ORDER BY id
        """)
        
        users = cursor.fetchall()
        
        print(f"👥 Total de usuarios: {len(users)}")
        print("\n📋 Lista de usuarios:")
        
        for user_id, email, username, full_name, is_admin, is_active in users:
            admin_status = "Admin" if is_admin else "Regular"
            active_status = "Activo" if is_active else "Inactivo"
            print(f"   ID: {user_id} | {email} | {username} | {admin_status} | {active_status}")
        
        print("\n🔑 Usuarios regulares activos para pruebas:")
        for user_id, email, username, full_name, is_admin, is_active in users:
            if not is_admin and is_active:
                print(f"   - {email} (ID: {user_id})")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_user_credentials()