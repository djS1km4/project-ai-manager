import openai
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus, TaskPriority
from ..models.ai_insight import (
    AIInsight, InsightType, InsightPriority, ProjectAnalytics,
    RiskAssessment, ProgressPrediction, TeamPerformanceAnalysis, BudgetForecast, ProjectInfo
)
from dotenv import load_dotenv

load_dotenv()

class DeepseekAIService:
    """Service for AI analysis using Deepseek via OpenRouter"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek/deepseek-chat:free")
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", "1000"))
        self.ai_provider = os.getenv("AI_PROVIDER", "deepseek")
        
        # Check if Deepseek is properly configured
        self.deepseek_enabled = (
            self.api_key and 
            self.api_key != "sk-or-v1-PLACEHOLDER-GET-FROM-OPENROUTER" and
            self.api_key.startswith("sk-or-")
        )
        
        if self.deepseek_enabled:
            # Configure OpenAI client to use OpenRouter
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
    
    def is_enabled(self) -> bool:
        """Check if Deepseek service is properly configured and enabled"""
        return self.deepseek_enabled
    
    def _call_deepseek_api(self, prompt: str, system_message: str = None) -> str:
        """Make a call to Deepseek API via OpenRouter"""
        if not self.deepseek_enabled:
            raise ValueError("Deepseek API is not properly configured")
        
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error calling Deepseek API: {str(e)}")
    
    def analyze_project_risk(self, project_id: int, db: Session) -> RiskAssessment:
        """Analyze project risks using Deepseek AI"""
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
            return RiskAssessment(
                project_info=project_info,
                overall_risk_score=0.1,
                risk_level="Bajo",
                risk_factors=[],
                recommendations=["📋 Crear tareas para poder evaluar riesgos del proyecto"],
                critical_issues=[],
                risk_categories={
                    "schedule_risk": 0.0,
                    "resource_risk": 0.0,
                    "quality_risk": 0.0,
                    "budget_risk": 0.0,
                    "technical_risk": 0.0
                },
                mitigation_strategies=[],
                impact_assessment={
                    "schedule_impact": "Bajo",
                    "budget_impact": "Bajo",
                    "quality_impact": "Bajo",
                    "team_impact": "Bajo"
                },
                risk_timeline={"current": 0.1, "projected_30_days": 0.1, "projected_60_days": 0.1}
            )
        
        # Prepare data for AI analysis
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
        in_progress_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        
        # Calculate basic metrics
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        overdue_rate = (len(overdue_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
        
        # Use AI for risk analysis if enabled
        if self.deepseek_enabled:
            try:
                system_message = """Eres un experto analista de riesgos de proyectos. Analiza los datos del proyecto y proporciona una evaluación de riesgos detallada en español. 
                Responde SOLO con un JSON válido con la siguiente estructura:
                {
                    "overall_risk_score": 0.0-1.0,
                    "risk_level": "Bajo|Medio|Alto",
                    "risk_factors": [{"factor": "nombre", "severity": "low|medium|high", "description": "descripción", "impact": 0.0-1.0}],
                    "recommendations": ["recomendación1", "recomendación2"],
                    "critical_issues": ["issue1", "issue2"],
                    "mitigation_strategies": ["estrategia1", "estrategia2"]
                }"""
                
                prompt = f"""
                Analiza este proyecto:
                - Nombre: {project.name}
                - Descripción: {project.description or 'Sin descripción'}
                - Estado: {project.status.value if project.status else 'activo'}
                - Total de tareas: {total_tasks}
                - Tareas completadas: {completed_tasks} ({completion_rate:.1f}%)
                - Tareas vencidas: {len(overdue_tasks)} ({overdue_rate:.1f}%)
                - Tareas en progreso: {len(in_progress_tasks)}
                - Fecha límite: {project.end_date.strftime('%Y-%m-%d') if project.end_date else 'No definida'}
                
                Proporciona un análisis de riesgos completo considerando estos factores.
                """
                
                ai_response = self._call_deepseek_api(prompt, system_message)
                
                # Parse AI response
                try:
                    ai_analysis = json.loads(ai_response)
                    
                    return RiskAssessment(
                        project_info=project_info,
                        overall_risk_score=ai_analysis.get("overall_risk_score", 0.3),
                        risk_level=ai_analysis.get("risk_level", "Medio"),
                        risk_factors=ai_analysis.get("risk_factors", []),
                        recommendations=ai_analysis.get("recommendations", []),
                        critical_issues=ai_analysis.get("critical_issues", []),
                        risk_categories={
                            "schedule_risk": min(0.8, overdue_rate / 100),
                            "resource_risk": 0.3,
                            "quality_risk": 0.2,
                            "budget_risk": 0.2,
                            "technical_risk": 0.3
                        },
                        mitigation_strategies=ai_analysis.get("mitigation_strategies", []),
                        impact_assessment={
                            "schedule_impact": "Alto" if overdue_rate > 30 else "Medio" if overdue_rate > 10 else "Bajo",
                            "budget_impact": "Medio",
                            "quality_impact": "Bajo",
                            "team_impact": "Bajo"
                        },
                        risk_timeline={
                            "current": ai_analysis.get("overall_risk_score", 0.3),
                            "projected_30_days": min(1.0, ai_analysis.get("overall_risk_score", 0.3) + 0.1),
                            "projected_60_days": min(1.0, ai_analysis.get("overall_risk_score", 0.3) + 0.2)
                        }
                    )
                except json.JSONDecodeError:
                    # Fallback if AI response is not valid JSON
                    pass
                    
            except Exception as e:
                print(f"Error in AI risk analysis: {e}")
                # Continue with fallback analysis
        
        # Fallback analysis (rule-based)
        risk_score = 0.0
        risk_factors = []
        recommendations = []
        critical_issues = []
        
        # Schedule risk
        if overdue_rate > 30:
            risk_score += 0.4
            risk_factors.append({
                "factor": "Tareas Vencidas Críticas",
                "severity": "high",
                "description": f"{len(overdue_tasks)} tareas vencidas ({overdue_rate:.1f}%)",
                "impact": 0.4
            })
            critical_issues.append("Alto porcentaje de tareas vencidas")
            recommendations.append("🚨 Revisar cronograma y reprogramar tareas críticas")
        elif overdue_rate > 10:
            risk_score += 0.2
            risk_factors.append({
                "factor": "Tareas Vencidas",
                "severity": "medium",
                "description": f"{len(overdue_tasks)} tareas vencidas ({overdue_rate:.1f}%)",
                "impact": 0.2
            })
            recommendations.append("⚠️ Revisar cronograma y reprogramar tareas críticas")
        
        # Progress risk
        if completion_rate < 30:
            risk_score += 0.3
            risk_factors.append({
                "factor": "Progreso Lento",
                "severity": "medium",
                "description": f"Solo {completion_rate:.1f}% de tareas completadas",
                "impact": 0.3
            })
            recommendations.append("📈 Implementar plan de aceleración para cerrar brechas de habilidades")
        
        # Default recommendations
        if not recommendations:
            recommendations.append("✅ Proyecto en riesgo bajo - Continuar monitoreo")
        
        risk_level = "Alto" if risk_score > 0.6 else "Medio" if risk_score > 0.3 else "Bajo"
        
        return RiskAssessment(
            project_info=project_info,
            overall_risk_score=min(1.0, risk_score),
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations,
            critical_issues=critical_issues,
            risk_categories={
                "schedule_risk": min(0.8, overdue_rate / 100),
                "resource_risk": 0.3,
                "quality_risk": 0.2,
                "budget_risk": 0.2,
                "technical_risk": 0.3
            },
            mitigation_strategies=[
                {"strategy": "Monitoreo", "description": "Implementar monitoreo semanal de progreso"},
                {"strategy": "Objetivos", "description": "Establecer objetivos SMART para cada tarea"},
                {"strategy": "Capacitación", "description": "Implementar plan de capacitación para cerrar brechas de habilidades"}
            ],
            impact_assessment={
                "schedule_impact": "Alto" if overdue_rate > 30 else "Medio" if overdue_rate > 10 else "Bajo",
                "budget_impact": "Medio",
                "quality_impact": "Bajo",
                "team_impact": "Bajo"
            },
            risk_timeline={
                "current": min(1.0, risk_score),
                "projected_30_days": min(1.0, risk_score + 0.1),
                "projected_60_days": min(1.0, risk_score + 0.2)
            }
        )
    
    def predict_project_completion(self, project_id: int, db: Session) -> ProgressPrediction:
        """Predict project completion using Deepseek AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
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
            predicted_date = datetime.utcnow() + timedelta(days=30)
            return ProgressPrediction(
                project_info=project_info,
                predicted_completion_date=predicted_date,
                confidence_level=0.3,
                current_progress_percentage=0.0,
                estimated_remaining_days=30,
                factors_affecting_timeline=["📋 Sin tareas definidas - Estimación basada en promedio de proyectos"],
                milestone_predictions=[],
                resource_requirements=[],
                bottleneck_analysis=[]
            )
        
        # Calculate current metrics
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        # Use AI for prediction if enabled
        if self.deepseek_enabled:
            try:
                system_message = """Eres un experto en gestión de proyectos. Analiza los datos del proyecto y predice la fecha de finalización. 
                Responde SOLO con un JSON válido con la siguiente estructura:
                {
                    "estimated_days_remaining": número,
                    "confidence_level": 0.0-1.0,
                    "factors_affecting_timeline": ["factor1", "factor2"],
                    "bottleneck_analysis": ["bottleneck1", "bottleneck2"],
                    "resource_requirements": ["recurso1", "recurso2"]
                }"""
                
                prompt = f"""
                Analiza este proyecto para predecir su finalización:
                - Nombre: {project.name}
                - Total de tareas: {total_tasks}
                - Tareas completadas: {completed_tasks} ({progress_percentage:.1f}%)
                - Fecha de inicio: {project.created_at.strftime('%Y-%m-%d')}
                - Fecha límite: {project.end_date.strftime('%Y-%m-%d') if project.end_date else 'No definida'}
                - Días transcurridos: {(datetime.utcnow() - project.created_at).days}
                
                Proporciona una predicción realista de finalización.
                """
                
                ai_response = self._call_deepseek_api(prompt, system_message)
                ai_analysis = json.loads(ai_response)
                
                estimated_days = ai_analysis.get("estimated_days_remaining", 30)
                predicted_date = datetime.utcnow() + timedelta(days=estimated_days)
                
                return ProgressPrediction(
                    project_info=project_info,
                    predicted_completion_date=predicted_date,
                    confidence_level=ai_analysis.get("confidence_level", 0.7),
                    current_progress_percentage=progress_percentage,
                    estimated_remaining_days=estimated_days,
                    factors_affecting_timeline=ai_analysis.get("factors_affecting_timeline", []),
                    milestone_predictions=[],
                    resource_requirements=ai_analysis.get("resource_requirements", []),
                    bottleneck_analysis=ai_analysis.get("bottleneck_analysis", [])
                )
                
            except Exception as e:
                print(f"Error in AI progress prediction: {e}")
                # Continue with fallback analysis
        
        # Fallback prediction (rule-based)
        if progress_percentage > 0:
            days_elapsed = (datetime.utcnow() - project.created_at).days
            estimated_total_days = (days_elapsed / progress_percentage) * 100
            remaining_days = max(1, int(estimated_total_days - days_elapsed))
        else:
            remaining_days = 60  # Default estimate
        
        predicted_date = datetime.utcnow() + timedelta(days=remaining_days)
        
        return ProgressPrediction(
            project_info=project_info,
            predicted_completion_date=predicted_date,
            confidence_level=0.6 if progress_percentage > 20 else 0.4,
            completion_probability=0.8 if progress_percentage > 50 else 0.6,
            factors_affecting_timeline=[
                f"📊 Progreso actual: {progress_percentage:.1f}%",
                f"⏱️ Velocidad estimada basada en {(datetime.utcnow() - project.created_at).days} días transcurridos"
            ],
            recommended_actions=[
                "📋 Continuar con el cronograma actual",
                "⏰ Monitorear progreso semanalmente"
            ],
            milestone_predictions=[],
            velocity_analysis={
                "current_velocity": 0.5,
                "historical_velocity": 0.4,
                "velocity_trend": 0.1
            },
            timeline_scenarios={
                "optimistic": {"completion_date": predicted_date - timedelta(days=5), "probability": 0.2},
                "realistic": {"completion_date": predicted_date, "probability": 0.6},
                "pessimistic": {"completion_date": predicted_date + timedelta(days=10), "probability": 0.2}
            }
        )