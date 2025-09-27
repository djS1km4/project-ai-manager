import sqlite3

def update_tasks_status():
    conn = sqlite3.connect('project_manager.db')
    cursor = conn.cursor()

    # Ver tareas de los primeros 3 proyectos
    cursor.execute('SELECT id, title, status, project_id FROM tasks WHERE project_id IN (1, 2, 3) ORDER BY project_id, id')
    tasks = cursor.fetchall()

    print('=== TAREAS DE LOS PRIMEROS 3 PROYECTOS (ANTES) ===')
    for task in tasks:
        print(f'ID: {task[0]}, Título: {task[1]}, Estado: {task[2]}, Proyecto: {task[3]}')

    # Marcar algunas tareas como completadas
    # Proyecto 1: marcar la tarea como completada (100%)
    cursor.execute('UPDATE tasks SET status = "DONE" WHERE id = 1')
    
    # Proyecto 2: marcar 2 de 3 como completadas (66%)
    cursor.execute('UPDATE tasks SET status = "DONE" WHERE id IN (2, 3)')
    
    # Proyecto 3: marcar 1 de 4 como completada (25%)
    cursor.execute('UPDATE tasks SET status = "DONE" WHERE id = 5')

    conn.commit()

    print('\n=== TAREAS ACTUALIZADAS (DESPUÉS) ===')
    cursor.execute('SELECT id, title, status, project_id FROM tasks WHERE project_id IN (1, 2, 3) ORDER BY project_id, id')
    updated_tasks = cursor.fetchall()
    for task in updated_tasks:
        print(f'ID: {task[0]}, Título: {task[1]}, Estado: {task[2]}, Proyecto: {task[3]}')

    conn.close()
    print('\n✅ Tareas actualizadas correctamente')

if __name__ == "__main__":
    update_tasks_status()