"""
Data formatting utilities
"""
from typing import Dict, List, Any
import re

def format_duration(duration_str: str) -> str:
    """
    Format ISO 8601 duration to human-readable format
    Example: PT11H30M -> 11h 30m
    """
    if not duration_str:
        return "N/A"

    # Parse ISO 8601 duration
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', duration_str)
    if not match:
        return duration_str

    hours = match.group(1) or "0"
    minutes = match.group(2) or "0"

    parts = []
    if hours != "0":
        parts.append(f"{hours}h")
    if minutes != "0":
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "N/A"

def format_price(price: float, currency: str = "SGD") -> str:
    """Format price with currency symbol"""
    symbols = {
        "SGD": "S$",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{price:,.2f}"

def categorize_attractions(attractions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize attractions by type

    Categories:
    - Culture (temples, shrines, museums)
    - Landmarks (monuments, viewpoints)
    - Nature (parks, gardens)
    - Food (restaurants, markets)
    - Shopping (malls, districts)
    - Entertainment (theaters, venues)
    """
    categories = {
        "culture": [],
        "landmarks": [],
        "nature": [],
        "food": [],
        "shopping": [],
        "entertainment": [],
        "other": []
    }

    for attraction in attractions:
        types = attraction.get("types", [])

        # Categorize based on types
        if any(t in types for t in ["museum", "art_gallery", "hindu_temple", "church", "synagogue", "mosque"]):
            categories["culture"].append(attraction)
        elif any(t in types for t in ["tourist_attraction", "point_of_interest", "establishment"]):
            categories["landmarks"].append(attraction)
        elif any(t in types for t in ["park", "natural_feature", "campground"]):
            categories["nature"].append(attraction)
        elif any(t in types for t in ["restaurant", "cafe", "food", "bar"]):
            categories["food"].append(attraction)
        elif any(t in types for t in ["shopping_mall", "store", "clothing_store"]):
            categories["shopping"].append(attraction)
        elif any(t in types for t in ["night_club", "movie_theater", "casino"]):
            categories["entertainment"].append(attraction)
        else:
            categories["other"].append(attraction)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def format_budget_summary(budget_data: Dict[str, Any]) -> str:
    """Format budget data into readable summary"""
    lines = []
    for tier, data in budget_data.items():
        lines.append(f"\n**{tier.upper()} Budget:**")
        lines.append(f"- Daily Total: ${data.get('daily_total', 0)}")
        lines.append(f"- Meals: ${data.get('meals', 0)}")
        lines.append(f"- Transport: ${data.get('transport', 0)}")
        lines.append(f"- Accommodation: ${data.get('accommodation', 0)}")

    return "\n".join(lines)

def extract_city_from_destination(destination: str) -> str:
    """Extract city name from destination string"""
    # Remove country names and common suffixes
    city = destination.split(",")[0].strip()
    return city

def normalize_month(month_input: str) -> str:
    """Normalize month input to full month name"""
    months = {
        "jan": "January", "january": "January", "1": "January",
        "feb": "February", "february": "February", "2": "February",
        "mar": "March", "march": "March", "3": "March",
        "apr": "April", "april": "April", "4": "April",
        "may": "May", "5": "May",
        "jun": "June", "june": "June", "6": "June",
        "jul": "July", "july": "July", "7": "July",
        "aug": "August", "august": "August", "8": "August",
        "sep": "September", "september": "September", "9": "September",
        "oct": "October", "october": "October", "10": "October",
        "nov": "November", "november": "November", "11": "November",
        "dec": "December", "december": "December", "12": "December"
    }

    month_lower = month_input.lower().strip()
    return months.get(month_lower, month_input)
