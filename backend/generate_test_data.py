#!/usr/bin/env python3
"""
Script to generate comprehensive test data for the Project AI Manager
"""
import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8001/api/v1"

# Test user credentials
TEST_USER = {
    "email": "test@example.com",
    "password": "testpassword123"
}

class TestDataGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.headers = {}
        self.user_id = None
        
    def login(self):
        """Login and get authentication token"""
        print("🔐 Logging in...")
        
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.user_id = data["user"]["id"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
            print("✅ Login successful")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    
    def create_projects(self):
        """Create diverse test projects"""
        print("\n📁 Creating test projects...")
        
        projects_data = [
            {
                "name": "E-commerce Platform Redesign",
                "description": "Complete redesign of the company's e-commerce platform with modern UI/UX",
                "status": "active",
                "priority": "high",
                "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "budget": 15000000  # $150,000 in cents
            },
            {
                "name": "Mobile App Development",
                "description": "Native mobile application for iOS and Android platforms",
                "status": "active", 
                "priority": "medium",
                "start_date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                "budget": 8000000  # $80,000 in cents
            },
            {
                "name": "Data Analytics Dashboard",
                "description": "Business intelligence dashboard for real-time analytics",
                "status": "completed",
                "priority": "high",
                "start_date": (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
                "budget": 4500000  # $45,000 in cents
            },
            {
                "name": "Security Audit & Compliance",
                "description": "Comprehensive security audit and compliance implementation",
                "status": "on_hold",
                "priority": "high",
                "start_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                "budget": 2500000  # $25,000 in cents
            },
            {
                "name": "Legacy System Migration",
                "description": "Migration from legacy systems to modern cloud infrastructure",
                "status": "cancelled",
                "priority": "low",
                "start_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "budget": 20000000  # $200,000 in cents
            }
        ]
        
        created_projects = []
        
        for project_data in projects_data:
            response = self.session.post(f"{BASE_URL}/projects", json=project_data, headers=self.headers)
            if response.status_code in [200, 201]:
                project = response.json()
                created_projects.append(project)
                print(f"✅ Created project: {project['name']} (ID: {project['id']})")
            else:
                print(f"❌ Failed to create project: {project_data['name']}")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                print(f"   Data sent: {project_data}")
        
        return created_projects
    
    def create_tasks(self, projects):
        """Create diverse test tasks for projects"""
        print("\n📋 Creating test tasks...")
        
        task_templates = [
            {
                "title": "Requirements Analysis",
                "description": "Gather and analyze project requirements from stakeholders",
                "priority": "high",
                "estimated_hours": 40
            },
            {
                "title": "UI/UX Design",
                "description": "Create wireframes and design mockups for the user interface",
                "priority": "medium",
                "estimated_hours": 60
            },
            {
                "title": "Backend Development",
                "description": "Implement server-side logic and database integration",
                "priority": "high",
                "estimated_hours": 120
            },
            {
                "title": "Frontend Development",
                "description": "Develop client-side interface and user interactions",
                "priority": "high",
                "estimated_hours": 100
            },
            {
                "title": "Testing & QA",
                "description": "Comprehensive testing including unit, integration, and user acceptance tests",
                "priority": "medium",
                "estimated_hours": 80
            },
            {
                "title": "Documentation",
                "description": "Create technical and user documentation",
                "priority": "low",
                "estimated_hours": 30
            },
            {
                "title": "Deployment",
                "description": "Deploy application to production environment",
                "priority": "high",
                "estimated_hours": 20
            },
            {
                "title": "Performance Optimization",
                "description": "Optimize application performance and scalability",
                "priority": "medium",
                "estimated_hours": 40
            }
        ]
        
        statuses = ["pending", "in_progress", "completed", "cancelled"]
        created_tasks = []
        
        for project in projects:
            # Create 3-6 tasks per project
            num_tasks = random.randint(3, 6)
            selected_templates = random.sample(task_templates, min(num_tasks, len(task_templates)))
            
            for i, template in enumerate(selected_templates):
                # Vary due dates
                days_offset = random.randint(5, 45)
                due_date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
                
                # Assign status based on project status (using valid task statuses)
                if project["status"] == "completed":
                    status = random.choice(["done", "done", "done", "cancelled"])
                elif project["status"] == "cancelled":
                    status = "cancelled"
                elif project["status"] == "on_hold":
                    status = random.choice(["todo", "in_progress", "cancelled"])
                else:  # active
                    status = random.choice(["todo", "in_progress", "in_review", "done"])
                
                task_data = {
                    "title": template["title"],
                    "description": template["description"],
                    "status": status,
                    "priority": template["priority"],
                    "project_id": project["id"],
                    "assignee_id": self.user_id,
                    "due_date": due_date,
                    "estimated_hours": template["estimated_hours"]
                }
                
                response = self.session.post(f"{BASE_URL}/tasks", json=task_data, headers=self.headers)
                if response.status_code in [200, 201]:
                    task = response.json()
                    created_tasks.append(task)
                    print(f"✅ Created task: {task['title']} ({task['status']}) for {project['name']}")
                else:
                    print(f"❌ Failed to create task: {template['title']}")
                    print(f"   Status: {response.status_code}")
                    print(f"   Response: {response.text}")
        
        return created_tasks
    
    def generate_ai_insights(self, projects):
        """Generate AI insights for projects"""
        print("\n🧠 Generating AI insights...")
        
        insight_types = [
            "risk_assessment",
            "progress_prediction", 
            "team_performance",
            "budget_forecast",
            "recommendation",
            "alert"
        ]
        
        for project in projects[:3]:  # Generate insights for first 3 projects
            for insight_type in random.sample(insight_types, 3):  # 3 random insight types per project
                insight_data = {
                    "insight_type": insight_type,
                    "title": f"{insight_type.replace('_', ' ').title()} for {project['name']}",
                    "content": f"AI-generated {insight_type} analysis for project {project['name']}",
                    "confidence_score": round(random.uniform(0.6, 0.95), 2),
                    "data": json.dumps({
                        "analysis_date": datetime.now().isoformat(),
                        "project_metrics": {
                            "completion_percentage": random.randint(10, 90),
                            "risk_level": random.choice(["low", "medium", "high"]),
                            "estimated_delay_days": random.randint(0, 15)
                        }
                    })
                }
                
                response = self.session.post(
                    f"{BASE_URL}/ai-insights/project/{project['id']}/insights", 
                    json=insight_data, 
                    headers=self.headers
                )
                
                if response.status_code == 201:
                    print(f"✅ Generated {insight_type} insight for {project['name']}")
                else:
                    print(f"❌ Failed to generate insight: {insight_type}")
    
    def run(self):
        """Run the complete test data generation"""
        print("🚀 Starting test data generation...")
        print("=" * 60)
        
        if not self.login():
            return False
        
        # Create projects
        projects = self.create_projects()
        if not projects:
            print("❌ No projects created, stopping...")
            return False
        
        # Create tasks
        tasks = self.create_tasks(projects)
        
        # Generate AI insights
        self.generate_ai_insights(projects)
        
        print("\n" + "=" * 60)
        print(f"✅ Test data generation completed!")
        print(f"📁 Created {len(projects)} projects")
        print(f"📋 Created {len(tasks)} tasks")
        print("🧠 Generated AI insights")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    generator = TestDataGenerator()
    success = generator.run()
    
    if not success:
        print("❌ Test data generation failed!")
        exit(1)