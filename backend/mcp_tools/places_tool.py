"""
Google Places API Search Tool
"""
import os
import httpx
from typing import Dict, List, Optional

async def search_places(
    destination: str,
    category: Optional[str] = None,
    keyword: Optional[str] = None
) -> Dict:
    """
    Search for attractions and POIs using Google Places API

    Args:
        destination: City or location name
        category: Category type (e.g., 'tourist_attraction', 'museum', 'restaurant')
        keyword: Optional keyword for refined search

    Returns:
        List of attractions with coordinates, ratings, and types
    """
    try:
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")

        if not api_key:
            raise ValueError("Google Places API key not configured")

        # First, geocode the destination
        async with httpx.AsyncClient() as client:
            geocode_response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={
                    "address": destination,
                    "key": api_key
                },
                timeout=15.0
            )
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()

        if not geocode_data.get("results"):
            raise ValueError(f"Could not geocode destination: {destination}")

        location = geocode_data["results"][0]["geometry"]["location"]

        # Search for places
        search_params = {
            "location": f"{location['lat']},{location['lng']}",
            "radius": 5000,  # 5km radius
            "key": api_key
        }

        if category:
            search_params["type"] = category
        if keyword:
            search_params["keyword"] = keyword

        async with httpx.AsyncClient() as client:
            places_response = await client.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params=search_params,
                timeout=15.0
            )
            places_response.raise_for_status()
            places_data = places_response.json()

        # Normalize response
        attractions = []
        for place in places_data.get("results", [])[:20]:
            place_location = place.get("geometry", {}).get("location", {})

            attractions.append({
                "name": place.get("name", "Unknown"),
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "types": place.get("types", []),
                "vicinity": place.get("vicinity", ""),
                "coordinates": {
                    "lat": place_location.get("lat", 0),
                    "lng": place_location.get("lng", 0)
                },
                "price_level": place.get("price_level"),
                "photo_reference": place.get("photos", [{}])[0].get("photo_reference") if place.get("photos") else None
            })

        return {
            "success": True,
            "destination": destination,
            "category": category,
            "keyword": keyword,
            "center_coordinates": {
                "lat": location["lat"],
                "lng": location["lng"]
            },
            "attractions": attractions,
            "total_found": len(attractions)
        }

    except Exception as e:
        # Return mock data if API fails
        return {
            "success": False,
            "error": str(e),
            "destination": destination,
            "attractions": [
                {"name": "Historic City Center", "rating": 4.6, "user_ratings_total": 2543, "types": ["tourist_attraction", "point_of_interest"], "vicinity": "Downtown", "coordinates": {"lat": 0, "lng": 0}},
                {"name": "National Museum", "rating": 4.8, "user_ratings_total": 1876, "types": ["museum", "tourist_attraction"], "vicinity": "Cultural District", "coordinates": {"lat": 0, "lng": 0}},
                {"name": "Central Park", "rating": 4.7, "user_ratings_total": 3421, "types": ["park", "tourist_attraction"], "vicinity": "City Center", "coordinates": {"lat": 0, "lng": 0}},
                {"name": "Old Town Market", "rating": 4.5, "user_ratings_total": 987, "types": ["shopping_mall", "tourist_attraction"], "vicinity": "Old Town", "coordinates": {"lat": 0, "lng": 0}},
                {"name": "Riverside Promenade", "rating": 4.4, "user_ratings_total": 1234, "types": ["park", "point_of_interest"], "vicinity": "Riverside", "coordinates": {"lat": 0, "lng": 0}}
            ],
            "total_found": 5,
            "note": "Using fallback data due to API error"
        }
