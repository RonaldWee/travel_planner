"""
Seasonality & Timing Agent
LLM-only agent for determining best travel times
"""
from crewai import Agent
from typing import Dict, Any

def create_seasonality_agent(llm) -> Agent:
    """Create the Seasonality & Timing Agent"""
    return Agent(
        role="Travel Seasonality Expert",
        goal="Determine the best months to visit {destination} based on weather, festivals, and seasonal factors",
        backstory="""You are a world-renowned travel timing expert with deep knowledge of
        global weather patterns, seasonal tourism trends, and cultural festivals. You provide
        detailed insights on the best and worst times to visit any destination, considering
        weather conditions, crowd levels, and special events.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_seasonality_task(agent: Agent, destination: str, travel_month: str = None):
    """Create task for seasonality analysis"""
    from crewai import Task

    description = f"""Analyze the best times to visit {destination}. Provide:

1. **Best Months to Visit**: List the 2-3 best months with reasons
2. **Weather Summary**: Describe typical weather conditions throughout the year
3. **Seasonal Highlights**: Major festivals, events, or seasonal attractions
4. **Months to Avoid**: Times with extreme weather, overcrowding, or closures
5. **Peak vs Off-Peak**: Tourist season information

{f'The traveler is interested in visiting in {travel_month}. Comment on this timing.' if travel_month else ''}

Output Format:
{{
    "best_months": ["month1", "month2", "month3"],
    "weather_summary": "detailed weather description",
    "seasonal_highlights": ["highlight1", "highlight2"],
    "months_to_avoid": ["month1", "month2"],
    "peak_season": "months",
    "off_peak_season": "months",
    "travel_month_assessment": "assessment if specific month provided"
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with seasonality analysis including best months, weather summary, and seasonal highlights"
    )
