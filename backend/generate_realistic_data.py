#!/usr/bin/env python3
"""
Script para generar datos de prueba realistas para el Project AI Manager
Incluye 40 proyectos colombianos con diferentes estados y tareas asociadas
"""

import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus
from app.services.auth_service import AuthService

# Datos realistas para proyectos colombianos
PROYECTOS_COLOMBIA = [
    {
        "name": "Modernización Metro de Bogotá",
        "description": "Actualización del sistema de transporte masivo de Bogotá con tecnología 4.0",
        "budget": 2500000000,
        "sector": "Transporte"
    },
    {
        "name": "Plataforma Digital Gobierno Distrital",
        "description": "Sistema unificado para trámites ciudadanos en línea para la Alcaldía de Bogotá",
        "budget": 850000000,
        "sector": "Gobierno"
    },
    {
        "name": "App Turismo Cartagena",
        "description": "Aplicación móvil para promoción turística de Cartagena de Indias",
        "budget": 320000000,
        "sector": "Turismo"
    },
    {
        "name": "Sistema ERP Ecopetrol",
        "description": "Implementación de sistema empresarial para gestión de recursos petroleros",
        "budget": 4200000000,
        "sector": "Energía"
    },
    {
        "name": "Portal E-learning Universidad Nacional",
        "description": "Plataforma educativa virtual para estudiantes de pregrado y posgrado",
        "budget": 680000000,
        "sector": "Educación"
    },
    {
        "name": "App Bancolombia Móvil",
        "description": "Renovación completa de la aplicación móvil bancaria",
        "budget": 1200000000,
        "sector": "Finanzas"
    },
    {
        "name": "Sistema Salud Medellín",
        "description": "Plataforma integrada para hospitales y centros de salud de Medellín",
        "budget": 950000000,
        "sector": "Salud"
    },
    {
        "name": "E-commerce Falabella Colombia",
        "description": "Modernización de la plataforma de comercio electrónico",
        "budget": 780000000,
        "sector": "Retail"
    },
    {
        "name": "Smart City Barranquilla",
        "description": "Implementación de IoT y sensores inteligentes en la ciudad",
        "budget": 1800000000,
        "sector": "Tecnología"
    },
    {
        "name": "App Delivery Rappi",
        "description": "Optimización del algoritmo de entrega y nueva interfaz",
        "budget": 450000000,
        "sector": "Logística"
    },
    {
        "name": "Portal DIAN Tributario",
        "description": "Sistema de declaración de impuestos en línea",
        "budget": 1100000000,
        "sector": "Gobierno"
    },
    {
        "name": "Plataforma Streaming Caracol",
        "description": "Servicio de video bajo demanda para contenido nacional",
        "budget": 620000000,
        "sector": "Entretenimiento"
    },
    {
        "name": "Sistema Agrícola Valle del Cauca",
        "description": "Plataforma para gestión de cultivos y predicción climática",
        "budget": 890000000,
        "sector": "Agricultura"
    },
    {
        "name": "App Movilidad Cali",
        "description": "Sistema integrado de transporte público para Cali",
        "budget": 540000000,
        "sector": "Transporte"
    },
    {
        "name": "Portal Inmobiliario Finca Raíz",
        "description": "Renovación completa del portal de bienes raíces",
        "budget": 380000000,
        "sector": "Inmobiliario"
    },
    {
        "name": "Sistema Minero Cerrejón",
        "description": "Plataforma de gestión y monitoreo de operaciones mineras",
        "budget": 2100000000,
        "sector": "Minería"
    },
    {
        "name": "App Fitness BodyTech",
        "description": "Aplicación para entrenamiento personalizado y nutrición",
        "budget": 290000000,
        "sector": "Deportes"
    },
    {
        "name": "Plataforma Logística Avianca",
        "description": "Sistema de gestión de vuelos y equipajes",
        "budget": 1350000000,
        "sector": "Aerolíneas"
    },
    {
        "name": "Portal Educativo SENA",
        "description": "Plataforma de formación técnica y tecnológica virtual",
        "budget": 720000000,
        "sector": "Educación"
    },
    {
        "name": "Sistema Hospitalario Fundación Santa Fe",
        "description": "Historia clínica electrónica y gestión hospitalaria",
        "budget": 650000000,
        "sector": "Salud"
    },
    {
        "name": "App Gastronomía Bogotá",
        "description": "Plataforma para descubrimiento de restaurantes locales",
        "budget": 180000000,
        "sector": "Gastronomía"
    },
    {
        "name": "Sistema Energético EPM",
        "description": "Plataforma de gestión de servicios públicos",
        "budget": 1600000000,
        "sector": "Servicios Públicos"
    },
    {
        "name": "Portal Cultura Ministerio",
        "description": "Plataforma digital para promoción cultural nacional",
        "budget": 420000000,
        "sector": "Cultura"
    },
    {
        "name": "App Seguridad Ciudadana",
        "description": "Sistema de alertas y emergencias para ciudadanos",
        "budget": 580000000,
        "sector": "Seguridad"
    },
    {
        "name": "Plataforma Textil Fabricato",
        "description": "Sistema de gestión de producción textil",
        "budget": 340000000,
        "sector": "Manufactura"
    },
    {
        "name": "Portal Exportaciones ProColombia",
        "description": "Plataforma para promoción de exportaciones colombianas",
        "budget": 480000000,
        "sector": "Comercio Exterior"
    },
    {
        "name": "Sistema Cafetero FNC",
        "description": "Plataforma de trazabilidad del café colombiano",
        "budget": 760000000,
        "sector": "Agricultura"
    },
    {
        "name": "App Parques Nacionales",
        "description": "Sistema de reservas y gestión de parques naturales",
        "budget": 250000000,
        "sector": "Medio Ambiente"
    },
    {
        "name": "Portal Judicial Rama Judicial",
        "description": "Sistema de gestión de procesos judiciales",
        "budget": 1400000000,
        "sector": "Justicia"
    },
    {
        "name": "Plataforma Cooperativa Coomeva",
        "description": "Sistema integral de servicios cooperativos",
        "budget": 520000000,
        "sector": "Cooperativo"
    },
    {
        "name": "App Deportes Millonarios FC",
        "description": "Aplicación oficial del club con contenido exclusivo",
        "budget": 150000000,
        "sector": "Deportes"
    },
    {
        "name": "Sistema Portuario Buenaventura",
        "description": "Plataforma de gestión portuaria y logística",
        "budget": 980000000,
        "sector": "Logística"
    },
    {
        "name": "Portal Artesanías de Colombia",
        "description": "E-commerce para artesanías tradicionales colombianas",
        "budget": 220000000,
        "sector": "Artesanías"
    },
    {
        "name": "App Clima IDEAM",
        "description": "Sistema de pronóstico meteorológico nacional",
        "budget": 380000000,
        "sector": "Meteorología"
    },
    {
        "name": "Plataforma Pensiones Colpensiones",
        "description": "Sistema de gestión de pensiones y cesantías",
        "budget": 1250000000,
        "sector": "Pensiones"
    },
    {
        "name": "Portal Empleo SENA",
        "description": "Plataforma de intermediación laboral nacional",
        "budget": 460000000,
        "sector": "Empleo"
    },
    {
        "name": "Sistema Académico Javeriana",
        "description": "Plataforma integral de gestión universitaria",
        "budget": 590000000,
        "sector": "Educación Superior"
    },
    {
        "name": "App Reciclaje Bogotá",
        "description": "Sistema de gestión de residuos y reciclaje urbano",
        "budget": 320000000,
        "sector": "Medio Ambiente"
    },
    {
        "name": "Portal Microfinanzas Bancamía",
        "description": "Plataforma de microcréditos para emprendedores",
        "budget": 280000000,
        "sector": "Microfinanzas"
    },
    {
        "name": "Sistema Hotelero Decameron",
        "description": "Plataforma de gestión hotelera y reservas",
        "budget": 410000000,
        "sector": "Hotelería"
    }
]

ESTADOS_PROYECTO = [ProjectStatus.PLANNING, ProjectStatus.ACTIVE, ProjectStatus.COMPLETED, ProjectStatus.ON_HOLD]
ESTADOS_TAREA = ["todo", "in_progress", "in_review", "done", "cancelled"]

TAREAS_TEMPLATES = [
    "Análisis de requerimientos",
    "Diseño de arquitectura",
    "Desarrollo del backend",
    "Desarrollo del frontend",
    "Implementación de base de datos",
    "Pruebas unitarias",
    "Pruebas de integración",
    "Pruebas de usuario",
    "Documentación técnica",
    "Capacitación de usuarios",
    "Despliegue en producción",
    "Monitoreo y mantenimiento",
    "Optimización de rendimiento",
    "Implementación de seguridad",
    "Integración con APIs externas",
    "Configuración de servidores",
    "Backup y recuperación",
    "Análisis de datos",
    "Reportes y métricas",
    "Soporte técnico"
]

def create_realistic_data():
    """Crear datos de prueba realistas"""
    print("🚀 Iniciando generación de datos realistas...")
    
    session = SessionLocal()
    try:
        # Verificar si ya existen usuarios
        user_count = session.query(User).count()
        
        if user_count == 0:
            print("❌ No se encontraron usuarios. Creando usuarios de prueba...")
            # Crear usuarios de prueba
            test_user = User(
                email="test@example.com",
                hashed_password=AuthService.get_password_hash("testpassword123"),
                full_name="Usuario de Prueba",
                is_active=True,
                is_admin=False
            )
            
            admin_user = User(
                email="admin@example.com",
                hashed_password=AuthService.get_password_hash("adminpassword123"),
                full_name="Administrador",
                is_active=True,
                is_admin=True
            )
            
            session.add(test_user)
            session.add(admin_user)
            session.commit()
            print("✅ Usuarios creados exitosamente")
        
        # Obtener usuarios existentes
        users = session.query(User).limit(10).all()
        user_ids = [user.id for user in users]
        
        if not user_ids:
            print("❌ No se pudieron obtener IDs de usuarios")
            return
        
        print(f"👥 Encontrados {len(user_ids)} usuarios")
        
        # Crear proyectos
        proyectos_creados = 0
        tareas_creadas = 0
        
        for i, proyecto_data in enumerate(PROYECTOS_COLOMBIA):
            # Fechas realistas
            start_date = datetime.now() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=random.randint(60, 300))
            
            # Estado aleatorio con distribución realista
            estado_weights = [0.15, 0.45, 0.25, 0.15]  # planning, in_progress, completed, on_hold
            estado = random.choices(ESTADOS_PROYECTO, weights=estado_weights)[0]
            
            proyecto = Project(
                name=proyecto_data["name"],
                description=proyecto_data["description"],
                start_date=start_date.date(),
                end_date=end_date.date(),
                budget=proyecto_data["budget"],
                status=estado,
                owner_id=random.choice(user_ids)
            )
            
            session.add(proyecto)
            session.flush()  # Para obtener el ID del proyecto
            
            # Crear 3-4 tareas por proyecto
            num_tareas = random.randint(3, 4)
            tareas_proyecto = random.sample(TAREAS_TEMPLATES, num_tareas)
            
            for j, tarea_nombre in enumerate(tareas_proyecto):
                # Fechas de tareas dentro del rango del proyecto
                task_start = start_date + timedelta(days=random.randint(0, 30))
                task_due = task_start + timedelta(days=random.randint(7, 45))
                
                # Estado de tarea basado en el estado del proyecto
                if estado == "completed":
                    task_status = random.choices(["done", "cancelled"], weights=[0.9, 0.1])[0]
                elif estado == "in_progress":
                    task_status = random.choices(ESTADOS_TAREA, weights=[0.2, 0.4, 0.2, 0.1, 0.1])[0]
                elif estado == "planning":
                    task_status = random.choices(["todo", "in_progress"], weights=[0.7, 0.3])[0]
                else:  # on_hold
                    task_status = random.choices(["todo", "cancelled"], weights=[0.6, 0.4])[0]
                
                # Prioridad aleatoria
                priority = random.choices(["low", "medium", "high", "critical"], weights=[0.3, 0.4, 0.2, 0.1])[0]
                
                tarea = Task(
                     title=f"{tarea_nombre} - {proyecto_data['name'][:30]}",
                     description=f"Tarea de {tarea_nombre.lower()} para el proyecto {proyecto_data['name']}",
                     status=task_status,
                     priority=priority,
                     due_date=task_due.date(),
                     project_id=proyecto.id,
                     assignee_id=random.choice(user_ids),
                     creator_id=random.choice(user_ids)
                 )
                
                session.add(tarea)
                tareas_creadas += 1
            
            proyectos_creados += 1
            
            if (i + 1) % 10 == 0:
                print(f"📊 Progreso: {i + 1}/40 proyectos creados...")
        
        session.commit()
        
        print(f"✅ Datos generados exitosamente:")
        print(f"   📁 {proyectos_creados} proyectos creados")
        print(f"   📋 {tareas_creadas} tareas creadas")
        print(f"   🏢 Sectores: Gobierno, Tecnología, Salud, Educación, Finanzas, etc.")
        print(f"   💰 Presupuestos: Desde $150M hasta $4.2B COP")
        print(f"   📅 Fechas: Últimos 12 meses con proyección futura")
        
    except Exception as e:
        print(f"❌ Error generando datos: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    create_realistic_data()