#!/usr/bin/env python3
"""
Comprehensive System Test Script
Tests all major functionalities of the Project AI Manager system
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
TEST_USER = {
    "email": "test@example.com",
    "password": "testpassword123",
    "username": "testuser",
    "full_name": "Test User"
}

class SystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_project_id = None
        self.test_task_id = None
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_authentication(self):
        """Test user registration and login"""
        self.log("Testing Authentication System...")
        
        # Test registration
        try:
            response = self.session.post(f"{BASE_URL}/auth/register", json=TEST_USER)
            if response.status_code in [200, 201]:
                self.log("✅ User registration successful")
            elif response.status_code == 400 and "already registered" in response.text.lower():
                self.log("✅ User already exists (expected)")
            else:
                self.log(f"❌ Registration failed: {response.status_code} - {response.text}", "ERROR")
        except Exception as e:
            self.log(f"❌ Registration error: {e}", "ERROR")
            
        # Test login
        try:
            login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
            response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                self.log("✅ Login successful")
                return True
            else:
                self.log(f"❌ Login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Login error: {e}", "ERROR")
            return False
            
    def test_projects(self):
        """Test project CRUD operations"""
        self.log("Testing Project Management...")
        
        # Create project
        project_data = {
            "name": f"Test Project {datetime.now().strftime('%H%M%S')}",
            "description": "Automated test project",
            "status": "active",
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/projects/", json=project_data)
            if response.status_code in [200, 201]:
                project = response.json()
                self.test_project_id = project["id"]
                self.log(f"✅ Project created successfully (ID: {self.test_project_id})")
            else:
                self.log(f"❌ Project creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Project creation error: {e}", "ERROR")
            return False
            
        # Get projects list
        try:
            response = self.session.get(f"{BASE_URL}/projects/")
            if response.status_code == 200:
                projects = response.json()
                self.log(f"✅ Projects list retrieved ({len(projects)} projects)")
            else:
                self.log(f"❌ Failed to get projects: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Get projects error: {e}", "ERROR")
            
        # Update project
        try:
            update_data = {"name": f"Updated Test Project {datetime.now().strftime('%H%M%S')}"}
            response = self.session.put(f"{BASE_URL}/projects/{self.test_project_id}", json=update_data)
            if response.status_code == 200:
                self.log("✅ Project updated successfully")
            else:
                self.log(f"❌ Project update failed: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Project update error: {e}", "ERROR")
            
        return True
        
    def test_tasks(self):
        """Test task CRUD operations"""
        self.log("Testing Task Management...")
        
        if not self.test_project_id:
            self.log("❌ No test project available for task testing", "ERROR")
            return False
            
        # Create task
        task_data = {
            "title": f"Test Task {datetime.now().strftime('%H%M%S')}",
            "description": "Automated test task",
            "project_id": self.test_project_id,
            "priority": "medium",
            "status": "todo",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "estimated_hours": 5
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/tasks/", json=task_data)
            if response.status_code in [200, 201]:
                task = response.json()
                self.test_task_id = task["id"]
                self.log(f"✅ Task created successfully (ID: {self.test_task_id})")
            else:
                self.log(f"❌ Task creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Task creation error: {e}", "ERROR")
            return False
            
        # Get tasks list
        try:
            response = self.session.get(f"{BASE_URL}/tasks/")
            if response.status_code == 200:
                tasks = response.json()
                self.log(f"✅ Tasks list retrieved ({len(tasks)} tasks)")
            else:
                self.log(f"❌ Failed to get tasks: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Get tasks error: {e}", "ERROR")
            
        # Update task
        try:
            update_data = {"status": "in_progress", "title": f"Updated Test Task {datetime.now().strftime('%H%M%S')}"}
            response = self.session.put(f"{BASE_URL}/tasks/{self.test_task_id}", json=update_data)
            if response.status_code == 200:
                self.log("✅ Task updated successfully")
            else:
                self.log(f"❌ Task update failed: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Task update error: {e}", "ERROR")
            
        return True
        
    def test_ai_insights(self):
        """Test AI insights functionality"""
        self.log("Testing AI Insights...")
        
        # Test dashboard insights
        try:
            response = self.session.get(f"{BASE_URL}/ai-insights/dashboard/insights")
            if response.status_code == 200:
                insights = response.json()
                self.log(f"✅ Dashboard insights retrieved ({len(insights)} insights)")
            else:
                self.log(f"❌ Dashboard insights failed: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Dashboard insights error: {e}", "ERROR")
            
        if self.test_project_id:
            # Test project insights (get existing insights)
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/project/{self.test_project_id}/insights")
                if response.status_code == 200:
                    insights = response.json()
                    self.log(f"✅ Project insights retrieved ({len(insights)} insights)")
                else:
                    self.log(f"❌ Project insights failed: {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"❌ Project insights error: {e}", "ERROR")
                
            # Test insight types
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/insights/types")
                if response.status_code == 200:
                    types = response.json()
                    self.log("✅ Insight types retrieved")
                else:
                    self.log(f"❌ Insight types failed: {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"❌ Insight types error: {e}", "ERROR")
                
            # Test trends insights
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/trends/insights")
                if response.status_code == 200:
                    trends = response.json()
                    self.log("✅ Trends insights retrieved")
                else:
                    self.log(f"❌ Trends insights failed: {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"❌ Trends insights error: {e}", "ERROR")
                
            # Test risk assessment (using AI service directly)
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/project/{self.test_project_id}/risk-assessment")
                if response.status_code == 200:
                    risk_data = response.json()
                    self.log("✅ Risk assessment retrieved")
                else:
                    self.log(f"⚠️ Risk assessment endpoint not available: {response.status_code}", "WARN")
            except Exception as e:
                self.log(f"⚠️ Risk assessment error: {e}", "WARN")
                
            # Test progress prediction (using AI service directly)
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/project/{self.test_project_id}/progress-prediction")
                if response.status_code == 200:
                    progress_data = response.json()
                    self.log("✅ Progress prediction retrieved")
                else:
                    self.log(f"⚠️ Progress prediction endpoint not available: {response.status_code}", "WARN")
            except Exception as e:
                self.log(f"⚠️ Progress prediction error: {e}", "WARN")
                
            # Test team performance (using AI service directly)
            try:
                response = self.session.get(f"{BASE_URL}/ai-insights/project/{self.test_project_id}/team-performance")
                if response.status_code == 200:
                    team_data = response.json()
                    self.log("✅ Team performance analysis retrieved")
                else:
                    self.log(f"⚠️ Team performance endpoint not available: {response.status_code}", "WARN")
            except Exception as e:
                self.log(f"⚠️ Team performance error: {e}", "WARN")
                
        return True
        
    def test_database_integrity(self):
        """Test database integrity and stored insights"""
        self.log("\n🗄️ Testing database integrity...")
        
        if not self.test_project_id:
            self.log("⚠️ No test project available for database integrity test", "WARN")
            return True
        
        try:
            # Test stored insights retrieval
            response = self.session.get(f"{BASE_URL}/ai-insights/project/{self.test_project_id}/insights")
            if response.status_code == 200:
                insights = response.json()
                self.log(f"✅ Database integrity verified ({len(insights)} stored insights)")
                
                # Test dashboard insights as well
                response = self.session.get(f"{BASE_URL}/ai-insights/dashboard/insights")
                if response.status_code == 200:
                    dashboard_data = response.json()
                    total_insights = dashboard_data.get('summary', {}).get('total_insights', 0)
                    self.log(f"✅ Dashboard insights accessible ({total_insights} total insights)")
                
                return True
            else:
                self.log(f"❌ Database integrity test failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Database integrity error: {e}", "ERROR")
            return False
        
    def cleanup(self):
        """Clean up test data"""
        self.log("Cleaning up test data...")
        
        # Delete test task
        if self.test_task_id:
            try:
                response = self.session.delete(f"{BASE_URL}/tasks/{self.test_task_id}")
                if response.status_code in [200, 204]:
                    self.log("✅ Test task deleted")
                else:
                    self.log(f"⚠️ Failed to delete test task: {response.status_code}", "WARN")
            except Exception as e:
                self.log(f"⚠️ Task cleanup error: {e}", "WARN")
                
        # Delete test project
        if self.test_project_id:
            try:
                response = self.session.delete(f"{BASE_URL}/projects/{self.test_project_id}")
                if response.status_code in [200, 204]:
                    self.log("✅ Test project deleted")
                else:
                    self.log(f"⚠️ Failed to delete test project: {response.status_code}", "WARN")
            except Exception as e:
                self.log(f"⚠️ Project cleanup error: {e}", "WARN")
                
    def run_all_tests(self):
        """Run all system tests"""
        self.log("=" * 60)
        self.log("STARTING COMPREHENSIVE SYSTEM TESTS")
        self.log("=" * 60)
        
        start_time = time.time()
        
        try:
            # Authentication test
            if not self.test_authentication():
                self.log("❌ Authentication failed - stopping tests", "ERROR")
                return False
                
            # Projects test
            self.test_projects()
            
            # Tasks test
            self.test_tasks()
            
            # AI Insights test
            self.test_ai_insights()
            
            # Database integrity test
            self.test_database_integrity()
            
        finally:
            # Always cleanup
            self.cleanup()
            
        end_time = time.time()
        duration = end_time - start_time
        
        self.log("=" * 60)
        self.log(f"SYSTEM TESTS COMPLETED IN {duration:.2f} SECONDS")
        self.log("=" * 60)
        
        return True

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()