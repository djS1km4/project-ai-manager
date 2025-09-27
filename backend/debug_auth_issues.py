#!/usr/bin/env python3
"""
Script para debuggear problemas de autenticación y errores 403
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001/api/v1"

def test_login_and_auth():
    """Probar login y autenticación"""
    print("🔐 Testing Authentication Issues")
    print("=" * 50)
    
    # Test 1: Login con cuenta de prueba
    print("\n1️⃣ Testing login with test account")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return None
    
    token_data = response.json()
    token = token_data["access_token"]
    user = token_data["user"]
    
    print(f"✅ Login successful")
    print(f"   User: {user['full_name']} ({user['email']})")
    print(f"   Token length: {len(token)}")
    print(f"   Response keys: {list(token_data.keys())}")
    if "expires_in" in token_data:
        print(f"   Token expires in: {token_data['expires_in']} seconds")
    
    # Test 2: Verificar token inmediatamente
    print("\n2️⃣ Testing immediate token verification")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Auth/me Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Token verification successful")
    else:
        print(f"❌ Token verification failed: {response.text}")
        return None
    
    # Test 3: Probar endpoints de tareas
    print("\n3️⃣ Testing tasks endpoints")
    
    # Get tasks
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"GET /tasks Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tasks retrieved: {len(tasks)} tasks")
    elif response.status_code == 403:
        print(f"❌ 403 Forbidden on tasks: {response.text}")
    else:
        print(f"❌ Error getting tasks: {response.status_code} - {response.text}")
    
    # Get projects (para comparar)
    response = requests.get(f"{BASE_URL}/projects/", headers=headers)
    print(f"GET /projects Status: {response.status_code}")
    
    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Projects retrieved: {len(projects)} projects")
    elif response.status_code == 403:
        print(f"❌ 403 Forbidden on projects: {response.text}")
    else:
        print(f"❌ Error getting projects: {response.status_code} - {response.text}")
    
    # Test 4: Crear una tarea simple
    print("\n4️⃣ Testing task creation")
    
    # Primero obtener un proyecto para usar
    if 'projects' in locals() and len(projects) > 0:
        project_id = projects[0]['id']
        print(f"Using project ID: {project_id}")
        
        task_data = {
            "title": "Test Task Auth Debug",
            "project_id": project_id,
            "priority": "medium",
            "status": "todo"
        }
        
        response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
        print(f"POST /tasks Status: {response.status_code}")
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Task created: {task['title']} (ID: {task['id']})")
        elif response.status_code == 403:
            print(f"❌ 403 Forbidden on task creation: {response.text}")
        elif response.status_code == 422:
            print(f"❌ 422 Validation error: {response.text}")
        else:
            print(f"❌ Error creating task: {response.status_code} - {response.text}")
    else:
        print("❌ No projects available for testing task creation")
    
    # Test 5: Probar con múltiples requests rápidos
    print("\n5️⃣ Testing rapid requests (simulating frontend behavior)")
    
    for i in range(5):
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Request {i+1}: {response.status_code}")
        if response.status_code != 200:
            print(f"   Error: {response.text}")
        time.sleep(0.1)  # Small delay
    
    # Test 6: Verificar token después de un tiempo
    print("\n6️⃣ Testing token after delay")
    time.sleep(2)
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Auth/me after delay: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Token failed after delay: {response.text}")
    else:
        print("✅ Token still valid after delay")
    
    return token

def test_new_user_creation():
    """Probar creación de nuevo usuario"""
    print("\n\n👤 Testing New User Creation")
    print("=" * 50)
    
    # Crear usuario nuevo
    timestamp = int(time.time())
    new_user_data = {
        "email": f"testuser{timestamp}@example.com",
        "username": f"testuser{timestamp}",
        "full_name": f"Test User {timestamp}",
        "password": "newuserpassword123"
    }
    
    print(f"Creating user: {new_user_data['full_name']} ({new_user_data['email']})")
    
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user_data)
    print(f"Registration Status: {response.status_code}")
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ User created successfully")
        print(f"   ID: {user_data['id']}")
        print(f"   Name: {user_data['full_name']}")
        print(f"   Email: {user_data['email']}")
        
        # Probar login inmediato
        print("\n🔐 Testing immediate login with new user")
        login_data = {
            "email": new_user_data["email"],
            "password": new_user_data["password"]
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ New user login successful")
            print(f"   Token length: {len(token_data['access_token'])}")
            
            # Probar acceso a tareas con nuevo usuario
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
            print(f"Tasks access with new user: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ New user can access tasks")
            else:
                print(f"❌ New user cannot access tasks: {response.text}")
        else:
            print(f"❌ New user login failed: {response.text}")
    else:
        print(f"❌ User creation failed: {response.text}")

if __name__ == "__main__":
    try:
        token = test_login_and_auth()
        test_new_user_creation()
        
        print("\n\n📋 Summary")
        print("=" * 50)
        print("Check the output above for any 403 errors or authentication issues.")
        print("Pay special attention to:")
        print("- Token verification failures")
        print("- 403 errors on tasks vs projects")
        print("- Rapid request failures")
        print("- New user authentication issues")
        
    except Exception as e:
        print(f"❌ Script error: {e}")
        import traceback
        traceback.print_exc()