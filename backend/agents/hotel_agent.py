"""
Hotel Search Agent
MCP Tool-based agent for hotel search
"""
from crewai import Agent, Task
from crewai.tools.base_tool import BaseTool
from typing import Optional, Dict, Type
from pydantic import BaseModel, Field
import asyncio
from mcp_tools import search_hotels

class HotelSearchInput(BaseModel):
    """Input for hotel search tool"""
    location: str = Field(..., description="City code (3 letters) or city name")
    check_in_date: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    check_out_date: str = Field(..., description="Check-out date (YYYY-MM-DD)")

class HotelSearchTool(BaseTool):
    name: str = "Hotel Search"
    description: str = "Search for hotels in a city"
    args_schema: Type[BaseModel] = HotelSearchInput
    
    def _run(self, location: str, check_in_date: str, check_out_date: str) -> Dict:
        # Create new event loop for sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in event loop, use run_in_executor
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, search_hotels(location, check_in_date, check_out_date))
                    return future.result()
            else:
                return loop.run_until_complete(search_hotels(location, check_in_date, check_out_date))
        except RuntimeError:
            return asyncio.run(search_hotels(location, check_in_date, check_out_date))

hotel_search_tool = HotelSearchTool()

def create_hotel_agent(llm) -> Agent:
    """Create the Hotel Search Agent"""
    return Agent(
        role="Accommodation Search Specialist",
        goal="Search for hotels and find suitable accommodation options in {destination} across different neighborhoods and price ranges",
        backstory="""You are a hospitality expert who knows the best neighborhoods in every
        major city. You search for accommodations that offer great value, convenient locations,
        and match the traveler's budget and preferences.""",
        verbose=True,
        allow_delegation=False,
        tools=[hotel_search_tool],
        llm=llm
    )

def create_hotel_task(
    agent: Agent,
    destination: str,
    check_in_date: Optional[str] = None,
    check_out_date: Optional[str] = None,
    budget_level: str = "moderate"
):
    """Create task for hotel search"""

    description = f"""Search for hotel options in {destination}.

Use the mcp_hotel_search tool with these parameters:
- location: {destination}
- check_in_date: {check_in_date or "2025-06-01 (or suitable date)"}
- check_out_date: {check_out_date or "2025-06-08 (or suitable date)"}

After receiving hotel data:
1. Identify 3-5 representative hotel options across different areas
2. Note the neighborhoods/districts
3. Highlight price ranges per night
4. Consider {budget_level} budget level

Output Format:
{{
    "destination": "{destination}",
    "hotels": [
        {{
            "name": "hotel name",
            "rating": "rating",
            "price_per_night": float,
            "total_price": float,
            "currency": "SGD",
            "area": "neighborhood"
        }}
    ],
    "price_range": {{"min_per_night": float, "max_per_night": float}},
    "recommended_areas": ["area1", "area2"],
    "notes": "neighborhood descriptions and recommendations"
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with hotel options, neighborhood recommendations, and price ranges"
    )
