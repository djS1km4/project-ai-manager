#!/usr/bin/env python3
"""
Debug script for AI analysis
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.services.ai_service import AIProjectAnalysisService

def debug_ai_analysis():
    print("🔍 Debugging AI analysis...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        ai_service = AIProjectAnalysisService()
        project_id = 3
        
        print(f"📊 Analyzing project {project_id}...")
        
        # Test each method individually
        print("\n1. Testing risk analysis...")
        try:
            risk_analysis = ai_service.analyze_project_risk(project_id, db)
            print(f"   Risk Score: {risk_analysis.overall_risk_score}")
            print(f"   Risk Factors: {len(risk_analysis.risk_factors)}")
            print(f"   Critical Issues: {len(risk_analysis.critical_issues)}")
            for factor in risk_analysis.risk_factors:
                print(f"     - {factor}")
        except Exception as e:
            print(f"   ❌ Error in risk analysis: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n2. Testing progress prediction...")
        try:
            progress_prediction = ai_service.predict_project_completion(project_id, db)
            print(f"   Predicted completion: {progress_prediction.predicted_completion_date}")
            print(f"   Confidence: {progress_prediction.confidence_level}")
            print(f"   Factors: {len(progress_prediction.factors_affecting_timeline)}")
        except Exception as e:
            print(f"   ❌ Error in progress prediction: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n3. Testing team performance...")
        try:
            team_analysis = ai_service.analyze_team_performance(project_id, db)
            print(f"   Team velocity: {team_analysis.team_velocity}")
            print(f"   Bottlenecks: {len(team_analysis.bottlenecks)}")
            print(f"   Performance data: {len(team_analysis.individual_performance)}")
        except Exception as e:
            print(f"   ❌ Error in team analysis: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n4. Testing budget forecast...")
        try:
            budget_forecast = ai_service.forecast_budget(project_id, db)
            print(f"   Current utilization: {budget_forecast.current_utilization}%")
            print(f"   Budget alerts: {len(budget_forecast.budget_alerts)}")
        except Exception as e:
            print(f"   ❌ Error in budget forecast: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n5. Testing full insights generation...")
        try:
            insights = ai_service.generate_project_insights(db, project_id)
            print(f"   Generated insights: {len(insights)}")
            for insight in insights:
                print(f"     - {insight.title} ({insight.insight_type})")
        except Exception as e:
            print(f"   ❌ Error in insights generation: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ General error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_ai_analysis()