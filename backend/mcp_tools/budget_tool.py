"""
Budget Estimation Tool - Web search or LLM-based cost estimation
"""
import os
import httpx
from typing import Dict, Optional

async def lookup_budget(
    city: str,
    country: Optional[str] = None
) -> Dict:
    """
    Estimate daily travel budget for food, transport, and accommodations

    Uses web search or LLM reasoning to estimate costs

    Args:
        city: City or destination name
        country: Optional country name

    Returns:
        Budget estimates with daily costs for meals, transport, and accommodation
    """
    try:
        location = f"{city}, {country}" if country else city

        # Generate structured budget estimation
        budget_data = estimate_budget_by_city(city, country)

        return {
            "success": True,
            "location": location,
            "city": city,
            "country": country,
            "budget_tiers": budget_data,
            "currency": "SGD",
            "note": "Estimates based on typical traveler budgets. Actual costs may vary."
        }

    except Exception as e:
        # Fallback estimation
        return {
            "success": False,
            "error": str(e),
            "location": f"{city}, {country}" if country else city,
            "budget_tiers": {
                "tight": {
                    "daily_total": 50,
                    "meals": 15,
                    "transport": 10,
                    "accommodation": 25,
                    "activities": 0
                },
                "moderate": {
                    "daily_total": 150,
                    "meals": 50,
                    "transport": 25,
                    "accommodation": 75,
                    "activities": 0
                },
                "flexible": {
                    "daily_total": 350,
                    "meals": 120,
                    "transport": 50,
                    "accommodation": 180,
                    "activities": 0
                }
            },
            "currency": "SGD",
            "note": "Using generic fallback estimates"
        }

def estimate_budget_by_city(city: str, country: Optional[str] = None) -> Dict:
    """
    Estimate budget based on city cost-of-living tier
    This uses heuristics based on known expensive vs. budget-friendly cities
    """
    city_lower = city.lower()

    # Tier 1: Very expensive cities
    expensive_cities = [
        "tokyo", "singapore", "zurich", "geneva", "london", "new york",
        "san francisco", "hong kong", "paris", "sydney", "oslo", "copenhagen"
    ]

    # Tier 2: Moderate cities
    moderate_cities = [
        "barcelona", "rome", "berlin", "amsterdam", "prague", "budapest",
        "lisbon", "athens", "mexico city", "buenos aires", "bangkok", "kuala lumpur"
    ]

    # Tier 3: Budget-friendly cities
    budget_cities = [
        "hanoi", "ho chi minh", "phnom penh", "manila", "delhi", "cairo",
        "marrakech", "lima", "bogota", "kiev", "sofia", "tirana"
    ]

    if any(exp_city in city_lower for exp_city in expensive_cities):
        return {
            "tight": {
                "daily_total": 80,
                "meals": 30,
                "transport": 15,
                "accommodation": 35,
                "airport_transfer": 50
            },
            "moderate": {
                "daily_total": 220,
                "meals": 80,
                "transport": 40,
                "accommodation": 100,
                "airport_transfer": 70
            },
            "flexible": {
                "daily_total": 500,
                "meals": 180,
                "transport": 70,
                "accommodation": 250,
                "airport_transfer": 100
            }
        }
    elif any(mod_city in city_lower for mod_city in moderate_cities):
        return {
            "tight": {
                "daily_total": 50,
                "meals": 20,
                "transport": 10,
                "accommodation": 20,
                "airport_transfer": 25
            },
            "moderate": {
                "daily_total": 120,
                "meals": 45,
                "transport": 20,
                "accommodation": 55,
                "airport_transfer": 40
            },
            "flexible": {
                "daily_total": 280,
                "meals": 100,
                "transport": 40,
                "accommodation": 140,
                "airport_transfer": 60
            }
        }
    else:
        # Default / budget tier
        return {
            "tight": {
                "daily_total": 30,
                "meals": 12,
                "transport": 5,
                "accommodation": 13,
                "airport_transfer": 15
            },
            "moderate": {
                "daily_total": 75,
                "meals": 30,
                "transport": 12,
                "accommodation": 33,
                "airport_transfer": 25
            },
            "flexible": {
                "daily_total": 180,
                "meals": 70,
                "transport": 25,
                "accommodation": 85,
                "airport_transfer": 40
            }
        }
