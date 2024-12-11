# app.py
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import psutil
import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Production API Server",
    description="A production-ready FastAPI server with health checks and monitoring",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track server start time for uptime calculation
START_TIME = time.time()

def get_system_health() -> Dict[str, Any]:
    """Get system health metrics"""
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime = time.time() - START_TIME
    
    return {
        "cpu_usage_percent": cpu_percent,
        "memory_usage_percent": memory.percent,
        "memory_available_mb": memory.available / (1024 * 1024),
        "disk_usage_percent": disk.percent,
        "disk_available_gb": disk.free / (1024 * 1024 * 1024),
        "uptime_seconds": uptime
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Production API Server",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Production API Server"
    }

@app.get("/health/deep")
async def deep_health_check():
    """Detailed health check with system metrics"""
    try:
        system_health = get_system_health()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Production API Server",
            "system_metrics": system_health,
            "components": {
                "api": "operational",
                "database": "connected",  # You would check DB connection here
                "cache": "operational"    # You would check cache here
            }
        }
    except Exception as e:
        logger.error(f"Deep health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system health metrics"
        )

@app.get("/error")
async def trigger_error():
    """Endpoint that deliberately raises an error for testing"""
    logger.error("Test error endpoint accessed")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="This is a deliberate error for testing purposes"
    )

@app.get("/error/{error_type}")
async def custom_error(error_type: str):
    """Generate different types of errors for testing"""
    if error_type == "404":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    elif error_type == "401":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    elif error_type == "403":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden access"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Custom error of type: {error_type}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

# For running the server directly
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Production API Server")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )