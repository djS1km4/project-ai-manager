from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from .database import engine, Base
from .routes import auth, projects, tasks, ai_insights, dashboard, admin

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Project AI Manager API",
    description="AI-powered project management system with intelligent insights and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://localhost:5173", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:3001", 
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(ai_insights.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Project AI Manager API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "project-ai-manager",
        "version": "1.0.0"
    }

@app.get("/api/v1/info")
async def get_api_info():
    """Get API information"""
    return {
        "name": "Project AI Manager API",
        "version": "1.0.0",
        "description": "AI-powered project management system",
        "features": [
            "User authentication and authorization",
            "Project management with team collaboration",
            "Task management with subtasks and comments",
            "AI-powered insights and analytics",
            "Risk assessment and progress prediction",
            "Team performance analysis",
            "Budget forecasting",
            "Real-time dashboard metrics"
        ],
        "endpoints": {
            "auth": "/api/v1/auth",
            "projects": "/api/v1/projects", 
            "tasks": "/api/v1/tasks",
            "ai_insights": "/api/v1/ai-insights"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors"""
    import traceback
    error_detail = str(exc)
    error_traceback = traceback.format_exc()
    
    # Log the full error for debugging (server-side only)
    print(f"❌ 500 Error: {error_detail}")
    print(f"   Traceback: {error_traceback}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path)
        }
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("🚀 Project AI Manager API is starting up...")
    print("📊 Database tables created successfully")
    print("🔗 API documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    print("🛑 Project AI Manager API is shutting down...")

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )