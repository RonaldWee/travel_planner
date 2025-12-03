"""
Culture, Safety & Transport Tips Agent
LLM-only agent for practical travel advice
"""
from crewai import Agent, Task

def create_tips_agent(llm) -> Agent:
    """Create the Culture, Safety & Transport Tips Agent"""
    return Agent(
        role="Local Culture & Safety Advisor",
        goal="Provide essential cultural etiquette, safety tips, and transportation advice for {destination}",
        backstory="""You are a seasoned expat and travel safety consultant who has lived in
        dozens of countries. You provide practical, honest advice about local customs, safety
        precautions, and transportation systems to help travelers navigate new destinations
        confidently and respectfully.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_tips_task(
    agent: Agent,
    destination: str,
    trip_type: str = "solo"
):
    """Create task for tips and advice"""

    description = f"""Provide comprehensive practical advice for traveling to {destination} (trip type: {trip_type}).

Cover the following categories:

1. **Cultural Etiquette**
   - Greetings and social customs
   - Dress code considerations
   - Dining etiquette
   - Photography restrictions
   - Religious/cultural sensitivities
   - Tipping customs

2. **Safety & Scams**
   - General safety level
   - Areas to avoid
   - Common tourist scams
   - Emergency numbers
   - Safety tips for {trip_type} travelers
   - Healthcare/pharmacy info

3. **Transportation**
   - Airport to city center (options, costs, duration)
   - Public transport system overview
   - Metro/bus/train card recommendations
   - Taxi/ride-share apps (safe options)
   - Walking vs. transport
   - Best transport apps

4. **Communication**
   - English proficiency level
   - Essential local phrases
   - SIM card/data options
   - Free WiFi availability

5. **Money Matters**
   - Currency and exchange
   - Credit card acceptance
   - ATM availability
   - Bargaining culture

6. **General Tips**
   - Best time to visit attractions (crowd avoidance)
   - Booking advice
   - What to pack specific to destination
   - Local apps to download

Output Format:
{{
    "destination": "{destination}",
    "culture_etiquette": {{
        "greetings": "...",
        "dress_code": "...",
        "dining": "...",
        "tips": ["tip1", "tip2"]
    }},
    "safety": {{
        "safety_level": "low/medium/high risk",
        "areas_to_avoid": ["area1"],
        "common_scams": ["scam1", "scam2"],
        "emergency_numbers": {{"police": "...", "ambulance": "..."}},
        "tips": ["tip1", "tip2"]
    }},
    "transportation": {{
        "airport_transfer": {{
            "options": ["metro", "taxi", "bus"],
            "recommended": "...",
            "cost": "...",
            "duration": "..."
        }},
        "public_transport": {{
            "description": "...",
            "card_name": "...",
            "cost_per_day": "...",
            "tips": ["tip1"]
        }},
        "apps": ["app1", "app2"]
    }},
    "communication": {{
        "english_level": "low/medium/high",
        "phrases": {{"hello": "...", "thank_you": "..."}},
        "sim_card": "..."
    }},
    "money": {{
        "currency": "...",
        "exchange_tips": "...",
        "card_acceptance": "...",
        "bargaining": "..."
    }},
    "general_tips": ["tip1", "tip2", "tip3"]
}}"""

    return Task(
        description=description,
        agent=agent,
        expected_output="JSON object with comprehensive cultural, safety, transportation, and practical travel tips"
    )
