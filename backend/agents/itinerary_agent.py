"""
Itinerary Planner Agent
LLM-only agent for creating day-by-day itineraries
"""
from crewai import Agent, Task
from typing import Dict, Any, List

def create_itinerary_agent(llm) -> Agent:
    """Create the Itinerary Planner Agent"""
    return Agent(
        role="Itinerary Planning Expert",
        goal="Create a detailed, optimized day-by-day itinerary for {destination} that balances activities, rest, and travel time",
        backstory="""You are a master itinerary planner who creates perfectly balanced travel
        schedules. You understand the importance of pacing, geographic clustering, and mixing
        different types of activities. Your itineraries are practical, efficient, and enjoyable.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_itinerary_task(
    agent: Agent,
    destination: str,
    duration_days: int,
    attractions_data: Dict[str, Any] = None,
    weather_data: Dict[str, Any] = None,
    hotel_data: Dict[str, Any] = None,
    budget_level: str = "moderate",
    interests: List[str] = None,
    trip_type: str = "solo"
):
    """Create task for itinerary planning"""

    attractions_summary = "Available attractions across various categories"
    if attractions_data and "categories" in attractions_data:
        categories = attractions_data["categories"]
        attractions_summary = f"Available attractions: {', '.join(categories.keys())}"

    weather_context = ""
    if weather_data:
        weather_context = f"\nWeather consideration: {weather_data.get('weather_summary', '')}"

    description = f"""Create a detailed {duration_days}-day itinerary for {destination}.

Trip Details:
- Duration: {duration_days} days
- Budget level: {budget_level}
- Trip type: {trip_type}
- Interests: {', '.join(interests) if interests else 'general tourism'}

Available Data:
{attractions_summary}
{weather_context}

Itinerary Guidelines:
1. **Day 1**: Arrival day - lighter schedule, nearby attractions, orientation
2. **Day 2-{duration_days-1}**: Full days with morning, afternoon, and evening activities
3. **Day {duration_days}**: Departure day - morning activities, travel to airport

4. For each day include:
   - **Morning** (9:00 AM - 12:00 PM): 1-2 activities
   - **Afternoon** (2:00 PM - 5:00 PM): 1-2 activities
   - **Evening** (6:00 PM - 9:00 PM): Dinner and evening activity

5. Optimization principles:
   - Group attractions by geographic area (minimize travel time)
   - Mix activity types (culture, nature, food, shopping)
   - Include rest breaks and meal times
   - Consider opening hours and best visiting times
   - Balance energetic and relaxed activities

6. Include practical details:
   - Estimated time at each location
   - Travel time between locations
   - Meal suggestions (specific restaurants/areas)
   - Tips for each day

Output Format (Markdown):

# {duration_days}-Day {destination} Itinerary

## Overview
Brief intro about the itinerary's focus and highlights

## Day 1: Arrival & Orientation
**Morning (Arrival)**
- Arrive at airport
- Transfer to hotel in [neighborhood] (~time)
- Check-in and freshen up

**Afternoon**
- 2:00 PM: [Attraction name] - [description] (~duration)
- Travel tip: [transportation advice]

**Evening**
- 6:00 PM: Dinner at [area/restaurant suggestion]
- 8:00 PM: [Evening activity]

**Day 1 Tips:** [practical advice]

## Day 2: [Theme for the day]
...

[Continue for all days]

## Practical Notes
- Best way to get around: [transport advice]
- Must-try foods: [food recommendations]
- Money-saving tips: [budget advice]"""

    return Task(
        description=description,
        agent=agent,
        expected_output=f"Detailed markdown itinerary with day-by-day breakdown including morning, afternoon, and evening activities for {duration_days} days"
    )
