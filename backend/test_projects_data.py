import requests
import json

def test_projects_data():
    # Login
    login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
                                 json={'email': 'test@example.com', 'password': 'testpassword123'})
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get projects
        projects_response = requests.get('http://localhost:8000/api/v1/projects/', headers=headers)
        
        if projects_response.status_code == 200:
            projects = projects_response.json()
            print('=== DATOS DE PROYECTOS ===')
            
            for i, project in enumerate(projects[:3]):  # Solo los primeros 3
                print(f'Proyecto {i+1}: {project.get("name")}')
                print(f'  ID: {project.get("id")}')
                print(f'  task_count: {project.get("task_count")}')
                print(f'  completed_tasks: {project.get("completed_tasks")}')
                print(f'  progress_percentage: {project.get("progress_percentage")}')
                print(f'  progress: {project.get("progress")}')
                print(f'  status: {project.get("status")}')
                print('  Todas las claves:', list(project.keys()))
                print('---')
        else:
            print(f'Error en proyectos: {projects_response.status_code} - {projects_response.text}')
    else:
        print(f'Error en login: {login_response.status_code} - {login_response.text}')

if __name__ == "__main__":
    test_projects_data()