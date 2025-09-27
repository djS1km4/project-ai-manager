#!/usr/bin/env python3
"""
Script para corregir los valores de enum en la base de datos.
"""

from sqlalchemy import text
from app.database import SessionLocal

def fix_enum_values():
    """Corregir valores de enum en la base de datos"""
    db = SessionLocal()
    
    try:
        # Mapeo de valores incorrectos a correctos
        status_mapping = {
            'planning': 'PLANNING',
            'in_progress': 'ACTIVE',
            'completed': 'COMPLETED',
            'on_hold': 'ON_HOLD',
            'cancelled': 'CANCELLED'
        }
        
        priority_mapping = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH',
            'critical': 'CRITICAL'
        }
        
        print("Corrigiendo valores de ProjectStatus...")
        for old_value, new_value in status_mapping.items():
            result = db.execute(
                text("UPDATE projects SET status = :new_value WHERE status = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            if result.rowcount > 0:
                print(f"  Actualizado {result.rowcount} proyectos: {old_value} -> {new_value}")
        
        print("\nCorrigiendo valores de ProjectPriority...")
        for old_value, new_value in priority_mapping.items():
            result = db.execute(
                text("UPDATE projects SET priority = :new_value WHERE priority = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            if result.rowcount > 0:
                print(f"  Actualizado {result.rowcount} proyectos: {old_value} -> {new_value}")
        
        # También corregir tareas si es necesario
        task_status_mapping = {
            'todo': 'TODO',
            'in_progress': 'IN_PROGRESS',
            'in_review': 'IN_REVIEW',
            'done': 'DONE',
            'cancelled': 'CANCELLED'
        }
        
        print("\nCorrigiendo valores de TaskStatus...")
        for old_value, new_value in task_status_mapping.items():
            result = db.execute(
                text("UPDATE tasks SET status = :new_value WHERE status = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            if result.rowcount > 0:
                print(f"  Actualizado {result.rowcount} tareas: {old_value} -> {new_value}")
        
        task_priority_mapping = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH',
            'critical': 'CRITICAL'
        }
        
        print("\nCorrigiendo valores de TaskPriority...")
        for old_value, new_value in task_priority_mapping.items():
            result = db.execute(
                text("UPDATE tasks SET priority = :new_value WHERE priority = :old_value"),
                {"old_value": old_value, "new_value": new_value}
            )
            if result.rowcount > 0:
                print(f"  Actualizado {result.rowcount} tareas: {old_value} -> {new_value}")
        
        db.commit()
        print("\n✅ Valores de enum corregidos exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_enum_values()