"""
Master Travel Planning Orchestrator
Coordinates MCP tools and single Crew workflow
"""
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .llm_config import get_llm_for_crewai
from .crew import create_travel_planning_crew

# Import MCP tools
from mcp_tools import search_flights, search_hotels, search_places, lookup_budget

# Import airport and city code resolvers
from utils.airport_codes import resolve_airport_code, resolve_city_code

class TravelPlanningOrchestrator:
    """
    Master orchestrator that manages single Crew workflow.
    Agents have MCP tools and will call them directly during execution.
    """

    def __init__(self, openrouter_api_key: str):
        """Initialize orchestrator with LLM configuration"""
        self.llm = get_llm_for_crewai(openrouter_api_key, use_claude=False)
        print(f"✅ Using OpenRouter model: {self.llm}")
        print("   Environment configured for OpenRouter routing")

        # Storage for results
        self.results = {}

    async def execute_planning(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete travel planning workflow

        Args:
            request_data: User request with destination, preferences, etc.

        Returns:
            Complete travel plan with all outputs
        """
        start_time = datetime.now()

        destination = request_data["destination"]
        origin = request_data.get("origin", "SIN")
        departure_date = request_data.get("departure_date", "2026-06-01")
        duration_days = request_data.get("duration_days", 7)
        
        # Infer travel month from departure date
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d")
        travel_month = dep_date.strftime("%B")
        print(f"📅 Inferred travel month: {travel_month}")
        
        # Calculate return date if not provided
        return_date = request_data.get("return_date")
        if not return_date:
            ret_date = dep_date + timedelta(days=duration_days)
            return_date = ret_date.strftime("%Y-%m-%d")
            print(f"📅 Calculated return date: {departure_date} + {duration_days} days = {return_date}")

        print(f"\n{'='*60}")
        print(f"🌍 Starting Travel Planning for {destination}")
        print(f"{'='*60}\n")

        # Resolve airport/city codes upfront for agents to use
        print("🔍 Resolving location codes...")
        try:
            origin_code = resolve_airport_code(origin)
            dest_airport_code = resolve_airport_code(destination)
            dest_city_code = resolve_city_code(destination)
            print(f"   ✅ Origin: {origin} → {origin_code}")
            print(f"   ✅ Destination (airport): {destination} → {dest_airport_code}")
            print(f"   ✅ Destination (city): {destination} → {dest_city_code}")
            
            # Add resolved codes to request for agents
            request_data["origin_code"] = origin_code
            request_data["dest_airport_code"] = dest_airport_code
            request_data["dest_city_code"] = dest_city_code
        except ValueError as e:
            print(f"   ⚠️  {e}")

        # Run single Crew workflow - agents call MCP tools via their tools= parameter
        print(f"\n{'='*60}")
        print("🤖 Running Agent Crew Workflow...")
        print("   (Agents will call flight_search_tool, hotel_search_tool, etc.)")
        print(f"{'='*60}\n")
        
        crew = create_travel_planning_crew(self.llm, request_data)
        crew_result = crew.kickoff()

        # Parse crew output
        self.results["crew_output"] = self._parse_crew_output(crew_result)

        # Assemble final response
        execution_time = (datetime.now() - start_time).total_seconds()

        print(f"\n{'='*60}")
        print(f"✅ Planning Complete! ({execution_time:.1f}s)")
        print(f"{'='*60}\n")

        return self._assemble_final_response(
            destination=destination,
            origin=origin,
            execution_time=execution_time
        )

    def _parse_crew_output(self, output: Any) -> Dict:
        """Parse crew output"""
        try:
            # Crew returns task outputs
            if hasattr(output, 'tasks_output'):
                return {
                    "tasks": [str(task_output) for task_output in output.tasks_output]
                }
            return {"raw": str(output)}
        except Exception as e:
            return {"error": str(e), "raw": str(output)}

    def _assemble_final_response(
        self, destination: str, origin: str, execution_time: float
    ) -> Dict[str, Any]:
        """Assemble final response from crew output"""
        crew_output = self.results.get("crew_output", {})
        tasks = crew_output.get("tasks", [])

        # Parse agent outputs (they return JSON strings)
        seasonality_data = self._parse_json_safe(tasks[0] if len(tasks) > 0 else "{}")
        flights_data = self._parse_json_safe(tasks[1] if len(tasks) > 1 else "{}")
        hotels_data = self._parse_json_safe(tasks[2] if len(tasks) > 2 else "{}")
        budget_data = self._parse_json_safe(tasks[3] if len(tasks) > 3 else "{}")
        attractions_data = self._parse_json_safe(tasks[4] if len(tasks) > 4 else "{}")
        itinerary_str = tasks[5] if len(tasks) > 5 else "# Itinerary\n\nNo itinerary generated."
        tips_data = self._parse_json_safe(tasks[6] if len(tasks) > 6 else "{}")

        # Transform to match TravelPlanResponse model
        return {
            "destination": destination,
            "origin": origin,
            "best_dates": ", ".join(seasonality_data.get("best_months", [])) if seasonality_data.get("best_months") else "Year-round",
            "weather_summary": seasonality_data.get("weather_summary", "No weather information available."),
            "flight_options": flights_data.get("flights", []),
            "hotel_options": hotels_data.get("hotels", []),
            "budget_estimate": budget_data.get("budget_tiers", {}),
            "attractions": attractions_data.get("categories", {}),
            "itinerary": itinerary_str,
            "tips": tips_data,
            "execution_time": execution_time
        }

    def _parse_json_safe(self, text: str) -> Dict:
        """Safely parse JSON, handling both JSON strings and plain text"""
        try:
            # Remove markdown code blocks if present
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            # Try to parse as JSON
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            # If not valid JSON, return empty dict
            return {}
