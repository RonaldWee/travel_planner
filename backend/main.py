"""
FastAPI Travel Planner Backend
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from typing import Dict, Any
import logging

from models import TravelPlanRequest, TravelPlanResponse
from orchestrator import TravelPlanningOrchestrator
from utils import load_environment

# Load environment variables
load_environment()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Travel Planner API",
    description="AI-powered travel planning with CrewAI and MCP tools",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator (lazy loading)
_orchestrator: TravelPlanningOrchestrator = None

def get_orchestrator() -> TravelPlanningOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")
        _orchestrator = TravelPlanningOrchestrator(openrouter_api_key)
    return _orchestrator

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Planner API",
        "version": "1.0.0",
        "endpoints": {
            "plan": "/plan - POST - Create travel plan",
            "health": "/health - GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "travel-planner-api"
    }

@app.post("/plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest) -> Dict[str, Any]:
    """
    Create a comprehensive travel plan

    This endpoint orchestrates all AI agents to:
    1. Analyze best travel times (Seasonality Agent)
    2. Search for flights (Flight Agent + MCP tools)
    3. Find accommodations (Hotel Agent + MCP tools)
    4. Estimate budgets (Budget Agent + MCP tools)
    5. Discover attractions (Attractions Agent + MCP tools)
    6. Generate itinerary (Itinerary Agent)
    7. Provide tips (Tips Agent)

    Returns:
        Complete travel plan with all information
    """
    try:
        logger.info(f"Received planning request for {request.destination}")

        # Convert request to dict
        request_data = {
            "destination": request.destination,
            "origin": request.origin or "SIN",
            "departure_date": request.departure_date or "2026-06-01",
            "return_date": request.return_date,
            "budget_level": request.budget_level,
            "interests": request.interests or [],
            "trip_type": request.trip_type,
            "duration_days": request.duration_days or 7
        }

        # Get orchestrator and execute planning
        orchestrator = get_orchestrator()
        result = await orchestrator.execute_planning(request_data)

        logger.info(f"Planning completed for {request.destination} in {result.get('execution_time', 0):.1f}s")

        return result

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Planning error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create travel plan: {str(e)}"
        )

@app.get("/destinations/popular")
async def get_popular_destinations():
    """Get list of popular destinations"""
    return {
        "destinations": [
            {"name": "Tokyo, Japan", "code": "NRT", "region": "Asia"},
            {"name": "Paris, France", "code": "CDG", "region": "Europe"},
            {"name": "Barcelona, Spain", "code": "BCN", "region": "Europe"},
            {"name": "Bangkok, Thailand", "code": "BKK", "region": "Asia"},
            {"name": "Rome, Italy", "code": "FCO", "region": "Europe"},
            {"name": "Dubai, UAE", "code": "DXB", "region": "Middle East"},
            {"name": "New York, USA", "code": "JFK", "region": "North America"},
            {"name": "London, UK", "code": "LHR", "region": "Europe"},
            {"name": "Singapore", "code": "SIN", "region": "Asia"},
            {"name": "Istanbul, Turkey", "code": "IST", "region": "Europe/Asia"}
        ]
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
