#!/usr/bin/env python3
"""
Script para crear usuarios de prueba para testing de aislamiento de datos
"""

import sqlite3
from passlib.context import CryptContext

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_users():
    """Crear usuarios de prueba en la base de datos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('project_manager.db')
    cursor = conn.cursor()
    
    # Usuarios de prueba
    test_users = [
        {
            'email': 'admin@example.com',
            'username': 'admin',
            'full_name': 'Administrator',
            'password': 'adminpass123',
            'is_admin': 1
        },
        {
            'email': 'user1@example.com',
            'username': 'user1',
            'full_name': 'User One',
            'password': 'userpass123',
            'is_admin': 0
        },
        {
            'email': 'user2@example.com',
            'username': 'user2',
            'full_name': 'User Two',
            'password': 'userpass123',
            'is_admin': 0
        }
    ]
    
    for user in test_users:
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM users WHERE email = ?", (user['email'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"Usuario {user['email']} ya existe, saltando...")
            continue
        
        # Hash de la contraseña
        hashed_password = pwd_context.hash(user['password'])
        
        # Insertar usuario
        cursor.execute("""
            INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin)
            VALUES (?, ?, ?, ?, 1, ?)
        """, (user['email'], user['username'], user['full_name'], hashed_password, user['is_admin']))
        
        print(f"✅ Usuario creado: {user['email']} (admin: {bool(user['is_admin'])})")
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print("\n🎉 Usuarios de prueba creados exitosamente!")

if __name__ == "__main__":
    create_test_users()