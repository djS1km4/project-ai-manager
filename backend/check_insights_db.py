#!/usr/bin/env python3
"""
Script to check AI insights in the database
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models.ai_insight import AIInsight

def check_insights():
    print("🔍 Checking AI insights in database...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # Get all insights
        insights = db.query(AIInsight).all()
        print(f"📊 Total insights found: {len(insights)}")
        
        if insights:
            print("\n📋 Insights details:")
            for insight in insights:
                print(f"  - ID: {insight.id}")
                print(f"    Project ID: {insight.project_id}")
                print(f"    Type: {insight.insight_type}")
                print(f"    Title: {insight.title}")
                print(f"    Confidence: {insight.confidence_score}")
                print(f"    Created: {insight.created_at}")
                print(f"    Data: {insight.data[:100]}..." if len(insight.data) > 100 else f"    Data: {insight.data}")
                print()
        else:
            print("⚠️ No insights found in database")
            
    except Exception as e:
        print(f"❌ Error checking insights: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_insights()