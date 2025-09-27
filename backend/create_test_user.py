#!/usr/bin/env python3
"""
Script to create a test user for debugging
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine
from passlib.context import CryptContext

def create_test_user():
    """Create a test user"""
    conn = engine.connect()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    try:
        # Delete existing test user
        conn.execute(text("DELETE FROM users WHERE email = 'test@example.com'"))
        conn.commit()
        
        # Create new user with proper password hash
        email = "test@example.com"
        username = "testuser"
        full_name = "Test User"
        password = "testpassword123"
        hashed_password = pwd_context.hash(password)
        
        # Insert user
        conn.execute(text("""
            INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin, created_at, updated_at)
            VALUES (:email, :username, :full_name, :hashed_password, 1, 0, datetime('now'), datetime('now'))
        """), {
            "email": email,
            "username": username,
            "full_name": full_name,
            "hashed_password": hashed_password
        })
        conn.commit()
        
        print(f"User created successfully:")
        print(f"  Email: {email}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        
        # Verify password works
        is_valid = pwd_context.verify(password, hashed_password)
        print(f"  Password verification: {is_valid}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_test_user()