#!/usr/bin/env python3
"""
Script para corregir las credenciales del administrador
"""

import sqlite3
import os
from app.services.auth_service import AuthService

def fix_admin_credentials():
    """Corregir las credenciales del administrador"""
    db_path = "project_manager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Corrigiendo credenciales del administrador...")
        
        # Verificar usuario admin actual
        cursor.execute("SELECT id, email, username, is_admin FROM users WHERE email = ?", ("admin@example.com",))
        admin_user = cursor.fetchone()
        
        if admin_user:
            admin_id, email, username, is_admin = admin_user
            print(f"   📋 Usuario admin encontrado: ID {admin_id}, Email: {email}")
            
            # Actualizar contraseña del administrador
            new_password_hash = AuthService.get_password_hash("adminpassword123")
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE email = ?",
                (new_password_hash, "admin@example.com")
            )
            
            # Asegurar que sea administrador
            cursor.execute(
                "UPDATE users SET is_admin = 1 WHERE email = ?",
                ("admin@example.com",)
            )
            
            print(f"   ✅ Contraseña actualizada para admin@example.com")
            print(f"   🔑 Nueva contraseña: adminpassword123")
        else:
            print("   ❌ Usuario admin@example.com no encontrado")
            return
        
        # Verificar usuario regular
        cursor.execute("SELECT id, email, username, is_admin FROM users WHERE email = ?", ("test@example.com",))
        regular_user = cursor.fetchone()
        
        if regular_user:
            user_id, email, username, is_admin = regular_user
            print(f"   📋 Usuario regular encontrado: ID {user_id}, Email: {email}")
            
            # Actualizar contraseña del usuario regular
            new_password_hash = AuthService.get_password_hash("testpassword123")
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE email = ?",
                (new_password_hash, "test@example.com")
            )
            
            # Asegurar que NO sea administrador
            cursor.execute(
                "UPDATE users SET is_admin = 0 WHERE email = ?",
                ("test@example.com",)
            )
            
            print(f"   ✅ Contraseña actualizada para test@example.com")
            print(f"   🔑 Contraseña: testpassword123")
        else:
            print("   ❌ Usuario test@example.com no encontrado")
        
        conn.commit()
        
        print("\n📊 Resumen de credenciales corregidas:")
        print("   👤 Usuario regular: test@example.com / testpassword123")
        print("   🔐 Administrador: admin@example.com / adminpassword123")
        
        # Verificar cambios
        cursor.execute("SELECT email, username, is_admin FROM users WHERE email IN (?, ?)", 
                      ("test@example.com", "admin@example.com"))
        users = cursor.fetchall()
        
        print("\n✅ Verificación de usuarios:")
        for email, username, is_admin in users:
            role = "Administrador" if is_admin else "Usuario regular"
            print(f"   - {email} ({username}): {role}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_admin_credentials()