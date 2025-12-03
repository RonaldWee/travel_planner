"""
Attractions & Activities Agent
MCP Tool + LLM for discovering things to do
"""
from crewai import Agent, Task
from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import asyncio
from mcp_tools import search_places

class PlacesSearchInput(BaseModel):
    """Input for places search tool"""
    location: str = Field(..., description="City or destination name")
    category: str = Field("tourist_attraction", description="Type of place (tourist_attraction, museum, park, restaurant)")

class PlacesSearchTool(BaseTool):
    name: str = "Places Search"
    description: str = "Search for attractions and places of interest in a location"
    args_schema: Type[BaseModel] = PlacesSearchInput
    
    def _run(self, location: str, category: str = "tourist_attraction") -> Dict:
        # Create new event loop for sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in event loop, use run_in_executor
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, search_places(location, category=category))
                    return future.result()
            else:
                return loop.run_until_complete(search_places(location, category=category))
        except RuntimeError:
            return asyncio.run(search_places(location, category=category))

places_search_tool = PlacesSearchTool()

def create_attractions_agent(llm) -> Agent:
    """Create the Attractions & Activities Agent"""
    return Agent(
        role="Local Attractions Expert",
        goal="Search for and discover must-see attractions and activities in {destination} tailored to traveler interests",
        backstory="""You are a local guide and cultural expert who knows the hidden gems
        and popular attractions in cities worldwide. You curate personalized lists of things
        to see and do based on interests like culture, adventure, food, or relaxation.""",
        verbose=True,
        allow_delegation=False,
        tools=[places_search_tool],
        llm=llm
    )

def create_attractions_task(
    agent: Agent,
    destination: str,
    interests: List[str] = None
):
    """Create task for attractions search and categorization"""

    interests_context = ""
    if interests:
        interests_context = f"\nUser interests: {', '.join(interests)}"

    categories = [
        "tourist_attraction",
        "museum",
        "park",
        "restaurant",
        "shopping_mall"
    ]

    description = f"""Find and categorize top attractions in {destination}.
{interests_context}

Use the mcp_places_search tool multiple times for different categories:
{chr(10).join([f"- Call with category: {cat}" for cat in categories])}

After collecting attraction data:
1. Categorize attractions into groups:
   - **Culture**: Museums, temples, historical sites
   - **Landmarks**: Famous monuments, viewpoints
   - **Nature/Outdoors**: Parks, gardens, beaches
   - **Food Districts**: Markets, food streets, famous restaurants
   - **Markets/Shopping**: Traditional markets, shopping districts
   - **Day Trips**: Nearby destinations for day excursions

2. For each attraction, provide:
   - Name and location
   - Brief description (enhance with your knowledge)
   - Rating and popularity
   - Recommended duration
   - Best time to visit

3. Prioritize based on:
   - High ratings and reviews
   - Cultural significance
   - User interests: {interests or 'general tourism'}

Output Format:
{{
    "destination": "{destination}",
    "categories": {{
        "culture": [
            {{
                "name": "attraction name",
                "description": "enriched description",
                "rating": float,
                "location": "area/district",
                "recommended_duration": "1-2 hours",
                "best_time": "morning/afternoon/evening",
                "coordinates": {{"lat": float, "lng": float}}
            }}
        ],
        "landmarks": [...],
        "nature": [...],
        "food_districts": [...],
        "markets": [...],
        "day_trips": [...]
    }},
    "top_picks": ["attraction1", "attraction2", "attraction3"],
    "notes": "general tips for sightseeing"
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with categorized attractions including descriptions, ratings, and visit recommendations"
    )
