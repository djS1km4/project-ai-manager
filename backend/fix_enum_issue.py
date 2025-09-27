#!/usr/bin/env python3
"""
Script para corregir valores de enum incorrectos en la base de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

def fix_enum_values():
    """Corregir valores de enum incorrectos en la base de datos"""
    print("🔧 Corrigiendo valores de enum incorrectos")
    print("=" * 50)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Corregir TaskStatus enum values
        print("📋 Corrigiendo valores de TaskStatus...")
        
        # Mapeo de valores incorrectos a correctos
        task_status_fixes = {
            'cancelled': 'CANCELLED',
            'todo': 'TODO',
            'in_progress': 'IN_PROGRESS',
            'in_review': 'IN_REVIEW',
            'done': 'DONE'
        }
        
        for old_value, new_value in task_status_fixes.items():
            # Actualizar tareas con valores incorrectos
            result = db.execute(
                text("UPDATE tasks SET status = :new_value WHERE status = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            
            if result.rowcount > 0:
                print(f"   ✅ Corregido {result.rowcount} tareas: '{old_value}' -> '{new_value}'")
            else:
                print(f"   ℹ️  No hay tareas con estado '{old_value}'")
        
        # Corregir TaskPriority enum values
        print("\n🎯 Corrigiendo valores de TaskPriority...")
        
        task_priority_fixes = {
            'low': 'LOW',
            'medium': 'MEDIUM', 
            'high': 'HIGH',
            'critical': 'CRITICAL'
        }
        
        for old_value, new_value in task_priority_fixes.items():
            result = db.execute(
                text("UPDATE tasks SET priority = :new_value WHERE priority = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            
            if result.rowcount > 0:
                print(f"   ✅ Corregido {result.rowcount} tareas: '{old_value}' -> '{new_value}'")
            else:
                print(f"   ℹ️  No hay tareas con prioridad '{old_value}'")
        
        # Corregir ProjectStatus enum values
        print("\n📁 Corrigiendo valores de ProjectStatus...")
        
        project_status_fixes = {
            'planning': 'PLANNING',
            'active': 'ACTIVE',
            'on_hold': 'ON_HOLD',
            'completed': 'COMPLETED',
            'cancelled': 'CANCELLED'
        }
        
        for old_value, new_value in project_status_fixes.items():
            result = db.execute(
                text("UPDATE projects SET status = :new_value WHERE status = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            
            if result.rowcount > 0:
                print(f"   ✅ Corregido {result.rowcount} proyectos: '{old_value}' -> '{new_value}'")
            else:
                print(f"   ℹ️  No hay proyectos con estado '{old_value}'")
        
        # Corregir ProjectPriority enum values
        print("\n🎯 Corrigiendo valores de ProjectPriority...")
        
        project_priority_fixes = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH',
            'critical': 'CRITICAL'
        }
        
        for old_value, new_value in project_priority_fixes.items():
            result = db.execute(
                text("UPDATE projects SET priority = :new_value WHERE priority = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            
            if result.rowcount > 0:
                print(f"   ✅ Corregido {result.rowcount} proyectos: '{old_value}' -> '{new_value}'")
            else:
                print(f"   ℹ️  No hay proyectos con prioridad '{old_value}'")
        
        # Confirmar cambios
        db.commit()
        print(f"\n✅ Todos los cambios han sido confirmados en la base de datos")
        
        # Verificar que no quedan valores incorrectos
        print(f"\n🔍 Verificando corrección...")
        
        # Verificar tareas
        invalid_tasks = db.execute(
            text("SELECT COUNT(*) as count FROM tasks WHERE status NOT IN ('TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE', 'CANCELLED')")
        ).fetchone()
        
        if invalid_tasks.count == 0:
            print(f"   ✅ Todos los estados de tareas son válidos")
        else:
            print(f"   ❌ Aún hay {invalid_tasks.count} tareas con estados inválidos")
        
        # Verificar proyectos
        invalid_projects = db.execute(
            text("SELECT COUNT(*) as count FROM projects WHERE status NOT IN ('PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED')")
        ).fetchone()
        
        if invalid_projects.count == 0:
            print(f"   ✅ Todos los estados de proyectos son válidos")
        else:
            print(f"   ❌ Aún hay {invalid_projects.count} proyectos con estados inválidos")
            
    except Exception as e:
        print(f"❌ Error durante la corrección: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
    
    print("\n" + "=" * 50)
    print("🏁 Corrección de enum completada")

if __name__ == "__main__":
    fix_enum_values()