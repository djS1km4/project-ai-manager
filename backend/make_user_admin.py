#!/usr/bin/env python3
"""
Script para hacer admin al usuario de prueba y probar el endpoint de usuarios
"""

import sqlite3
import os

def make_user_admin():
    """Hacer admin al usuario de prueba"""
    db_path = "project_manager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar usuario actual
        cursor.execute("SELECT id, email, username, is_admin FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        
        if not user:
            print("❌ Usuario test@example.com no encontrado")
            return False
        
        user_id, email, username, is_admin = user
        print(f"👤 Usuario encontrado: {username} ({email})")
        print(f"   ID: {user_id}, Admin: {bool(is_admin)}")
        
        if is_admin:
            print("✅ El usuario ya es administrador")
            return True
        
        # Hacer admin al usuario
        cursor.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
        conn.commit()
        
        # Verificar cambio
        cursor.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
        new_admin_status = cursor.fetchone()[0]
        
        if new_admin_status:
            print("✅ Usuario actualizado a administrador exitosamente")
            return True
        else:
            print("❌ Error al actualizar usuario")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

def main():
    """Función principal"""
    print("🔧 Haciendo admin al usuario de prueba")
    print("=" * 50)
    
    success = make_user_admin()
    
    if success:
        print("\n✅ Usuario actualizado. Ahora puedes probar el endpoint de usuarios.")
    else:
        print("\n❌ Error al actualizar usuario.")

if __name__ == "__main__":
    main()