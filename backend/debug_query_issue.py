from app.database import get_db
from app.models.task import Task
from app.models.project import Project, ProjectMember
from app.models.user import User
from sqlalchemy.orm import Session
import traceback

def debug_query_issue():
    print("🔍 Debuggeando problema de consulta SQL...")
    
    db = next(get_db())
    
    try:
        # Obtener usuario admin
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            print("❌ Usuario admin no encontrado")
            return
        
        print(f"✅ Usuario admin encontrado: ID {admin_user.id}, is_admin: {admin_user.is_admin}")
        
        # Probar la consulta que está fallando para administradores
        print("\n🔍 Probando consulta de administrador...")
        try:
            # Esta es la consulta que está en TaskService para administradores
            query = db.query(Task).join(Project)
            
            print("   Ejecutando query.all()...")
            tasks = query.all()
            print(f"✅ Consulta exitosa: {len(tasks)} tareas encontradas")
            
        except Exception as e:
            print(f"❌ Error en consulta de administrador: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
        
        # Probar consulta alternativa sin join
        print("\n🔍 Probando consulta alternativa sin join...")
        try:
            tasks_no_join = db.query(Task).all()
            print(f"✅ Consulta sin join exitosa: {len(tasks_no_join)} tareas encontradas")
        except Exception as e:
            print(f"❌ Error en consulta sin join: {str(e)}")
        
        # Probar consulta con join explícito
        print("\n🔍 Probando consulta con join explícito...")
        try:
            tasks_explicit = db.query(Task).join(Project, Task.project_id == Project.id).all()
            print(f"✅ Consulta con join explícito exitosa: {len(tasks_explicit)} tareas encontradas")
        except Exception as e:
            print(f"❌ Error en consulta con join explícito: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
        
        # Verificar si hay problemas con las relaciones
        print("\n🔍 Verificando relaciones...")
        try:
            # Obtener una tarea y verificar sus relaciones
            task = db.query(Task).first()
            if task:
                print(f"   Tarea ID: {task.id}")
                print(f"   Proyecto ID: {task.project_id}")
                print(f"   Proyecto: {task.project.name if task.project else 'None'}")
            else:
                print("   No hay tareas en la base de datos")
        except Exception as e:
            print(f"❌ Error verificando relaciones: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_query_issue()