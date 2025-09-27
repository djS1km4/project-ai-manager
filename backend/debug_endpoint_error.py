import requests
import json
import traceback

def test_tasks_endpoint():
    base_url = "http://localhost:8001"
    
    # Credenciales
    admin_credentials = {"email": "admin@example.com", "password": "adminpassword123"}
    regular_credentials = {"email": "test@example.com", "password": "testpassword123"}
    
    print("🔍 Probando endpoint de tareas con diferentes usuarios...")
    
    # Función para hacer login
    def login(credentials, user_type):
        try:
            response = requests.post(
                f"{base_url}/api/v1/auth/login",
                json=credentials,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                print(f"✅ Login exitoso para {user_type}: {credentials['email']}")
                return token
            else:
                print(f"❌ Error en login para {user_type}: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Excepción en login para {user_type}: {str(e)}")
            return None
    
    # Función para probar endpoint de tareas
    def test_tasks(token, user_type):
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print(f"\n🔍 Probando /api/v1/tasks para {user_type}...")
            response = requests.get(f"{base_url}/api/v1/tasks", headers=headers)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Éxito: {len(data)} tareas obtenidas")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Respuesta completa: {response.text}")
                
                # Intentar parsear como JSON para ver el error
                try:
                    error_data = response.json()
                    print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Error no es JSON válido")
                
                return False
                
        except Exception as e:
            print(f"❌ Excepción al probar endpoint para {user_type}: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    # Probar con usuario regular
    print("\n" + "="*50)
    print("PROBANDO CON USUARIO REGULAR")
    print("="*50)
    regular_token = login(regular_credentials, "usuario regular")
    if regular_token:
        test_tasks(regular_token, "usuario regular")
    
    # Probar con administrador
    print("\n" + "="*50)
    print("PROBANDO CON ADMINISTRADOR")
    print("="*50)
    admin_token = login(admin_credentials, "administrador")
    if admin_token:
        test_tasks(admin_token, "administrador")
    
    print("\n🔍 Pruebas completadas.")

if __name__ == "__main__":
    test_tasks_endpoint()