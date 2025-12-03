"""
Crew configuration and management
Single Crew workflow for all travel planning agents
"""
from crewai import Crew, Process
from typing import Dict, Any
from datetime import datetime, timedelta

from agents import (
    create_seasonality_agent, create_seasonality_task,
    create_flight_agent, create_flight_task,
    create_hotel_agent, create_hotel_task,
    create_budget_agent, create_budget_task,
    create_attractions_agent, create_attractions_task,
    create_itinerary_agent, create_itinerary_task,
    create_tips_agent, create_tips_task
)

def create_travel_planning_crew(
    llm,
    request_data: Dict[str, Any]
) -> Crew:
    """
    Create a single CrewAI crew with all travel planning agents and tasks
    
    Agents have access to MCP tools and will call them as needed.

    Args:
        llm: Language model instance
        request_data: User request with destination, preferences, etc.

    Returns:
        Configured Crew instance with all tasks
    """
    
    # Extract request data
    destination = request_data["destination"]
    origin = request_data.get("origin", "SIN")
    departure_date = request_data.get("departure_date", "2025-06-01")
    duration_days = request_data.get("duration_days", 7)
    
    # Get resolved codes from orchestrator (already validated)
    origin_code = request_data.get("origin_code", origin)
    dest_airport_code = request_data.get("dest_airport_code", destination)
    dest_city_code = request_data.get("dest_city_code", destination)
    
    # Infer travel month from departure date
    dep_date = datetime.strptime(departure_date, "%Y-%m-%d")
    travel_month = dep_date.strftime("%B")
    
    # Calculate return date if not provided
    return_date = request_data.get("return_date")
    if not return_date:
        ret_date = dep_date + timedelta(days=duration_days)
        return_date = ret_date.strftime("%Y-%m-%d")
    
    budget_level = request_data.get("budget_level", "moderate")
    interests = request_data.get("interests", [])
    trip_type = request_data.get("trip_type", "solo")

    # Create all agents (they have tools= parameter to call MCP functions)
    seasonality_agent = create_seasonality_agent(llm)
    flight_agent = create_flight_agent(llm)
    hotel_agent = create_hotel_agent(llm)
    budget_agent = create_budget_agent(llm)
    attractions_agent = create_attractions_agent(llm)
    itinerary_agent = create_itinerary_agent(llm)
    tips_agent = create_tips_agent(llm)

    # Create all tasks - agents will call their tools during execution
    tasks = [
        create_seasonality_task(seasonality_agent, destination, travel_month),
        create_flight_task(flight_agent, origin_code, dest_airport_code, departure_date, return_date),
        create_hotel_task(hotel_agent, dest_city_code, departure_date, return_date),
        create_budget_task(budget_agent, destination, {}, {}, duration_days),
        create_attractions_task(attractions_agent, destination, interests),
        create_itinerary_task(
            itinerary_agent, destination, duration_days, {}, {}, {}, 
            budget_level, interests, trip_type
        ),
        create_tips_task(tips_agent, destination, trip_type)
    ]

    # Create crew with all 7 agents working sequentially
    crew = Crew(
        agents=[
            seasonality_agent,
            flight_agent,
            hotel_agent,
            budget_agent,
            attractions_agent,
            itinerary_agent,
            tips_agent
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        full_output=True
    )

    return crew
