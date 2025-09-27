from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..database import get_db
from ..models.ai_insight import (
    AIInsight, AIInsightCreate, AIInsightUpdate, AIInsightResponse,
    ProjectAnalytics, ProjectAnalyticsResponse,
    RiskAssessment, ProgressPrediction, TeamPerformanceAnalysis, BudgetForecast
)
from ..services.auth_service import AuthService
from ..services.ai_service import AIProjectAnalysisService
from ..services.project_service import ProjectService

router = APIRouter(prefix="/ai-insights", tags=["ai-insights"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    return AuthService.get_current_user_from_token(db, token)

@router.post("/analyze-project/{project_id}")
def analyze_project(
    project_id: int,
    analysis_type: Optional[str] = Query(None, description="Specific analysis type: risk, progress, team, budget, or all"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI analysis for a project - specific type or comprehensive"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        if analysis_type and analysis_type != "all":
            # Generate specific analysis type
            insights = ai_service.generate_specific_analysis(db, project_id, analysis_type)
            return {
                "message": f"{analysis_type.title()} analysis completed successfully",
                "analysis_type": analysis_type,
                "insights": insights
            }
        else:
            # Generate comprehensive analysis (all types)
            insights = ai_service.generate_project_insights(db, project_id)
            return {
                "message": "Comprehensive project analysis completed successfully",
                "analysis_type": "all",
                "insights": insights
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing project: {str(e)}"
        )

@router.get("/project/{project_id}/risk-assessment")
def get_risk_assessment(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered risk assessment for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        risk_assessment = ai_service.analyze_project_risk(project_id, db)
        return risk_assessment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating risk assessment: {str(e)}"
        )

@router.get("/project/{project_id}/progress-prediction")
def get_progress_prediction(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered progress prediction for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        prediction = ai_service.predict_project_completion(project_id, db)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating progress prediction: {str(e)}"
        )

@router.get("/project/{project_id}/team-performance")
def get_team_performance_analysis(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered team performance analysis for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        analysis = ai_service.analyze_team_performance(project_id, db)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing team performance: {str(e)}"
        )

@router.post("/project/{project_id}/analyze/risk")
def analyze_project_risk_specific(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate specific risk analysis for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        insights = ai_service.generate_specific_analysis(db, project_id, "risk")
        return {
            "message": "Risk analysis completed successfully",
            "analysis_type": "risk",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing project risk: {str(e)}"
        )

@router.post("/project/{project_id}/analyze/progress")
def analyze_project_progress_specific(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate specific progress prediction for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        insights = ai_service.generate_specific_analysis(db, project_id, "progress")
        return {
            "message": "Progress prediction completed successfully",
            "analysis_type": "progress",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting project progress: {str(e)}"
        )

@router.post("/project/{project_id}/analyze/team")
def analyze_project_team_specific(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate specific team performance analysis for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        insights = ai_service.generate_specific_analysis(db, project_id, "team")
        return {
            "message": "Team performance analysis completed successfully",
            "analysis_type": "team",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing team performance: {str(e)}"
        )

@router.get("/project/{project_id}/budget-forecast")
def get_budget_forecast(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered budget forecast for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    ai_service = AIProjectAnalysisService()
    try:
        forecast = ai_service.forecast_budget(db, project_id)
        return forecast
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating budget forecast: {str(e)}"
        )

@router.get("/project/{project_id}/insights", response_model=List[AIInsightResponse])
def get_project_insights(
    project_id: int,
    insight_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all AI insights for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    from ..models.project import Project
    
    query = db.query(AIInsight, Project.name.label('project_name')).join(
        Project, AIInsight.project_id == Project.id
    ).filter(AIInsight.project_id == project_id)
    
    if insight_type:
        query = query.filter(AIInsight.insight_type == insight_type)
    
    insights_query = query.order_by(AIInsight.created_at.desc()).limit(limit).all()
    
    # Convert to list of dictionaries with project_name included
    insights = []
    for insight, project_name in insights_query:
        insight_dict = AIInsightResponse(
            id=insight.id,
            project_id=insight.project_id,
            project_name=project_name,
            insight_type=insight.insight_type,
            priority=insight.priority,
            title=insight.title,
            description=insight.description,
            recommendations=insight.recommendations,
            confidence_score=insight.confidence_score,
            data_source=insight.data_source,
            is_acknowledged=insight.is_acknowledged,
            acknowledged_by=insight.acknowledged_by,
            acknowledged_at=insight.acknowledged_at,
            created_at=insight.created_at,
            expires_at=insight.expires_at
        )
        insights.append(insight_dict)
    
    return insights

@router.get("/project/{project_id}/analytics", response_model=ProjectAnalyticsResponse)
def get_project_analytics(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project analytics data"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    # Get the latest analytics record
    analytics = db.query(ProjectAnalytics).filter(
        ProjectAnalytics.project_id == project_id
    ).order_by(ProjectAnalytics.analysis_date.desc()).first()
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analytics data found for this project"
        )
    
    return analytics

@router.post("/project/{project_id}/insights", response_model=AIInsightResponse)
def create_insight(
    project_id: int,
    insight: AIInsightCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new AI insight for a project"""
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    # Create the insight
    insight_data = insight.dict()
    insight_data['project_id'] = project_id
    db_insight = AIInsight(**insight_data)
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    
    return db_insight

@router.put("/insights/{insight_id}", response_model=AIInsightResponse)
def update_insight(
    insight_id: int,
    insight_update: AIInsightUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an AI insight"""
    # Get the insight
    db_insight = db.query(AIInsight).filter(AIInsight.id == insight_id).first()
    if not db_insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insight not found"
        )
    
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, db_insight.project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this insight"
        )
    
    # Update the insight
    update_data = insight_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_insight, field, value)
    
    db_insight.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_insight)
    
    return db_insight

@router.delete("/insights/{insight_id}")
def delete_insight(
    insight_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an AI insight"""
    # Get the insight
    db_insight = db.query(AIInsight).filter(AIInsight.id == insight_id).first()
    if not db_insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insight not found"
        )
    
    # Check if user has access to the project
    project_service = ProjectService()
    project = project_service.get_project(db, db_insight.project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this insight"
        )
    
    db.delete(db_insight)
    db.commit()
    
    return {"message": "Insight deleted successfully"}

@router.get("/dashboard/insights")
def get_dashboard_insights(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI insights for user's dashboard"""
    # Get user's projects
    project_service = ProjectService()
    user_projects = project_service.get_projects(db, current_user.id)
    project_ids = [p["id"] for p in user_projects]
    
    if not project_ids:
        return {
            "insights": [],
            "summary": {
                "total_insights": 0,
                "risk_alerts": 0,
                "recommendations": 0,
                "predictions": 0
            }
        }
    
    # Get insights from the last N days with project information
    since_date = datetime.utcnow() - timedelta(days=days)
    
    from ..models.project import Project
    
    insights_query = db.query(AIInsight, Project.name.label('project_name')).join(
        Project, AIInsight.project_id == Project.id
    ).filter(
        AIInsight.project_id.in_(project_ids),
        AIInsight.created_at >= since_date
    ).order_by(AIInsight.created_at.desc()).limit(100).all()
    
    # Convert to list of dictionaries with project_name included
    insights = []
    for insight, project_name in insights_query:
        insight_dict = {
            "id": insight.id,
            "project_id": insight.project_id,
            "project_name": project_name,
            "insight_type": insight.insight_type,
            "priority": insight.priority,
            "title": insight.title,
            "description": insight.description,
            "recommendations": insight.recommendations,
            "confidence_score": insight.confidence_score,
            "data_source": insight.data_source,
            "is_acknowledged": insight.is_acknowledged,
            "acknowledged_by": insight.acknowledged_by,
            "acknowledged_at": insight.acknowledged_at,
            "created_at": insight.created_at,
            "expires_at": insight.expires_at
        }
        insights.append(insight_dict)
    
    # Categorize insights
    risk_alerts = [i for i in insights if i["insight_type"] == "risk_assessment" and i["confidence_score"] and i["confidence_score"] > 0.7]
    recommendations = [i for i in insights if i["insight_type"] == "recommendation"]
    predictions = [i for i in insights if i["insight_type"] == "prediction"]
    
    return {
        "insights": insights[:20],  # Return top 20 for dashboard
        "summary": {
            "total_insights": len(insights),
            "risk_alerts": len(risk_alerts),
            "recommendations": len(recommendations),
            "predictions": len(predictions)
        },
        "period_days": days
    }

@router.get("/insights/types")
def get_insight_types():
    """Get available insight types"""
    return {
        "insight_types": [
            "risk_assessment",
            "progress_prediction", 
            "team_performance",
            "budget_forecast",
            "recommendation",
            "alert",
            "optimization",
            "trend_analysis"
        ]
    }

@router.post("/batch-analyze")
def batch_analyze_projects(
    project_ids: List[int],
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze multiple projects in batch"""
    project_service = ProjectService()
    ai_service = AIProjectAnalysisService()
    
    results = []
    errors = []
    
    for project_id in project_ids:
        try:
            # Check access
            project = project_service.get_project(db, project_id, current_user.id)
            if not project:
                errors.append(f"Project {project_id}: Not found or access denied")
                continue
            
            # Generate insights
            insights = ai_service.generate_project_insights(db, project_id)
            results.append({
                "project_id": project_id,
                "project_name": project.name,
                "insights_generated": len(insights) if isinstance(insights, list) else 1,
                "status": "success"
            })
            
        except Exception as e:
            errors.append(f"Project {project_id}: {str(e)}")
    
    return {
        "analyzed_projects": results,
        "success_count": len(results),
        "errors": errors
    }

@router.get("/trends/insights")
def get_insights_trends(
    days: int = Query(90, ge=7, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trends in AI insights over time"""
    # Get user's projects
    project_service = ProjectService()
    user_projects = project_service.get_projects(db, current_user.id)
    project_ids = [p["id"] for p in user_projects]
    
    if not project_ids:
        return {"trends": [], "summary": {}}
    
    # Get insights from the last N days
    since_date = datetime.utcnow() - timedelta(days=days)
    
    insights = db.query(AIInsight).filter(
        AIInsight.project_id.in_(project_ids),
        AIInsight.created_at >= since_date
    ).all()
    
    # Group by week and type
    trends = {}
    for insight in insights:
        week = insight.created_at.strftime("%Y-W%U")
        if week not in trends:
            trends[week] = {}
        
        insight_type = insight.insight_type
        if insight_type not in trends[week]:
            trends[week][insight_type] = 0
        trends[week][insight_type] += 1
    
    # Convert to list format
    trend_list = []
    for week, types in sorted(trends.items()):
        trend_list.append({
            "week": week,
            "insights_by_type": types,
            "total": sum(types.values())
        })
    
    return {
        "trends": trend_list,
        "summary": {
            "total_insights": len(insights),
            "period_days": days,
            "avg_per_week": len(insights) / max(1, len(trend_list))
        }
    }