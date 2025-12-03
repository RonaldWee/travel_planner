"""
Budget Estimation Agent
LLM + MCP tools for comprehensive budget analysis
"""
from crewai import Agent, Task
from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field
import asyncio
from mcp_tools import lookup_budget

class BudgetLookupInput(BaseModel):
    """Input for budget lookup tool"""
    city: str = Field(..., description="City name")

class BudgetLookupTool(BaseTool):
    name: str = "Budget Lookup"
    description: str = "Look up budget and cost of living data for a city"
    args_schema: Type[BaseModel] = BudgetLookupInput
    
    def _run(self, city: str) -> Dict:
        # Create new event loop for sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in event loop, use run_in_executor
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, lookup_budget(city))
                    return future.result()
            else:
                return loop.run_until_complete(lookup_budget(city))
        except RuntimeError:
            return asyncio.run(lookup_budget(city))

budget_lookup_tool = BudgetLookupTool()

def create_budget_agent(llm) -> Agent:
    """Create the Budget Estimation Agent"""
    return Agent(
        role="Travel Budget Analyst",
        goal="Look up budget data and provide comprehensive budget estimates for traveling to {destination} across different spending tiers",
        backstory="""You are a financial travel advisor with expertise in analyzing travel
        costs worldwide. You combine flight and hotel data with local cost-of-living information
        to provide accurate budget estimates for tight, moderate, and flexible spending levels.""",
        verbose=True,
        allow_delegation=False,
        tools=[budget_lookup_tool],
        llm=llm
    )

def create_budget_task(
    agent: Agent,
    destination: str,
    flight_data: Dict[str, Any] = None,
    hotel_data: Dict[str, Any] = None,
    duration_days: int = 7
):
    """Create task for budget estimation"""

    flight_context = ""
    if flight_data:
        price_range = flight_data.get("price_range", {})
        flight_context = f"\nFlight costs: ${price_range.get('min', 0)} - ${price_range.get('max', 0)}"

    hotel_context = ""
    if hotel_data:
        price_range = hotel_data.get("price_range", {})
        hotel_context = f"\nHotel costs per night: ${price_range.get('min_per_night', 0)} - ${price_range.get('max_per_night', 0)}"

    description = f"""Estimate travel budget for {destination} for a {duration_days}-day trip.

Use the mcp_budget_lookup tool to get local cost estimates:
- city: {destination}

Context from other searches:
{flight_context}
{hotel_context}

After receiving budget data:
1. Combine flight, hotel, and daily costs
2. Provide estimates for THREE budget tiers:
   - **Tight**: Budget travel (hostels, street food, public transport)
   - **Moderate**: Mid-range travel (3-4★ hotels, mix of restaurants)
   - **Flexible**: Comfortable travel (4-5★ hotels, nice dining)

3. Break down daily costs:
   - Accommodation (per night)
   - Meals (breakfast, lunch, dinner)
   - Local transport
   - Activities/attractions

4. Calculate total trip cost including flights

Output Format:
{{
    "destination": "{destination}",
    "duration_days": {duration_days},
    "budget_tiers": {{
        "tight": {{
            "daily_total": float,
            "meals": float,
            "transport": float,
            "accommodation": float,
            "activities": float,
            "trip_total": float
        }},
        "moderate": {{...}},
        "flexible": {{...}}
    }},
    "notes": "budget tips and money-saving advice"
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with detailed budget breakdown for tight, moderate, and flexible spending levels"
    )
