from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum as PyEnum
from ..database import Base

class InsightType(PyEnum):
    RISK_ANALYSIS = "risk_analysis"
    PROGRESS_PREDICTION = "progress_prediction"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    DEADLINE_ALERT = "deadline_alert"
    TEAM_PERFORMANCE = "team_performance"
    BUDGET_FORECAST = "budget_forecast"

class InsightPriority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    insight_type = Column(Enum(InsightType), nullable=False)
    priority = Column(Enum(InsightPriority), default=InsightPriority.MEDIUM)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    data_source = Column(String(100), nullable=True)  # Source of the insight
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="ai_insights")
    acknowledged_by_user = relationship("User", foreign_keys=[acknowledged_by])

class ProjectAnalytics(Base):
    __tablename__ = "project_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    analysis_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Progress metrics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    in_progress_tasks = Column(Integer, default=0)
    overdue_tasks = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0.0)
    
    # Time metrics
    estimated_total_hours = Column(Integer, default=0)
    actual_total_hours = Column(Integer, default=0)
    remaining_estimated_hours = Column(Integer, default=0)
    
    # Team metrics
    active_team_members = Column(Integer, default=0)
    average_task_completion_time = Column(Float, default=0.0)  # in hours
    team_velocity = Column(Float, default=0.0)  # tasks per week
    
    # Risk indicators
    budget_utilization = Column(Float, default=0.0)  # percentage
    schedule_variance = Column(Float, default=0.0)  # days ahead/behind
    risk_score = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Relationships
    project = relationship("Project")

# Pydantic models for API
class AIInsightBase(BaseModel):
    insight_type: InsightType
    priority: Optional[InsightPriority] = InsightPriority.MEDIUM
    title: str
    description: str
    recommendations: Optional[str] = None
    confidence_score: Optional[float] = None
    data_source: Optional[str] = None

class AIInsightCreate(AIInsightBase):
    project_id: int

class AIInsightUpdate(BaseModel):
    priority: Optional[InsightPriority] = None
    title: Optional[str] = None
    description: Optional[str] = None
    recommendations: Optional[str] = None
    is_acknowledged: Optional[bool] = None

class AIInsightResponse(AIInsightBase):
    id: int
    project_id: int
    is_acknowledged: bool
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProjectAnalyticsBase(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    overdue_tasks: int
    progress_percentage: float
    estimated_total_hours: int
    actual_total_hours: int
    remaining_estimated_hours: int
    active_team_members: int
    average_task_completion_time: float
    team_velocity: float
    budget_utilization: float
    schedule_variance: float
    risk_score: float

class ProjectAnalyticsResponse(ProjectAnalyticsBase):
    id: int
    project_id: int
    analysis_date: datetime
    
    class Config:
        from_attributes = True

class RiskAssessment(BaseModel):
    overall_risk_score: float
    risk_factors: List[Dict[str, Any]]
    recommendations: List[str]
    critical_issues: List[str]

class ProgressPrediction(BaseModel):
    predicted_completion_date: datetime
    confidence_level: float
    factors_affecting_timeline: List[str]
    recommended_actions: List[str]

class TeamPerformanceAnalysis(BaseModel):
    team_velocity: float
    individual_performance: List[Dict[str, Any]]
    bottlenecks: List[str]
    optimization_suggestions: List[str]

class BudgetForecast(BaseModel):
    projected_total_cost: float
    current_utilization: float
    cost_variance: float
    budget_alerts: List[str]
    cost_optimization_tips: List[str]