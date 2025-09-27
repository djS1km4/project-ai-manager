from app.database import get_db
from app.services.task_service import TaskService
from app.services.auth_service import AuthService
from app.models.user import User
from sqlalchemy.orm import Session
import traceback

def debug_endpoint_flow():
    print("🔍 Simulando flujo completo del endpoint de tareas...")
    
    db = next(get_db())
    
    try:
        # Simular autenticación del administrador
        print("\n1️⃣ Simulando autenticación...")
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            print("❌ Usuario admin no encontrado")
            return
        
        print(f"✅ Usuario admin: ID {admin_user.id}, is_admin: {admin_user.is_admin}")
        
        # Simular llamada al TaskService exactamente como en el endpoint
        print("\n2️⃣ Simulando llamada a TaskService.get_tasks...")
        task_service = TaskService()
        
        try:
            # Estos son los parámetros por defecto del endpoint
            tasks = task_service.get_tasks(
                db=db,
                user_id=admin_user.id,
                project_id=None,
                assignee_id=None,
                status=None,
                priority=None,
                search=None,
                due_date_from=None,
                due_date_to=None,
                skip=0,
                limit=100
            )
            print(f"✅ TaskService.get_tasks exitoso: {len(tasks)} tareas")
            
            # Verificar que las tareas se pueden serializar
            print("\n3️⃣ Verificando serialización de tareas...")
            for i, task in enumerate(tasks[:3]):  # Solo las primeras 3 para no saturar
                try:
                    print(f"   Tarea {i+1}: ID={task.id}, título='{task.title[:30]}...'")
                    # Verificar acceso a relaciones
                    project_name = task.project.name if task.project else "Sin proyecto"
                    assignee_name = task.assignee.name if task.assignee else "Sin asignado"
                    creator_name = task.creator.name if task.creator else "Sin creador"
                    print(f"     Proyecto: {project_name}")
                    print(f"     Asignado: {assignee_name}")
                    print(f"     Creador: {creator_name}")
                except Exception as e:
                    print(f"❌ Error accediendo a relaciones de tarea {task.id}: {str(e)}")
                    print(f"   Traceback: {traceback.format_exc()}")
                    break
            
            print("✅ Serialización de tareas exitosa")
            
        except Exception as e:
            print(f"❌ Error en TaskService.get_tasks: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
        
        # Probar con usuario regular para comparar
        print("\n4️⃣ Comparando con usuario regular...")
        regular_user = db.query(User).filter(User.email == "test@example.com").first()
        if regular_user:
            try:
                regular_tasks = task_service.get_tasks(
                    db=db,
                    user_id=regular_user.id,
                    project_id=None,
                    assignee_id=None,
                    status=None,
                    priority=None,
                    search=None,
                    due_date_from=None,
                    due_date_to=None,
                    skip=0,
                    limit=100
                )
                print(f"✅ Usuario regular: {len(regular_tasks)} tareas")
            except Exception as e:
                print(f"❌ Error con usuario regular: {str(e)}")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_endpoint_flow()