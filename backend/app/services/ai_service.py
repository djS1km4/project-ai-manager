import openai
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus
from ..models.ai_insight import (
    AIInsight, InsightType, InsightPriority, ProjectAnalytics,
    RiskAssessment, ProgressPrediction, TeamPerformanceAnalysis, BudgetForecast
)
import os
from dotenv import load_dotenv

load_dotenv()

class AIProjectAnalysisService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def analyze_project_risk(self, project_id: int, db: Session) -> RiskAssessment:
        """Analyze project risks using AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # Calculate risk factors
        risk_factors = []
        risk_score = 0.0
        
        # Time-based risks
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
        if overdue_tasks:
            overdue_percentage = len(overdue_tasks) / len(tasks) * 100
            risk_factors.append({
                "factor": "Overdue Tasks",
                "severity": "high" if overdue_percentage > 20 else "medium",
                "description": f"{len(overdue_tasks)} tasks are overdue ({overdue_percentage:.1f}%)",
                "impact": 0.3 if overdue_percentage > 20 else 0.15
            })
            risk_score += 0.3 if overdue_percentage > 20 else 0.15
        
        # Progress risks
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        if tasks:
            progress_percentage = len(completed_tasks) / len(tasks) * 100
            if project.end_date:
                days_remaining = (project.end_date - datetime.utcnow()).days
                if days_remaining > 0:
                    expected_progress = max(0, 100 - (days_remaining / 30) * 100)  # Rough calculation
                    if progress_percentage < expected_progress * 0.8:
                        risk_factors.append({
                            "factor": "Behind Schedule",
                            "severity": "high",
                            "description": f"Project is {expected_progress - progress_percentage:.1f}% behind expected progress",
                            "impact": 0.25
                        })
                        risk_score += 0.25
        
        # Resource allocation risks
        unassigned_tasks = [t for t in tasks if not t.assignee_id and t.status != TaskStatus.DONE]
        if unassigned_tasks:
            unassigned_percentage = len(unassigned_tasks) / len(tasks) * 100
            if unassigned_percentage > 10:
                risk_factors.append({
                    "factor": "Unassigned Tasks",
                    "severity": "medium",
                    "description": f"{len(unassigned_tasks)} tasks are unassigned ({unassigned_percentage:.1f}%)",
                    "impact": 0.15
                })
                risk_score += 0.15
        
        # Team workload risks
        assignee_workload = {}
        for task in tasks:
            if task.assignee_id and task.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]:
                if task.assignee_id not in assignee_workload:
                    assignee_workload[task.assignee_id] = 0
                assignee_workload[task.assignee_id] += 1
        
        if assignee_workload:
            max_workload = max(assignee_workload.values())
            avg_workload = sum(assignee_workload.values()) / len(assignee_workload)
            if max_workload > avg_workload * 2:
                risk_factors.append({
                    "factor": "Uneven Workload Distribution",
                    "severity": "medium",
                    "description": f"Some team members have {max_workload} tasks while average is {avg_workload:.1f}",
                    "impact": 0.1
                })
                risk_score += 0.1
        
        # Generate recommendations
        recommendations = []
        critical_issues = []
        
        for factor in risk_factors:
            if factor["severity"] == "high":
                critical_issues.append(factor["description"])
                if "overdue" in factor["factor"].lower():
                    recommendations.append("Review and reschedule overdue tasks immediately")
                elif "behind schedule" in factor["factor"].lower():
                    recommendations.append("Consider adding more resources or reducing scope")
            else:
                if "unassigned" in factor["factor"].lower():
                    recommendations.append("Assign tasks to team members to improve accountability")
                elif "workload" in factor["factor"].lower():
                    recommendations.append("Redistribute tasks to balance team workload")
        
        if not recommendations:
            recommendations.append("Project is on track - continue monitoring progress")
        
        return RiskAssessment(
            overall_risk_score=min(1.0, risk_score),
            risk_factors=risk_factors,
            recommendations=recommendations,
            critical_issues=critical_issues
        )
    
    def predict_project_completion(self, project_id: int, db: Session) -> ProgressPrediction:
        """Predict project completion date using AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        if not tasks:
            return ProgressPrediction(
                predicted_completion_date=project.end_date or datetime.utcnow() + timedelta(days=30),
                confidence_level=0.1,
                factors_affecting_timeline=["No tasks defined"],
                recommended_actions=["Define project tasks and timeline"]
            )
        
        # Calculate current progress
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE]
        in_progress_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        remaining_tasks = [t for t in tasks if t.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]]
        
        progress_percentage = len(completed_tasks) / len(tasks) * 100
        
        # Calculate average completion time for completed tasks
        completed_with_times = [t for t in completed_tasks if t.completed_at and t.created_at]
        if completed_with_times:
            avg_completion_days = sum(
                (t.completed_at - t.created_at).days for t in completed_with_times
            ) / len(completed_with_times)
        else:
            avg_completion_days = 5  # Default assumption
        
        # Predict remaining time
        remaining_days = len(remaining_tasks) * avg_completion_days
        
        # Adjust for team size and workload
        active_assignees = len(set(t.assignee_id for t in tasks if t.assignee_id))
        if active_assignees > 1:
            remaining_days = remaining_days / active_assignees * 0.8  # Team efficiency factor
        
        # Consider overdue tasks
        overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE]
        if overdue_tasks:
            remaining_days *= 1.2  # Add buffer for overdue work
        
        predicted_date = datetime.utcnow() + timedelta(days=remaining_days)
        
        # Calculate confidence level
        confidence = 0.8
        if len(completed_tasks) < 3:
            confidence -= 0.3  # Less confidence with limited historical data
        if overdue_tasks:
            confidence -= 0.2  # Less confidence with overdue tasks
        if not active_assignees:
            confidence -= 0.3  # Less confidence without assigned team
        
        confidence = max(0.1, confidence)
        
        # Identify factors affecting timeline
        factors = []
        if overdue_tasks:
            factors.append(f"{len(overdue_tasks)} overdue tasks affecting schedule")
        if active_assignees == 0:
            factors.append("No tasks assigned to team members")
        elif active_assignees == 1:
            factors.append("Single team member - potential bottleneck")
        if progress_percentage < 20:
            factors.append("Project in early stages - estimates may change")
        
        # Generate recommendations
        recommendations = []
        if overdue_tasks:
            recommendations.append("Address overdue tasks immediately")
        if active_assignees < 2 and len(remaining_tasks) > 10:
            recommendations.append("Consider adding more team members")
        if not factors:
            recommendations.append("Project timeline looks realistic")
        
        return ProgressPrediction(
            predicted_completion_date=predicted_date,
            confidence_level=confidence,
            factors_affecting_timeline=factors,
            recommended_actions=recommendations
        )
    
    def analyze_team_performance(self, project_id: int, db: Session) -> TeamPerformanceAnalysis:
        """Analyze team performance using AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # Calculate team velocity (tasks completed per week)
        completed_tasks = [t for t in tasks if t.status == TaskStatus.DONE and t.completed_at]
        
        if completed_tasks:
            # Calculate velocity over last 4 weeks
            four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
            recent_completions = [t for t in completed_tasks if t.completed_at >= four_weeks_ago]
            team_velocity = len(recent_completions) / 4  # tasks per week
        else:
            team_velocity = 0.0
        
        # Analyze individual performance
        individual_performance = []
        assignees = set(t.assignee_id for t in tasks if t.assignee_id)
        
        for assignee_id in assignees:
            assignee_tasks = [t for t in tasks if t.assignee_id == assignee_id]
            completed_by_assignee = [t for t in assignee_tasks if t.status == TaskStatus.DONE]
            
            # Calculate completion rate
            completion_rate = len(completed_by_assignee) / len(assignee_tasks) * 100 if assignee_tasks else 0
            
            # Calculate average completion time
            completed_with_times = [t for t in completed_by_assignee if t.completed_at and t.created_at]
            if completed_with_times:
                avg_completion_time = sum(
                    (t.completed_at - t.created_at).days for t in completed_with_times
                ) / len(completed_with_times)
            else:
                avg_completion_time = 0
            
            # Check for overdue tasks
            overdue_count = len([t for t in assignee_tasks 
                               if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE])
            
            individual_performance.append({
                "assignee_id": assignee_id,
                "total_tasks": len(assignee_tasks),
                "completed_tasks": len(completed_by_assignee),
                "completion_rate": completion_rate,
                "avg_completion_time_days": avg_completion_time,
                "overdue_tasks": overdue_count,
                "performance_score": max(0, completion_rate - (overdue_count * 10))
            })
        
        # Identify bottlenecks
        bottlenecks = []
        
        # Check for tasks stuck in progress
        stuck_tasks = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS 
                      and t.updated_at and (datetime.utcnow() - t.updated_at).days > 7]
        if stuck_tasks:
            bottlenecks.append(f"{len(stuck_tasks)} tasks stuck in progress for over a week")
        
        # Check for unassigned tasks
        unassigned_tasks = [t for t in tasks if not t.assignee_id and t.status != TaskStatus.DONE]
        if unassigned_tasks:
            bottlenecks.append(f"{len(unassigned_tasks)} unassigned tasks")
        
        # Check for overloaded team members
        if individual_performance:
            max_tasks = max(p["total_tasks"] for p in individual_performance)
            avg_tasks = sum(p["total_tasks"] for p in individual_performance) / len(individual_performance)
            if max_tasks > avg_tasks * 2:
                bottlenecks.append("Uneven task distribution among team members")
        
        # Generate optimization suggestions
        optimization_suggestions = []
        
        if team_velocity < 2:
            optimization_suggestions.append("Consider breaking down large tasks into smaller ones")
        
        if bottlenecks:
            optimization_suggestions.append("Address identified bottlenecks to improve flow")
        
        if individual_performance:
            low_performers = [p for p in individual_performance if p["completion_rate"] < 50]
            if low_performers:
                optimization_suggestions.append("Provide additional support to team members with low completion rates")
        
        if not optimization_suggestions:
            optimization_suggestions.append("Team performance is good - maintain current practices")
        
        return TeamPerformanceAnalysis(
            team_velocity=team_velocity,
            individual_performance=individual_performance,
            bottlenecks=bottlenecks,
            optimization_suggestions=optimization_suggestions
        )
    
    def forecast_budget(self, project_id: int, db: Session) -> BudgetForecast:
        """Forecast project budget using AI"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found")
        
        if not project.budget:
            return BudgetForecast(
                projected_total_cost=0.0,
                current_utilization=0.0,
                cost_variance=0.0,
                budget_alerts=["No budget defined for this project"],
                cost_optimization_tips=["Define a project budget to enable cost tracking"]
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
        
        # Generate budget alerts
        budget_alerts = []
        if current_utilization > 80:
            budget_alerts.append("Budget utilization is over 80% - monitor closely")
        if projected_total_cost > project.budget:
            budget_alerts.append(f"Projected cost (${projected_total_cost:,.2f}) exceeds budget by ${projected_total_cost - project.budget:,.2f}")
        if cost_variance > 20:
            budget_alerts.append(f"Cost variance is {cost_variance:.1f}% above expected")
        
        # Generate cost optimization tips
        cost_optimization_tips = []
        if projected_total_cost > project.budget:
            cost_optimization_tips.append("Consider reducing scope or optimizing task estimates")
        if cost_variance > 10:
            cost_optimization_tips.append("Review actual vs estimated hours to improve future estimates")
        if not budget_alerts:
            cost_optimization_tips.append("Budget is on track - continue monitoring")
        
        return BudgetForecast(
            projected_total_cost=projected_total_cost,
            current_utilization=current_utilization,
            cost_variance=cost_variance,
            budget_alerts=budget_alerts,
            cost_optimization_tips=cost_optimization_tips
        )
    
    def generate_ai_insights(self, project_id: int, db: Session) -> List[Dict[str, Any]]:
        """Generate comprehensive AI insights for a project"""
        insights = []
        
        try:
            # Risk analysis
            risk_assessment = self.analyze_project_risk(project_id, db)
            if risk_assessment.overall_risk_score > 0.3:
                insights.append({
                    "type": InsightType.RISK_ANALYSIS,
                    "priority": InsightPriority.HIGH if risk_assessment.overall_risk_score > 0.6 else InsightPriority.MEDIUM,
                    "title": f"Project Risk Score: {risk_assessment.overall_risk_score:.1%}",
                    "description": f"Risk analysis identified {len(risk_assessment.risk_factors)} risk factors",
                    "recommendations": "; ".join(risk_assessment.recommendations),
                    "confidence_score": 0.8
                })
            
            # Progress prediction
            progress_prediction = self.predict_project_completion(project_id, db)
            insights.append({
                "type": InsightType.PROGRESS_PREDICTION,
                "priority": InsightPriority.MEDIUM,
                "title": f"Predicted Completion: {progress_prediction.predicted_completion_date.strftime('%Y-%m-%d')}",
                "description": f"Based on current progress, project completion predicted with {progress_prediction.confidence_level:.1%} confidence",
                "recommendations": "; ".join(progress_prediction.recommended_actions),
                "confidence_score": progress_prediction.confidence_level
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
        
        return insights