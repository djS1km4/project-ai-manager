#!/usr/bin/env python3
"""
Script to check database structure and users
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine

def check_database():
    """Check database structure and users"""
    conn = engine.connect()
    try:
        # Check tables
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        print("Tables:", tables)
        
        # Check if users table exists and has data
        if 'users' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"Users count: {user_count}")
            
            if user_count > 0:
                result = conn.execute(text("SELECT id, email, username, is_active FROM users LIMIT 5"))
                users = result.fetchall()
                print("Sample users:")
                for user in users:
                    print(f"  ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Active: {user[3]}")
        else:
            print("Users table does not exist")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database()