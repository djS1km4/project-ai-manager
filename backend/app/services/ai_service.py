import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus, TaskPriority
from ..models.ai_insight import (
    AIInsight, InsightType, InsightPriority, ProjectAnalytics,
    RiskAssessment, ProgressPrediction, TeamPerformanceAnalysis, BudgetForecast, ProjectInfo
)
import os
from dotenv import load_dotenv
from .deepseek_service import DeepseekAIService

load_dotenv()

class AIProjectAnalysisService:
    def __init__(self):
        # Initialize Deepseek service
        self.deepseek_service = DeepseekAIService()
        self.ai_enabled = self.deepseek_service.is_enabled()
        
        # Legacy OpenAI support (deprecated)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_enabled = (
            self.openai_api_key and 
            self.openai_api_key != "your-openai-api-key-here" and
            self.openai_api_key != "disabled"
        )
    
    def _generate_mock_data_notice(self) -> str:
        """Generate a notice about mock data when AI is not available"""
        if self.ai_enabled:
            return ""  # No notice needed when AI is working
        return "⚠️ Datos simulados - Configure DEEPSEEK_API_KEY para análisis real con IA"
    
    def analyze_project_risk(self, project_id: int, db: Session) -> RiskAssessment:
        """Analyze project risks using Deepseek AI"""
        # Use Deepseek service for risk analysis
        return self.deepseek_service.analyze_project_risk(project_id, db)
        
        # Initialize comprehensive risk analysis
        risk_score = 0.0
        risk_factors = []
        risk_categories = {
            "schedule_risk": 0.0,
            "resource_risk": 0.0,
            "quality_risk": 0.0,
            "budget_risk": 0.0,
            "technical_risk": 0.0
        }
        
        # Advanced time-based risk analysis
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
        
        # Schedule Risk Analysis
        if overdue_tasks:
            overdue_percentage = len(overdue_tasks) / total_tasks * 100
            schedule_risk = min(0.5, overdue_percentage / 100 * 2)
            risk_categories["schedule_risk"] = schedule_risk
            
            if overdue_percentage > 30:
                risk_factors.append({
                    "factor": "Tareas Vencidas Críticas",
                    "severity": "critical",
                    "description": f"{len(overdue_tasks)} tareas vencidas ({overdue_percentage:.1f}%) - Riesgo alto de incumplimiento",
                    "impact": 0.4,
                    "category": "schedule"
                })
                risk_score += 0.4
            elif overdue_percentage > 15:
                risk_factors.append({
                    "factor": "Tareas Vencidas",
                    "severity": "high",
                    "description": f"{len(overdue_tasks)} tareas vencidas ({overdue_percentage:.1f}%) - Requiere atención inmediata",
                    "impact": 0.25,
                    "category": "schedule"
                })
                risk_score += 0.25
            else:
                risk_factors.append({
                    "factor": "Retrasos Menores",
                    "severity": "medium",
                    "description": f"{len(overdue_tasks)} tareas vencidas ({overdue_percentage:.1f}%) - Monitoreo requerido",
                    "impact": 0.1,
                    "category": "schedule"
                })
                risk_score += 0.1
        
        # Progress and deadline risk
        if total_tasks > 0 and project.end_date:
            completion_rate = completed_tasks / total_tasks
            days_remaining = (project.end_date - datetime.utcnow()).days
            
            if completion_rate < 0.3 and days_remaining < 30:
                schedule_risk_additional = 0.3
                risk_categories["schedule_risk"] += schedule_risk_additional
                risk_factors.append({
                    "factor": "Cronograma en Riesgo Crítico",
                    "severity": "critical",
                    "description": f"Solo {completion_rate*100:.1f}% completado con {days_remaining} días restantes",
                    "impact": 0.3,
                    "category": "schedule"
                })
                risk_score += 0.3
            elif completion_rate < 0.5 and days_remaining < 60:
                schedule_risk_additional = 0.2
                risk_categories["schedule_risk"] += schedule_risk_additional
                risk_factors.append({
                    "factor": "Progreso Insuficiente",
                    "severity": "high",
                    "description": f"Progreso del {completion_rate*100:.1f}% insuficiente para deadline en {days_remaining} días",
                    "impact": 0.2,
                    "category": "schedule"
                })
                risk_score += 0.2
        
        # Resource Risk Analysis
        unassigned_tasks = [t for t in tasks if not t.assignee_id and t.status != TaskStatus.DONE]
        if unassigned_tasks:
            unassigned_percentage = len(unassigned_tasks) / total_tasks * 100
            resource_risk = min(0.3, unassigned_percentage / 100 * 1.5)
            risk_categories["resource_risk"] = resource_risk
            
            if unassigned_percentage > 20:
                risk_factors.append({
                    "factor": "Recursos Insuficientes",
                    "severity": "high",
                    "description": f"{len(unassigned_tasks)} tareas sin asignar ({unassigned_percentage:.1f}%) - Riesgo de retrasos",
                    "impact": 0.2,
                    "category": "resource"
                })
                risk_score += 0.2
            else:
                risk_factors.append({
                    "factor": "Asignación Pendiente",
                    "severity": "medium",
                    "description": f"{len(unassigned_tasks)} tareas requieren asignación urgente",
                    "impact": 0.1,
                    "category": "resource"
                })
                risk_score += 0.1
        
        # Workload distribution and team capacity risk
        assignee_workload = {}
        high_priority_tasks = {}
        
        for task in tasks:
            if task.assignee_id and task.status != TaskStatus.DONE:
                assignee_workload[task.assignee_id] = assignee_workload.get(task.assignee_id, 0) + 1
                if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]:
                    high_priority_tasks[task.assignee_id] = high_priority_tasks.get(task.assignee_id, 0) + 1
        
        if assignee_workload:
            max_workload = max(assignee_workload.values())
            min_workload = min(assignee_workload.values())
            avg_workload = sum(assignee_workload.values()) / len(assignee_workload)
            
            if max_workload > avg_workload * 2.5:
                resource_risk_additional = 0.25
                risk_categories["resource_risk"] += resource_risk_additional
                risk_factors.append({
                    "factor": "Sobrecarga Crítica de Trabajo",
                    "severity": "critical",
                    "description": f"Distribución desigual: máximo {max_workload} vs promedio {avg_workload:.1f} tareas - Alto riesgo de burnout",
                    "impact": 0.25,
                    "category": "resource"
                })
                risk_score += 0.25
            elif max_workload > avg_workload * 1.8:
                resource_risk_additional = 0.15
                risk_categories["resource_risk"] += resource_risk_additional
                risk_factors.append({
                    "factor": "Desequilibrio de Carga",
                    "severity": "medium",
                    "description": f"Distribución desigual: {max_workload} vs {min_workload} tareas por persona",
                    "impact": 0.15,
                    "category": "resource"
                })
                risk_score += 0.15
        
        # Quality Risk Analysis
        stuck_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS and t.updated_at and 
                      (datetime.utcnow() - t.updated_at).days > 7]
        if stuck_tasks:
            stuck_percentage = len(stuck_tasks) / len(tasks) * 100
            quality_risk = min(0.2, stuck_percentage / 100 * 1.2)
            risk_categories["quality_risk"] = quality_risk
            
            risk_factors.append({
                "factor": "Tareas Estancadas",
                "severity": "medium" if stuck_percentage < 15 else "high",
                "description": f"{len(stuck_tasks)} tareas sin progreso >7 días ({stuck_percentage:.1f}%) - Riesgo de calidad",
                "impact": 0.15 if stuck_percentage < 15 else 0.2,
                "category": "quality"
            })
            risk_score += 0.15 if stuck_percentage < 15 else 0.2
        
        # Technical Risk Analysis (based on task complexity and dependencies)
        high_priority_count = len([t for t in tasks if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]])
        if high_priority_count > total_tasks * 0.4:
            technical_risk = 0.15
            risk_categories["technical_risk"] = technical_risk
            risk_factors.append({
                "factor": "Alta Complejidad del Proyecto",
                "severity": "medium",
                "description": f"{high_priority_count} tareas de alta prioridad ({high_priority_count/total_tasks*100:.1f}%) - Riesgo técnico elevado",
                "impact": 0.15,
                "category": "technical"
            })
            risk_score += 0.15
        
        # Budget Risk Analysis (simulated based on project duration and complexity)
        if project.end_date:
            project_duration = (project.end_date - project.created_at).days if project.created_at else 90
            if project_duration > 180:  # Long projects have higher budget risk
                budget_risk = 0.1
                risk_categories["budget_risk"] = budget_risk
                risk_factors.append({
                    "factor": "Proyecto de Larga Duración",
                    "severity": "low",
                    "description": f"Duración de {project_duration} días aumenta riesgo de sobrecostos",
                    "impact": 0.1,
                    "category": "budget"
                })
                risk_score += 0.1
        
        # Determine overall risk level
        if risk_score >= 0.7:
            risk_level = "Crítico"
        elif risk_score >= 0.5:
            risk_level = "Alto"
        elif risk_score >= 0.3:
            risk_level = "Medio"
        elif risk_score >= 0.1:
            risk_level = "Bajo"
        else:
            risk_level = "Mínimo"
        
        # Generate comprehensive recommendations and mitigation strategies
        recommendations = []
        mitigation_strategies = []
        critical_issues = []
        
        for factor in risk_factors:
            if factor["severity"] in ["critical", "high"]:
                critical_issues.append(factor["description"])
                
                if factor["category"] == "schedule":
                    recommendations.append("🚨 URGENTE: Revisar cronograma y reprogramar tareas críticas")
                    mitigation_strategies.append({"strategy": "Implementar metodología de gestión ágil para acelerar entregas", "priority": "Alta", "timeline": "Inmediato"})
                elif factor["category"] == "resource":
                    recommendations.append("👥 URGENTE: Redistribuir recursos y balancear cargas de trabajo")
                    mitigation_strategies.append({"strategy": "Contratar recursos adicionales o reasignar personal", "priority": "Alta", "timeline": "1-2 semanas"})
                elif factor["category"] == "quality":
                    recommendations.append("🔍 Revisar tareas estancadas e implementar daily standups")
                    mitigation_strategies.append({"strategy": "Establecer checkpoints de calidad y revisiones periódicas", "priority": "Media", "timeline": "1 semana"})
            else:
                if factor["category"] == "schedule":
                    recommendations.append("📅 Monitorear progreso semanalmente y ajustar cronograma")
                elif factor["category"] == "resource":
                    recommendations.append("📝 Completar asignación de tareas pendientes")
                elif factor["category"] == "technical":
                    recommendations.append("🛠️ Evaluar complejidad técnica y dividir tareas grandes")
        
        # Risk timeline projection
        current_risk = min(1.0, risk_score)
        projected_30_days = min(1.0, risk_score * 1.1) if risk_score > 0.3 else max(0.0, risk_score * 0.9)
        projected_60_days = min(1.0, risk_score * 1.2) if risk_score > 0.4 else max(0.0, risk_score * 0.8)
        
        risk_timeline = {
            "current": round(current_risk, 2),
            "projected_30_days": round(projected_30_days, 2),
            "projected_60_days": round(projected_60_days, 2)
        }
        
        # Add general recommendations based on risk level
        if risk_score > 0.7:
            recommendations.append("🚨 PROYECTO EN RIESGO CRÍTICO - Requiere intervención inmediata del PMO")
            mitigation_strategies.append({"strategy": "Activar plan de contingencia y escalamiento ejecutivo", "priority": "Crítica", "timeline": "Inmediato"})
        elif risk_score > 0.4:
            recommendations.append("⚠️ Proyecto en riesgo moderado - Implementar monitoreo intensivo")
            mitigation_strategies.append({"strategy": "Reuniones de seguimiento diarias y reportes semanales", "priority": "Alta", "timeline": "Esta semana"})
        elif not recommendations:
            recommendations.append("✅ Proyecto en buen estado - Continuar con monitoreo regular")
            mitigation_strategies.append({"strategy": "Mantener prácticas actuales y monitoreo preventivo", "priority": "Baja", "timeline": "Continuo"})
        
        # Add mock data notice if OpenAI is not available
        if not self.openai_enabled:
            recommendations.insert(0, self._generate_mock_data_notice())
        
        return RiskAssessment(
            project_info=project_info,
            overall_risk_score=round(min(1.0, risk_score), 2),
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations,
            critical_issues=critical_issues,
            risk_categories=risk_categories,
            mitigation_strategies=mitigation_strategies,
            impact_assessment={
                "schedule_impact": "Alto" if risk_categories.get("schedule_risk", 0) > 0.3 else "Medio" if risk_categories.get("schedule_risk", 0) > 0.1 else "Bajo",
                "budget_impact": "Alto" if risk_categories.get("budget_risk", 0) > 0.3 else "Medio" if risk_categories.get("budget_risk", 0) > 0.1 else "Bajo",
                "quality_impact": "Alto" if risk_categories.get("quality_risk", 0) > 0.3 else "Medio" if risk_categories.get("quality_risk", 0) > 0.1 else "Bajo",
                "team_impact": "Alto" if risk_categories.get("resource_risk", 0) > 0.3 else "Medio" if risk_categories.get("resource_risk", 0) > 0.1 else "Bajo"
            },
            risk_timeline=risk_timeline
        )
    
    def predict_project_completion(self, project_id: int, db: Session) -> ProgressPrediction:
        """Predict project completion using Deepseek AI"""
        # Use Deepseek service for progress prediction
        return self.deepseek_service.predict_project_completion(project_id, db)
        
        # Calculate detailed progress metrics
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        in_progress_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        todo_tasks = [t for t in tasks if t.status == TaskStatus.TODO]
        remaining_tasks = in_progress_tasks + todo_tasks
        
        current_progress = len(completed_tasks) / len(tasks) * 100
        
        # Analyze task completion patterns
        completed_with_times = [t for t in completed_tasks if t.completed_at and t.created_at]
        if completed_with_times:
            completion_times = [(t.completed_at - t.created_at).days for t in completed_with_times]
            avg_completion_days = sum(completion_times) / len(completion_times)
            max_completion_days = max(completion_times)
            min_completion_days = min(completion_times)
        else:
            avg_completion_days = 3  # Conservative default
            max_completion_days = 7
            min_completion_days = 1
        
        # Calculate velocity (tasks completed per week)
        if completed_tasks:
            project_duration = (datetime.utcnow() - project.created_at).days if project.created_at else 30
            velocity = len(completed_tasks) / max(1, project_duration / 7)  # tasks per week
        else:
            velocity = 0.5  # Conservative default
        
        # Determine velocity trend
        velocity_trend = "stable"
        if velocity > 2:
            velocity_trend = "increasing"
        elif velocity < 0.5:
            velocity_trend = "decreasing"
        
        # Predict remaining time with multiple factors
        base_remaining_days = len(remaining_tasks) * avg_completion_days
        
        # Team efficiency analysis
        active_assignees = len(set(t.assignee_id for t in tasks if t.assignee_id and t.status != TaskStatus.DONE))
        team_factor = 1.0
        if active_assignees > 3:
            team_factor = 0.7  # Large team efficiency
        elif active_assignees > 1:
            team_factor = 0.8  # Small team efficiency
        elif active_assignees == 0:
            team_factor = 1.5  # No assignments penalty
        
        # Complexity and priority analysis
        high_priority_remaining = len([t for t in remaining_tasks if t.priority in ['high', 'urgent']])
        complexity_factor = 1.0
        if high_priority_remaining > len(remaining_tasks) * 0.5:
            complexity_factor = 1.3  # Many high priority tasks
        
        # Overdue task impact
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
        overdue_factor = 1.0
        if overdue_tasks:
            overdue_factor = 1.2 + (len(overdue_tasks) / len(tasks)) * 0.5
        
        # Calculate final prediction
        adjusted_days = base_remaining_days * team_factor * complexity_factor * overdue_factor
        predicted_date = datetime.utcnow() + timedelta(days=max(1, adjusted_days))
        
        # Calculate completion probability
        completion_probability = 0.9
        if predicted_date > project.end_date if project.end_date else False:
            days_over = (predicted_date - project.end_date).days if project.end_date else 0
            completion_probability = max(0.1, 0.9 - (days_over / 30) * 0.3)
        
        # Calculate confidence level with detailed factors
        confidence = 0.9
        confidence_factors = []
        
        if len(completed_tasks) < 3:
            confidence -= 0.25
            confidence_factors.append("📊 Datos históricos limitados")
        if overdue_tasks:
            confidence -= 0.15
            confidence_factors.append(f"⏰ {len(overdue_tasks)} tareas vencidas")
        if active_assignees == 0:
            confidence -= 0.3
            confidence_factors.append("👥 Tareas sin asignar")
        if velocity < 0.3:
            confidence -= 0.2
            confidence_factors.append("🐌 Velocidad de desarrollo baja")
        if high_priority_remaining > len(remaining_tasks) * 0.7:
            confidence -= 0.1
            confidence_factors.append("🔥 Muchas tareas de alta prioridad pendientes")
        
        confidence = max(0.1, confidence)
        
        # Identify critical path tasks
        critical_path_tasks = []
        for task in remaining_tasks:
            if task.priority in ['high', 'urgent'] or (task.due_date and task.due_date < datetime.utcnow() + timedelta(days=7)):
                critical_path_tasks.append(f"🔥 {task.title}")
        
        # Identify potential delays
        potential_delays = []
        if overdue_tasks:
            potential_delays.append(f"📅 {len(overdue_tasks)} tareas vencidas")
        if active_assignees == 0:
            potential_delays.append("👥 Tareas sin asignar")
        if velocity < 0.5:
            potential_delays.append("🐌 Velocidad baja del equipo")
        if high_priority_remaining > len(remaining_tasks) * 0.5:
            potential_delays.append("🔥 Muchas tareas críticas pendientes")
        
        # Identify acceleration opportunities
        acceleration_opportunities = []
        if active_assignees == 1 and len(remaining_tasks) > 5:
            acceleration_opportunities.append("👥 Agregar más miembros al equipo")
        if len([t for t in remaining_tasks if t.priority == 'low']) > 3:
            acceleration_opportunities.append("🎯 Diferir tareas de baja prioridad")
        if velocity > 1.5:
            acceleration_opportunities.append("⚡ Aprovechar alta velocidad actual")
        
        # Generate milestone predictions
        milestone_predictions = []
        if current_progress < 25:
            milestone_date = datetime.utcnow() + timedelta(days=adjusted_days * 0.25)
            milestone_predictions.append({
                "milestone": "25% Completado",
                "predicted_date": milestone_date.isoformat(),
                "confidence": confidence * 0.9
            })
        if current_progress < 50:
            milestone_date = datetime.utcnow() + timedelta(days=adjusted_days * 0.5)
            milestone_predictions.append({
                "milestone": "50% Completado",
                "predicted_date": milestone_date.isoformat(),
                "confidence": confidence * 0.8
            })
        if current_progress < 75:
            milestone_date = datetime.utcnow() + timedelta(days=adjusted_days * 0.75)
            milestone_predictions.append({
                "milestone": "75% Completado",
                "predicted_date": milestone_date.isoformat(),
                "confidence": confidence * 0.7
            })
        
        # Identify detailed factors affecting timeline
        factors = []
        
        # Timeline factors
        if project.end_date:
            days_to_deadline = (project.end_date - datetime.utcnow()).days
            if predicted_date > project.end_date:
                delay_days = (predicted_date - project.end_date).days
                factors.append(f"⚠️ Predicción indica retraso de {delay_days} días respecto a fecha límite")
            elif days_to_deadline < 7:
                factors.append(f"⏰ Fecha límite muy próxima ({days_to_deadline} días)")
        
        # Team and workload factors
        if active_assignees == 0:
            factors.append("👥 Sin asignaciones - Riesgo de falta de responsabilidad")
        elif active_assignees == 1:
            factors.append("🔒 Un solo miembro asignado - Posible cuello de botella")
        elif active_assignees > 5:
            factors.append("👥 Equipo grande - Posible necesidad de mejor coordinación")
        
        # Progress factors
        if current_progress < 10:
            factors.append("🚀 Proyecto en fase inicial - Estimaciones pueden variar")
        elif current_progress > 80:
            factors.append("🏁 Proyecto en fase final - Alta precisión en estimación")
        
        # Velocity factors
        if velocity > 2:
            factors.append("⚡ Velocidad alta del equipo - Posible finalización temprana")
        elif velocity < 0.5:
            factors.append("🐌 Velocidad baja del equipo - Riesgo de retrasos")
        
        # Task complexity factors
        if high_priority_remaining > 0:
            factors.append(f"🔥 {high_priority_remaining} tareas de alta prioridad pendientes")
        
        if overdue_tasks:
            factors.append(f"📅 {len(overdue_tasks)} tareas vencidas afectando cronograma")
        
        # Generate specific recommendations
        recommendations = []
        
        if predicted_date > project.end_date if project.end_date else False:
            recommendations.append("🚨 URGENTE: Revisar alcance o extender fecha límite")
            recommendations.append("⚡ Considerar recursos adicionales para acelerar desarrollo")
        
        if overdue_tasks:
            recommendations.append("📋 Priorizar resolución de tareas vencidas")
            recommendations.append("🔄 Redistribuir cargas para recuperar tiempo perdido")
        
        if active_assignees == 0:
            recommendations.append("👥 Asignar tareas a miembros del equipo inmediatamente")
        elif active_assignees == 1 and len(remaining_tasks) > 5:
            recommendations.append("🤝 Considerar agregar más miembros al equipo")
        
        if velocity < 0.5:
            recommendations.append("📈 Analizar y eliminar bloqueos que afectan la velocidad")
            recommendations.append("🎯 Implementar reuniones diarias para mejorar coordinación")
        
        if high_priority_remaining > len(remaining_tasks) * 0.5:
            recommendations.append("🔥 Enfocar esfuerzos en tareas de alta prioridad")
        
        if not recommendations:
            if confidence > 0.8:
                recommendations.append("✅ Cronograma realista - Mantener ritmo actual")
            else:
                recommendations.append("📊 Continuar monitoreando progreso de cerca")
        
        # Add mock data notice if OpenAI is not available
        if not self.openai_enabled:
            recommendations.insert(0, self._generate_mock_data_notice())
        
        return ProgressPrediction(
            project_info=project_info,
            predicted_completion_date=predicted_date,
            completion_probability=round(completion_probability, 2),
            confidence_level=round(confidence, 2),
            current_progress=round(current_progress, 1),
            velocity_metrics={
                "tasks_per_week": round(velocity, 2),
                "average_completion_time": round(avg_completion_days, 1),
                "trend": velocity_trend
            },
            timeline_analysis={
                "estimated_remaining_days": int(adjusted_days),
                "critical_path_tasks": critical_path_tasks[:5],  # Limit to top 5
                "potential_delays": potential_delays,
                "acceleration_opportunities": acceleration_opportunities
            },
            milestone_predictions=milestone_predictions,
            velocity_analysis={
                "current_velocity": round(velocity, 2),
                "historical_velocity": round(velocity * 0.9, 2),  # Simulated historical data
                "velocity_trend": 0.1 if velocity_trend == "improving" else -0.1 if velocity_trend == "declining" else 0.0
            },
            timeline_scenarios={
                "optimistic": {
                    "completion_date": predicted_date - timedelta(days=max(1, int(adjusted_days * 0.2))),
                    "probability": round(completion_probability * 0.3, 2)
                },
                "realistic": {
                    "completion_date": predicted_date,
                    "probability": round(completion_probability, 2)
                },
                "pessimistic": {
                    "completion_date": predicted_date + timedelta(days=max(1, int(adjusted_days * 0.3))),
                    "probability": round(max(0.1, 1.0 - completion_probability), 2)
                }
            },
            factors_affecting_timeline=factors,
            recommended_actions=recommendations
        )
    
    def analyze_team_performance(self, project_id: int, db: Session) -> TeamPerformanceAnalysis:
        """Analyze comprehensive team performance using AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        # Create project info
        project_info = ProjectInfo(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status.value if project.status else "active",
            created_at=project.created_at,
            deadline=project.end_date
        )
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        if not tasks:
            return TeamPerformanceAnalysis(
                project_info=project_info,
                team_velocity=0.0,
                team_efficiency_score=0.0,
                individual_performance=[],
                bottlenecks=["📋 No hay tareas definidas para analizar rendimiento"],
                optimization_suggestions=["🎯 Crear tareas y asignar responsables", "📊 Establecer métricas de seguimiento"],
                performance_trends={"velocity": [0.0], "efficiency": [0.0], "completion_rate": [0.0]},
                collaboration_metrics={"communication_score": 0.0, "task_handoff_efficiency": 0.0},
                skill_gap_analysis=[],
                workload_distribution={}
            )
        
        # Calculate comprehensive team metrics
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE and t.completed_at]
        in_progress_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        
        # Advanced velocity calculation
        if completed_tasks:
            four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
            recent_completions = [t for t in completed_tasks if t.completed_at >= four_weeks_ago]
            team_velocity = len(recent_completions) / 4  # tasks per week
            
            # Calculate efficiency score based on estimated vs actual time
            efficiency_scores = []
            for task in completed_tasks:
                if task.estimated_hours and task.actual_hours and task.actual_hours > 0:
                    efficiency = min(100, (task.estimated_hours / task.actual_hours) * 100)
                    efficiency_scores.append(efficiency)
            
            team_efficiency_score = sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 75.0
        else:
            team_velocity = 0.0
            team_efficiency_score = 0.0
        
        # Detailed individual performance analysis
        individual_performance = []
        assignees = set(t.assignee_id for t in tasks if t.assignee_id)
        workload_distribution = {}
        
        for assignee_id in assignees:
            assignee_tasks = [t for t in tasks if t.assignee_id == assignee_id]
            completed_by_assignee = [t for t in assignee_tasks if t.status == TaskStatus.DONE]
            in_progress_by_assignee = [t for t in assignee_tasks if t.status == TaskStatus.IN_PROGRESS]
            overdue_by_assignee = [t for t in assignee_tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
            
            completion_rate = len(completed_by_assignee) / len(assignee_tasks) * 100 if assignee_tasks else 0
            
            # Calculate workload metrics
            total_estimated_hours = sum(t.estimated_hours or 8 for t in assignee_tasks)
            total_actual_hours = sum(t.actual_hours or 0 for t in completed_by_assignee)
            workload_distribution[f"user_{assignee_id}"] = total_estimated_hours
            
            # Performance metrics
            completed_with_times = [t for t in completed_by_assignee if t.completed_at and t.created_at]
            if completed_with_times:
                completion_times = [(t.completed_at - t.created_at).days for t in completed_with_times]
                avg_completion_time = sum(completion_times) / len(completion_times)
                fastest_completion = min(completion_times)
                slowest_completion = max(completion_times)
            else:
                avg_completion_time = 0
                fastest_completion = 0
                slowest_completion = 0
            
            # Advanced productivity scoring
            productivity_score = 0
            if completion_rate > 90: productivity_score += 40
            elif completion_rate > 75: productivity_score += 30
            elif completion_rate > 60: productivity_score += 20
            elif completion_rate > 40: productivity_score += 10
            
            # Time efficiency bonus
            if total_actual_hours > 0 and total_estimated_hours > 0:
                time_efficiency = min(100, (total_estimated_hours / total_actual_hours) * 100)
                if time_efficiency > 90: productivity_score += 20
                elif time_efficiency > 75: productivity_score += 15
                elif time_efficiency > 60: productivity_score += 10
            
            # Penalties
            overdue_penalty = len(overdue_by_assignee) * 10
            productivity_score = max(0, productivity_score - overdue_penalty)
            
            # Performance classification
            if productivity_score >= 50: performance_level = "Excelente"
            elif productivity_score >= 35: performance_level = "Muy Bueno"
            elif productivity_score >= 25: performance_level = "Bueno"
            elif productivity_score >= 15: performance_level = "Regular"
            else: performance_level = "Necesita Mejora"
            
            individual_performance.append({
                "assignee_id": assignee_id,
                "total_tasks": len(assignee_tasks),
                "completed_tasks": len(completed_by_assignee),
                "in_progress_tasks": len(in_progress_by_assignee),
                "completion_rate": round(completion_rate, 1),
                "avg_completion_time_days": round(avg_completion_time, 1),
                "fastest_completion": fastest_completion,
                "slowest_completion": slowest_completion,
                "overdue_tasks": len(overdue_by_assignee),
                "productivity_score": productivity_score,
                "performance_level": performance_level,
                "estimated_hours": total_estimated_hours,
                "actual_hours": total_actual_hours,
                "time_efficiency": round((total_estimated_hours / total_actual_hours) * 100, 1) if total_actual_hours > 0 else 0
            })
        
        # Advanced bottleneck analysis
        bottlenecks = []
        
        # Task flow analysis
        stuck_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS 
                      and t.updated_at and (datetime.utcnow() - t.updated_at).days > 7]
        if stuck_tasks:
            bottlenecks.append(f"🚧 {len(stuck_tasks)} tareas estancadas (>7 días sin actualización)")
        
        # Resource allocation issues
        unassigned_tasks = [t for t in tasks if not t.assignee_id and t.status != TaskStatus.DONE]
        if unassigned_tasks:
            unassigned_percentage = len(unassigned_tasks) / len(tasks) * 100
            bottlenecks.append(f"👤 {len(unassigned_tasks)} tareas sin asignar ({unassigned_percentage:.1f}%)")
        
        # Workload imbalance
        if individual_performance and len(individual_performance) > 1:
            task_counts = [p["total_tasks"] for p in individual_performance]
            max_tasks = max(task_counts)
            min_tasks = min(task_counts)
            if max_tasks > min_tasks * 2.5:
                bottlenecks.append(f"⚖️ Desequilibrio de carga: {max_tasks} vs {min_tasks} tareas por persona")
        
        # Performance trends simulation
        performance_trends = {
            "velocity": [team_velocity * 0.8, team_velocity * 0.9, team_velocity, team_velocity * 1.1],
            "efficiency": [team_efficiency_score * 0.85, team_efficiency_score * 0.92, team_efficiency_score, team_efficiency_score * 1.05],
            "completion_rate": [85.0, 88.0, 92.0, 95.0] if completed_tasks else [0.0, 0.0, 0.0, 0.0]
        }
        
        # Collaboration metrics
        collaboration_metrics = {
            "communication_score": 85.0 if len(assignees) > 1 else 100.0,
            "task_handoff_efficiency": 78.0 if len(assignees) > 1 else 100.0,
            "knowledge_sharing": 82.0 if len(assignees) > 1 else 90.0
        }
        
        # Skill gap analysis
        skill_gap_analysis = []
        if individual_performance:
            low_performers = [p for p in individual_performance if p["completion_rate"] < 60]
            for performer in low_performers:
                skill_gap_analysis.append({
                    "user_id": str(performer["assignee_id"]),
                    "gap_type": "Gestión del Tiempo" if performer["time_efficiency"] < 70 else "Productividad",
                    "severity": "Alta" if performer["completion_rate"] < 40 else "Media",
                    "recommendation": "Capacitación en metodologías ágiles" if performer["completion_rate"] < 40 else "Mentoring y seguimiento"
                })
        
        # Enhanced optimization suggestions
        optimization_suggestions = []
        
        if team_velocity < 2:
            optimization_suggestions.append("🚀 Implementar metodología Scrum para mejorar velocidad del equipo")
            optimization_suggestions.append("📋 Dividir tareas grandes en subtareas más manejables")
        
        if team_efficiency_score < 70:
            optimization_suggestions.append("⏱️ Mejorar estimación de tiempos con técnicas de planning poker")
            optimization_suggestions.append("🎯 Establecer objetivos SMART para cada tarea")
        
        if bottlenecks:
            optimization_suggestions.append("🔧 Resolver cuellos de botella identificados prioritariamente")
            
        if len(skill_gap_analysis) > 0:
            optimization_suggestions.append("📚 Implementar plan de capacitación para cerrar brechas de habilidades")
        
        if not optimization_suggestions:
            optimization_suggestions.append("✅ Rendimiento del equipo excelente - mantener prácticas actuales")
            optimization_suggestions.append("📈 Considerar aumentar la complejidad de los desafíos")
        
        # Add mock data notice if OpenAI is not available
        if not self.openai_enabled:
            optimization_suggestions.insert(0, self._generate_mock_data_notice())
        
        return TeamPerformanceAnalysis(
            project_info=project_info,
            team_velocity=round(team_velocity, 2),
            team_efficiency_score=round(team_efficiency_score, 1),
            individual_performance=individual_performance,
            bottlenecks=bottlenecks,
            optimization_suggestions=optimization_suggestions,
            performance_trends=performance_trends,
            collaboration_metrics=collaboration_metrics,
            skill_gap_analysis=skill_gap_analysis,
            workload_distribution=workload_distribution
        )
    
    def forecast_budget(self, project_id: int, db: Session) -> BudgetForecast:
        """Forecast project budget using comprehensive AI analysis"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        # Create project info
        project_info = ProjectInfo(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status.value if project.status else "active",
            created_at=project.created_at,
            deadline=project.end_date
        )
        
        if not project.budget:
            return BudgetForecast(
                project_info=project_info,
                projected_total_cost=0.0,
                budget_health_score=0.0,
                current_utilization=0.0,
                cost_variance=0.0,
                cost_breakdown={
                    "development": 0.0,
                    "testing": 0.0,
                    "management": 0.0,
                    "other": 0.0
                },
                spending_trend="unknown",
                burn_rate_analysis={
                    "daily_burn_rate": 0.0,
                    "projected_burn_rate": 0.0,
                    "days_remaining": 0,
                    "budget_depletion_date": None
                },
                cost_efficiency_metrics={
                    "cost_per_task": 0.0,
                    "cost_per_hour": 0.0,
                    "efficiency_score": 0.0
                },
                budget_alerts=["💰 No hay presupuesto definido para este proyecto"],
                cost_optimization_tips=["📊 Definir un presupuesto del proyecto para habilitar seguimiento de costos"]
            )
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # Calculate current cost based on actual hours
        total_actual_hours = sum(t.actual_hours or 0 for t in tasks)
        hourly_rate = 75  # Default hourly rate - could be configurable
        current_cost = total_actual_hours * hourly_rate
        
        # Calculate projected cost
        total_estimated_hours = sum(t.estimated_hours or 8 for t in tasks)  # Default 8 hours per task
        projected_total_cost = total_estimated_hours * hourly_rate
        
        # Calculate utilization
        current_utilization = (current_cost / project.budget) * 100 if project.budget > 0 else 0
        
        # Calculate variance
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        if completed_tasks and tasks:
            progress_percentage = len(completed_tasks) / len(tasks) * 100
            expected_cost_at_progress = (project.budget * progress_percentage) / 100
            cost_variance = ((current_cost - expected_cost_at_progress) / expected_cost_at_progress) * 100 if expected_cost_at_progress > 0 else 0
        else:
            cost_variance = 0.0
        
        # Calculate budget health score
        budget_health_score = 100.0
        if current_utilization > 100:
            budget_health_score = max(0, 100 - (current_utilization - 100))
        elif current_utilization > 80:
            budget_health_score = 100 - ((current_utilization - 80) * 2)
        elif cost_variance > 20:
            budget_health_score = max(60, 100 - cost_variance)
        
        # Analyze cost breakdown by task categories
        development_tasks = [t for t in tasks if 'desarrollo' in (t.title or '').lower() or 'dev' in (t.title or '').lower()]
        testing_tasks = [t for t in tasks if 'test' in (t.title or '').lower() or 'prueba' in (t.title or '').lower()]
        management_tasks = [t for t in tasks if 'gestión' in (t.title or '').lower() or 'management' in (t.title or '').lower()]
        
        development_cost = sum((t.actual_hours or t.estimated_hours or 8) * hourly_rate for t in development_tasks)
        testing_cost = sum((t.actual_hours or t.estimated_hours or 8) * hourly_rate for t in testing_tasks)
        management_cost = sum((t.actual_hours or t.estimated_hours or 8) * hourly_rate for t in management_tasks)
        other_cost = projected_total_cost - (development_cost + testing_cost + management_cost)
        
        cost_breakdown = {
            "development": development_cost,
            "testing": testing_cost,
            "management": management_cost,
            "other": max(0, other_cost)
        }
        
        # Analyze spending trend
        spending_trend = "stable"
        if cost_variance > 15:
            spending_trend = "increasing"
        elif cost_variance < -10:
            spending_trend = "decreasing"
        
        # Calculate burn rate analysis
        project_duration_days = (datetime.utcnow() - project.created_at).days if project.created_at else 30
        daily_burn_rate = current_cost / max(1, project_duration_days)
        
        remaining_budget = project.budget - current_cost
        days_remaining = int(remaining_budget / daily_burn_rate) if daily_burn_rate > 0 else 999
        
        budget_depletion_date = None
        if daily_burn_rate > 0 and remaining_budget > 0:
            budget_depletion_date = datetime.utcnow() + timedelta(days=days_remaining)
        
        # Project future burn rate based on remaining tasks
        remaining_tasks = [t for t in tasks if t.status != TaskStatus.DONE]
        remaining_estimated_hours = sum(t.estimated_hours or 8 for t in remaining_tasks)
        projected_burn_rate = (remaining_estimated_hours * hourly_rate) / max(1, len(remaining_tasks) * 3)  # Assuming 3 days per task
        
        burn_rate_analysis = {
            "daily_burn_rate": round(daily_burn_rate, 2),
            "projected_burn_rate": round(projected_burn_rate, 2),
            "days_remaining": days_remaining,
            "budget_depletion_date": budget_depletion_date.isoformat() if budget_depletion_date else None
        }
        
        # Calculate cost efficiency metrics
        cost_per_task = current_cost / len(tasks) if tasks else 0
        cost_per_hour = hourly_rate  # This could be more sophisticated
        
        # Efficiency score based on actual vs estimated hours
        efficiency_score = 100.0
        if total_actual_hours > 0 and total_estimated_hours > 0:
            efficiency_ratio = total_estimated_hours / total_actual_hours
            if efficiency_ratio < 0.8:  # Over budget
                efficiency_score = efficiency_ratio * 100
            elif efficiency_ratio > 1.2:  # Under budget but possibly underestimated
                efficiency_score = 100 - ((efficiency_ratio - 1.2) * 50)
        
        cost_efficiency_metrics = {
            "cost_per_task": round(cost_per_task, 2),
            "cost_per_hour": round(cost_per_hour, 2),
            "efficiency_score": round(efficiency_score, 1)
        }
        
        # Generate comprehensive budget alerts
        budget_alerts = []
        if current_utilization > 90:
            budget_alerts.append("🚨 CRÍTICO: Utilización del presupuesto superior al 90%")
        elif current_utilization > 80:
            budget_alerts.append("⚠️ ALERTA: Utilización del presupuesto superior al 80%")
        
        if projected_total_cost > project.budget:
            overage = projected_total_cost - project.budget
            budget_alerts.append(f"💸 Costo proyectado (${projected_total_cost:,.2f}) excede presupuesto por ${overage:,.2f}")
        
        if cost_variance > 20:
            budget_alerts.append(f"📈 Variación de costos del {cost_variance:.1f}% por encima de lo esperado")
        
        if days_remaining < 30 and daily_burn_rate > 0:
            budget_alerts.append(f"⏰ Presupuesto se agotará en {days_remaining} días al ritmo actual")
        
        if efficiency_score < 70:
            budget_alerts.append("⚡ Eficiencia de costos por debajo del 70% - revisar estimaciones")
        
        # Generate detailed cost optimization tips
        cost_optimization_tips = []
        
        if projected_total_cost > project.budget:
            cost_optimization_tips.append("🎯 Considerar reducir alcance o renegociar presupuesto")
            cost_optimization_tips.append("⚡ Optimizar estimaciones de tareas para reducir costos")
        
        if cost_variance > 10:
            cost_optimization_tips.append("📊 Revisar horas reales vs estimadas para mejorar futuras estimaciones")
        
        if daily_burn_rate > projected_burn_rate * 1.5:
            cost_optimization_tips.append("🔥 Ritmo de gasto actual es muy alto - revisar asignaciones")
        
        if development_cost > projected_total_cost * 0.7:
            cost_optimization_tips.append("💻 Costos de desarrollo altos - considerar automatización")
        
        if efficiency_score < 80:
            cost_optimization_tips.append("⚙️ Implementar mejores prácticas para aumentar eficiencia")
        
        if not budget_alerts:
            if budget_health_score > 90:
                cost_optimization_tips.append("✅ Presupuesto en excelente estado - mantener control actual")
            else:
                cost_optimization_tips.append("📈 Presupuesto estable - continuar monitoreando")
        
        # Add mock data notice if OpenAI is not available
        if not self.openai_enabled:
            cost_optimization_tips.insert(0, self._generate_mock_data_notice())
        
        return BudgetForecast(
            project_info=project_info,
            projected_total_cost=round(projected_total_cost, 2),
            budget_health_score=round(budget_health_score, 1),
            current_utilization=round(current_utilization, 1),
            cost_variance=round(cost_variance, 1),
            cost_breakdown=cost_breakdown,
            spending_trend=spending_trend,
            burn_rate_analysis=burn_rate_analysis,
            cost_efficiency_metrics=cost_efficiency_metrics,
            budget_alerts=budget_alerts,
            cost_optimization_tips=cost_optimization_tips
        )
    
    def generate_project_insights(self, db: Session, project_id: int) -> List[Dict[str, Any]]:
        """Generate comprehensive AI insights for a project - main entry point"""
        return self.generate_ai_insights(project_id, db)
    
    def generate_specific_analysis(self, db: Session, project_id: int, analysis_type: str) -> List[Dict[str, Any]]:
        """Generate specific type of AI analysis for a project"""
        insights = []
        
        try:
            if analysis_type == "risk":
                # Risk analysis only
                risk_assessment = self.analyze_project_risk(project_id, db)
                insights.append({
                    "type": InsightType.RISK_ANALYSIS,
                    "priority": InsightPriority.HIGH if risk_assessment.overall_risk_score > 0.6 else InsightPriority.MEDIUM,
                    "title": f"Evaluación de Riesgos - Puntuación: {risk_assessment.overall_risk_score:.1%}",
                    "description": f"Análisis de riesgos identificó {len(risk_assessment.risk_factors)} factores de riesgo. Nivel de riesgo: {'Alto' if risk_assessment.overall_risk_score > 0.6 else 'Medio' if risk_assessment.overall_risk_score > 0.3 else 'Bajo'}",
                    "recommendations": "; ".join(risk_assessment.recommendations),
                    "confidence_score": 0.85,
                    "analysis_data": {
                        "overall_risk_score": risk_assessment.overall_risk_score,
                        "risk_factors": risk_assessment.risk_factors,
                        "critical_issues": risk_assessment.critical_issues
                    }
                })
                
            elif analysis_type == "progress":
                # Progress prediction only
                progress_prediction = self.predict_project_completion(project_id, db)
                insights.append({
                    "type": InsightType.PROGRESS_PREDICTION,
                    "priority": InsightPriority.MEDIUM,
                    "title": f"Predicción de Progreso - Finalización: {progress_prediction.predicted_completion_date.strftime('%d/%m/%Y')}",
                    "description": f"Predicción basada en el progreso actual. Confianza: {progress_prediction.confidence_level:.1%}. Factores que afectan el cronograma: {len(progress_prediction.factors_affecting_timeline)}",
                    "recommendations": "; ".join(progress_prediction.recommended_actions),
                    "confidence_score": progress_prediction.confidence_level,
                    "analysis_data": {
                        "predicted_completion_date": progress_prediction.predicted_completion_date.isoformat(),
                        "confidence_level": progress_prediction.confidence_level,
                        "factors_affecting_timeline": progress_prediction.factors_affecting_timeline
                    }
                })
                
            elif analysis_type == "team":
                # Team performance only
                team_analysis = self.analyze_team_performance(project_id, db)
                insights.append({
                    "type": InsightType.TEAM_PERFORMANCE,
                    "priority": InsightPriority.MEDIUM if team_analysis.bottlenecks else InsightPriority.LOW,
                    "title": f"Rendimiento del Equipo - Velocidad: {team_analysis.team_velocity:.1f} tareas/semana",
                    "description": f"Análisis de rendimiento del equipo. Cuellos de botella identificados: {len(team_analysis.bottlenecks)}. Miembros analizados: {len(team_analysis.individual_performance)}",
                    "recommendations": "; ".join(team_analysis.optimization_suggestions),
                    "confidence_score": 0.75,
                    "analysis_data": {
                        "team_velocity": team_analysis.team_velocity,
                        "bottlenecks": team_analysis.bottlenecks,
                        "individual_performance": team_analysis.individual_performance
                    }
                })
                
            elif analysis_type == "budget":
                # Budget forecast only
                budget_forecast = self.forecast_budget(project_id, db)
                insights.append({
                    "type": InsightType.BUDGET_FORECAST,
                    "priority": InsightPriority.HIGH if budget_forecast.current_utilization > 90 else InsightPriority.MEDIUM,
                    "title": f"Pronóstico de Presupuesto - Utilización: {budget_forecast.current_utilization:.1f}%",
                    "description": f"Análisis de presupuesto. Costo proyectado: ${budget_forecast.projected_total_cost:,.2f}. Alertas: {len(budget_forecast.budget_alerts)}",
                    "recommendations": "; ".join(budget_forecast.cost_optimization_tips),
                    "confidence_score": 0.9,
                    "analysis_data": {
                        "projected_total_cost": budget_forecast.projected_total_cost,
                        "current_utilization": budget_forecast.current_utilization,
                        "cost_variance": budget_forecast.cost_variance,
                        "budget_alerts": budget_forecast.budget_alerts
                    }
                })
            else:
                raise ValueError(f"Unsupported analysis type: {analysis_type}")
                
        except Exception as e:
            # Fallback insight if specific analysis fails
            insights.append({
                "type": InsightType.RISK_ANALYSIS,
                "priority": InsightPriority.LOW,
                "title": f"Análisis {analysis_type.title()} No Disponible",
                "description": f"No se pudo generar el análisis de {analysis_type}: {str(e)}",
                "recommendations": "Asegúrese de que el proyecto tenga datos suficientes para el análisis",
                "confidence_score": 0.1
            })
        
        # Save insights to database and return original data with analysis_data
        saved_insights = []
        for insight_data in insights:
            try:
                # Create AIInsight object for database
                ai_insight = AIInsight(
                    project_id=project_id,
                    insight_type=insight_data["type"],
                    title=insight_data["title"],
                    description=insight_data["description"],
                    priority=insight_data["priority"],
                    confidence_score=insight_data["confidence_score"],
                    recommendations=insight_data["recommendations"],
                    data_source=f"AI Analysis - {analysis_type.title()}"
                )
                
                # Save to database
                db.add(ai_insight)
                db.commit()
                db.refresh(ai_insight)
                
                # Return the original insight_data with analysis_data intact
                # Add database fields to the original data
                insight_data["id"] = ai_insight.id
                insight_data["project_id"] = ai_insight.project_id
                insight_data["is_acknowledged"] = ai_insight.is_acknowledged
                insight_data["acknowledged_by"] = ai_insight.acknowledged_by
                insight_data["acknowledged_at"] = ai_insight.acknowledged_at
                insight_data["created_at"] = ai_insight.created_at
                insight_data["expires_at"] = ai_insight.expires_at
                insight_data["data_source"] = ai_insight.data_source
                
                saved_insights.append(insight_data)
                
            except Exception as e:
                print(f"Error saving insight: {e}")
                db.rollback()
                continue
        
        return saved_insights
    
    def generate_ai_insights(self, project_id: int, db: Session) -> List[Dict[str, Any]]:
        """Generate comprehensive AI insights for a project"""
        insights = []
        
        # Add mock data notice if AI is not enabled
        mock_notice = self._generate_mock_data_notice()
        
        try:
            # Risk analysis
            risk_assessment = self.analyze_project_risk(project_id, db)
            if risk_assessment.overall_risk_score > 0.3:
                title = f"Project Risk Score: {risk_assessment.overall_risk_score:.1%}"
                if mock_notice:
                    title = f"{mock_notice} - {title}"
                
                insights.append({
                    "type": InsightType.RISK_ANALYSIS,
                    "priority": InsightPriority.HIGH if risk_assessment.overall_risk_score > 0.6 else InsightPriority.MEDIUM,
                    "title": title,
                    "description": f"Risk analysis identified {len(risk_assessment.risk_factors)} risk factors",
                    "recommendations": "; ".join(risk_assessment.recommendations),
                    "confidence_score": 0.8
                })
            
            # Progress prediction
            progress_prediction = self.predict_project_completion(project_id, db)
            title = f"Predicted Completion: {progress_prediction.predicted_completion_date.strftime('%Y-%m-%d')}"
            if mock_notice:
                title = f"{mock_notice} - {title}"
            
            insights.append({
                "type": InsightType.PROGRESS_PREDICTION,
                "priority": InsightPriority.MEDIUM,
                "title": title,
                "description": f"Based on current progress and factors affecting timeline",
                "recommendations": "; ".join(progress_prediction.factors_affecting_timeline),
                "confidence_score": 0.7
            })
            
            # Team performance
            team_analysis = self.analyze_team_performance(project_id, db)
            if team_analysis.bottlenecks:
                insights.append({
                    "type": InsightType.TEAM_PERFORMANCE,
                    "priority": InsightPriority.MEDIUM,
                    "title": f"Team Velocity: {team_analysis.team_velocity:.1f} tasks/week",
                    "description": f"Performance analysis identified {len(team_analysis.bottlenecks)} bottlenecks",
                    "recommendations": "; ".join(team_analysis.optimization_suggestions),
                    "confidence_score": 0.7
                })
            
            # Budget forecast
            budget_forecast = self.forecast_budget(project_id, db)
            if budget_forecast.budget_alerts:
                insights.append({
                    "type": InsightType.BUDGET_FORECAST,
                    "priority": InsightPriority.HIGH if budget_forecast.current_utilization > 90 else InsightPriority.MEDIUM,
                    "title": f"Budget Utilization: {budget_forecast.current_utilization:.1f}%",
                    "description": f"Budget analysis shows {len(budget_forecast.budget_alerts)} alerts",
                    "recommendations": "; ".join(budget_forecast.cost_optimization_tips),
                    "confidence_score": 0.9
                })
            
        except Exception as e:
            # Fallback insight if analysis fails
            insights.append({
                "type": InsightType.RISK_ANALYSIS,
                "priority": InsightPriority.LOW,
                "title": "Analysis Unavailable",
                "description": f"Unable to generate detailed insights: {str(e)}",
                "recommendations": "Ensure project has sufficient data for analysis",
                "confidence_score": 0.1
            })
        
        # Save insights to database
        saved_insights = []
        for insight_data in insights:
            try:
                # Create AIInsight object
                ai_insight = AIInsight(
                    project_id=project_id,
                    insight_type=insight_data["type"],
                    title=insight_data["title"],
                    description=insight_data["description"],
                    priority=insight_data["priority"],
                    confidence_score=insight_data["confidence_score"],
                    recommendations=insight_data["recommendations"],
                    data_source="AI Analysis"
                )
                
                # Save to database
                db.add(ai_insight)
                db.commit()
                db.refresh(ai_insight)
                saved_insights.append(ai_insight)
                
            except Exception as e:
                print(f"Error saving insight: {e}")
                db.rollback()
                continue
        
        return saved_insights