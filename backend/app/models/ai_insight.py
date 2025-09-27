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
    project = relationship("Project")
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
    project_name: Optional[str] = None
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

class ProjectInfo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    deadline: Optional[datetime] = None

class RiskAssessment(BaseModel):
    project_info: ProjectInfo
    overall_risk_score: float
    risk_level: str  # "Bajo", "Medio", "Alto", "Crítico"
    risk_factors: List[Dict[str, Any]]
    recommendations: List[str]
    critical_issues: List[str]
    risk_categories: Dict[str, float]  # {"technical": 0.2, "timeline": 0.5, "resources": 0.3}
    mitigation_strategies: List[Dict[str, str]]
    impact_assessment: Dict[str, Any]

class ProgressPrediction(BaseModel):
    project_info: ProjectInfo
    predicted_completion_date: datetime
    confidence_level: float
    completion_probability: float  # Probabilidad de completar a tiempo
    factors_affecting_timeline: List[str]
    recommended_actions: List[str]
    milestone_predictions: List[Dict[str, Any]]
    velocity_analysis: Dict[str, float]
    timeline_scenarios: Dict[str, Dict[str, Any]]  # optimistic, realistic, pessimistic

class TeamPerformanceAnalysis(BaseModel):
    project_info: ProjectInfo
    team_velocity: float
    team_efficiency_score: float  # 0-100
    individual_performance: List[Dict[str, Any]]
    bottlenecks: List[str]
    optimization_suggestions: List[str]
    performance_trends: Dict[str, List[float]]
    collaboration_metrics: Dict[str, float]
    skill_gap_analysis: List[Dict[str, str]]
    workload_distribution: Dict[str, float]

class BudgetForecast(BaseModel):
    project_info: ProjectInfo
    projected_total_cost: float
    current_utilization: float
    cost_variance: float
    budget_alerts: List[str]
    cost_optimization_tips: List[str]
    cost_breakdown: Dict[str, float]
    spending_trends: List[Dict[str, Any]]
    roi_analysis: Dict[str, float]