"""
Amadeus Flight Search Tool
"""
import os
import httpx
from typing import Dict, List, Optional
from datetime import datetime

async def get_amadeus_token() -> str:
    """Get Amadeus API access token"""
    api_key = os.getenv("AMADEUS_API_KEY")
    api_secret = os.getenv("AMADEUS_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("Amadeus API credentials not configured")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": api_key,
                "client_secret": api_secret
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]

async def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None
) -> Dict:
    """
    Search for flights using Amadeus API

    Args:
        origin: Origin airport code (e.g., 'LAX')
        destination: Destination airport code (e.g., 'CDG')
        departure_date: Departure date (YYYY-MM-DD)
        return_date: Optional return date (YYYY-MM-DD)

    Returns:
        Normalized flight options with prices and durations
    """
    try:
        # Validate airport codes (must be 3 letters)
        origin = origin.upper().strip()
        destination = destination.upper().strip()
        
        if len(origin) != 3 or not origin.isalpha():
            raise ValueError(f"Invalid origin airport code: '{origin}'. Must be a 3-letter IATA code (e.g., 'LAX', 'JFK')")
        
        if len(destination) != 3 or not destination.isalpha():
            raise ValueError(f"Invalid destination airport code: '{destination}'. Must be a 3-letter IATA code (e.g., 'CDG', 'NRT'). Use city airport codes, not country names.")
        
        token = await get_amadeus_token()

        params = {
            "originLocationCode": origin.upper(),
            "destinationLocationCode": destination.upper(),
            "departureDate": departure_date,
            "adults": 1,
            "max": 5,
            "currencyCode": "SGD"
        }

        if return_date:
            params["returnDate"] = return_date

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://test.api.amadeus.com/v2/shopping/flight-offers",
                headers={"Authorization": f"Bearer {token}"},
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

        # Normalize response
        flight_options = []
        for offer in data.get("data", [])[:5]:
            price = offer.get("price", {})
            itineraries = offer.get("itineraries", [])

            # Calculate total duration
            total_duration = ""
            if itineraries:
                total_duration = itineraries[0].get("duration", "")

            flight_options.append({
                "price": float(price.get("total", 0)),
                "currency": price.get("currency", "SGD"),
                "duration": total_duration,
                "segments": len(itineraries[0].get("segments", [])) if itineraries else 0,
                "one_way": return_date is None
            })

        return {
            "success": True,
            "origin": origin.upper(),
            "destination": destination.upper(),
            "departure_date": departure_date,
            "return_date": return_date,
            "flights": flight_options,
            "price_range": {
                "min": min([f["price"] for f in flight_options]) if flight_options else 0,
                "max": max([f["price"] for f in flight_options]) if flight_options else 0
            }
        }

    except Exception as e:
        # Log the actual error
        print(f"❌ Flight search error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return mock data as fallback
        return {
            "success": False,
            "error": str(e),
            "origin": origin.upper(),
            "destination": destination.upper(),
            "flights": [
                {"price": 450, "currency": "SGD", "duration": "PT8H30M", "segments": 1, "one_way": return_date is None},
                {"price": 620, "currency": "SGD", "duration": "PT10H15M", "segments": 2, "one_way": return_date is None},
                {"price": 580, "currency": "SGD", "duration": "PT9H45M", "segments": 1, "one_way": return_date is None}
            ],
            "price_range": {"min": 450, "max": 620},
            "note": "Using fallback data due to API error"
        }
