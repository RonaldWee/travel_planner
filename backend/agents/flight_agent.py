"""
Flight Search Agent
MCP Tool-based agent for flight search
"""
from crewai import Agent, Task
from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Optional, Type
from pydantic import BaseModel, Field
import asyncio
from mcp_tools import search_flights

class FlightSearchInput(BaseModel):
    """Input for flight search tool"""
    origin: str = Field(..., description="Origin airport code (3 letters)")
    destination: str = Field(..., description="Destination airport code (3 letters)")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: str = Field(..., description="Return date (YYYY-MM-DD)")

class FlightSearchTool(BaseTool):
    name: str = "Flight Search"
    description: str = "Search for flights between two airports"
    args_schema: Type[BaseModel] = FlightSearchInput
    
    def _run(self, origin: str, destination: str, departure_date: str, return_date: str) -> Dict:
        # Create new event loop for sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in event loop, use run_in_executor
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, search_flights(origin, destination, departure_date, return_date))
                    return future.result()
            else:
                return loop.run_until_complete(search_flights(origin, destination, departure_date, return_date))
        except RuntimeError:
            return asyncio.run(search_flights(origin, destination, departure_date, return_date))

flight_search_tool = FlightSearchTool()

def create_flight_agent(llm) -> Agent:
    """Create the Flight Search Agent"""
    return Agent(
        role="Flight Search Specialist",
        goal="Search for flights and analyze flight options to provide recommendations",
        backstory="""You are an expert flight search specialist who searches for flights,
        analyzes options, compares prices, and identifies the best deals considering
        duration, number of stops, and value for money.""",
        verbose=True,
        allow_delegation=False,
        tools=[flight_search_tool],
        llm=llm
    )

def create_flight_task(
    agent: Agent,
    origin: str,
    destination: str,
    departure_date: Optional[str] = None,
    return_date: Optional[str] = None
):
    """Create task for flight search"""

    description = f"""Search for flight options from {origin} to {destination}.

Use the mcp_flight_search tool with these parameters:
- origin: {origin}
- destination: {destination}
- departure_date: {departure_date or "2025-06-01 (or suitable date)"}
{f"- return_date: {return_date}" if return_date else ""}

After receiving flight data:
1. Identify 3-5 representative flight options
2. Calculate price range (min-max)
3. Summarize average duration
4. Note if flights are direct or have connections

Output Format:
{{
    "origin": "{origin}",
    "destination": "{destination}",
    "flights": [
        {{
            "price": float,
            "currency": "SGD",
            "duration": "duration string",
            "segments": int,
            "one_way": boolean
        }}
    ],
    "price_range": {{"min": float, "max": float}},
    "average_duration": "duration string",
    "notes": "any relevant observations"
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with flight options, price ranges, and travel duration information"
    )
