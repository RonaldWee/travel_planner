"""
Amadeus Hotel Search Tool
"""
import os
import httpx
from typing import Dict, List, Optional

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

async def get_city_code(location: str, token: str) -> Optional[str]:
    """Get IATA city code for a location"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://test.api.amadeus.com/v1/reference-data/locations",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "keyword": location,
                    "subType": "CITY"
                },
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                return data["data"][0].get("iataCode")
        return None
    except:
        return None

async def search_hotels(
    location: str,
    check_in_date: str,
    check_out_date: str
) -> Dict:
    """
    Search for hotel options using Amadeus API

    Args:
        location: City IATA code (3 letters) or city name
        check_in_date: Check-in date (YYYY-MM-DD)
        check_out_date: Check-out date (YYYY-MM-DD)

    Returns:
        Simplified hotel area data with price ranges
    """
    try:
        token = await get_amadeus_token()
        
        # If already a 3-letter code, use it directly
        if len(location) == 3 and location.isalpha():
            city_code = location.upper()
            print(f"🏨 Using city code directly: {city_code}")
        else:
            # Try to resolve via Amadeus API
            city_code = await get_city_code(location, token)
            if not city_code:
                raise ValueError(f"Could not find city code for {location}")
            print(f"🏨 Resolved '{location}' to city code: {city_code}")

        async with httpx.AsyncClient() as client:
            # Step 1: Get hotel IDs for the city
            print(f"🔍 Searching for hotels in city: {city_code}")
            hotels_response = await client.get(
                "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "cityCode": city_code,
                    "radius": 1,
                    "radiusUnit": "KM",
                    "hotelSource": "ALL"
                },
                timeout=30.0
            )
            hotels_response.raise_for_status()
            hotels_data = hotels_response.json()
            # Extract hotel IDs (limit to first 10 to avoid too many API calls)
            hotel_ids = [hotel["hotelId"] for hotel in hotels_data.get("data", [])[:10]]
            
            if not hotel_ids:
                raise ValueError(f"No hotels found in {city_code}")
            
            print(f"✅ Found {len(hotel_ids)} hotels, fetching offers (one at a time)...")
            
            # Step 2: Get offers for each hotel individually
            # API only accepts one hotelId at a time
            all_hotel_data = []
            for i, hotel_id in enumerate(hotel_ids, 1):
                try:
                    response = await client.get(
                        "https://test.api.amadeus.com/v3/shopping/hotel-offers",
                        headers={"Authorization": f"Bearer {token}"},
                        params={
                            "hotelIds": hotel_id,
                            "checkInDate": check_in_date,
                            "checkOutDate": check_out_date,
                            "adults": 1,
                            "currency": "SGD",
                            "bestRateOnly": True
                        },
                        timeout=15.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("data"):
                            all_hotel_data.extend(data["data"])
                            print(f"  ✅ Hotel {i}/{len(hotel_ids)}: Found offers")
                        else:
                            print(f"  ⚠️ Hotel {i}/{len(hotel_ids)}: No offers available")
                    elif response.status_code == 429:
                        print(f"  ⚠️ Hotel {i}/{len(hotel_ids)}: Rate limit - stopping search")
                        break  # Stop on rate limit
                    else:
                        error_data = response.json() if response.text else {}
                        error_msg = error_data.get("errors", [{}])[0].get("detail", "Unknown error") if error_data.get("errors") else response.text[:100]
                        print(f"  ❌ Hotel {i}/{len(hotel_ids)}: {response.status_code} - {error_msg}")
                except Exception as e:
                    print(f"  ❌ Hotel {i}/{len(hotel_ids)}: {str(e)[:80]}")
                    continue
            
            print(f"📊 Total hotels with offers: {len(all_hotel_data)}")

        # Normalize response
        hotel_options = []
        for hotel in all_hotel_data[:5]:
            offers = hotel.get("offers", [])
            if not offers:
                continue

            offer = offers[0]
            price = offer.get("price", {})

            hotel_options.append({
                "name": hotel.get("hotel", {}).get("name", "Unknown Hotel"),
                "rating": hotel.get("hotel", {}).get("rating", "N/A"),
                "price_per_night": float(price.get("base", 0)),
                "total_price": float(price.get("total", 0)),
                "currency": price.get("currency", "SGD"),
                "area": hotel.get("hotel", {}).get("cityCode", city_code)
            })
        
        print(f"✅ Parsed {len(hotel_options)} hotel options with valid offers")
        
        # If no hotels with offers, return fallback
        if not hotel_options:
            print(f"⚠️ No hotels available for {check_in_date} to {check_out_date}, using fallback data")
            return {
                "success": False,
                "error": "No hotels available for selected dates",
                "location": location,
                "city_code": city_code,
                "hotels": [
                    {"name": "City Center Hotel", "rating": "4", "price_per_night": 120, "total_price": 360, "currency": "SGD", "area": "Downtown"},
                    {"name": "Historic District Inn", "rating": "3", "price_per_night": 85, "total_price": 255, "currency": "SGD", "area": "Old Town"},
                    {"name": "Modern Business Hotel", "rating": "4", "price_per_night": 150, "total_price": 450, "currency": "SGD", "area": "Business District"},
                    {"name": "Boutique Riverside Hotel", "rating": "5", "price_per_night": 220, "total_price": 660, "currency": "SGD", "area": "Riverside"},
                    {"name": "Budget Traveler Hostel", "rating": "3", "price_per_night": 45, "total_price": 135, "currency": "SGD", "area": "Student Quarter"}
                ],
                "price_range": {"min_per_night": 45, "max_per_night": 220},
                "note": "Using fallback data - no availability for selected dates"
            }

        return {
            "success": True,
            "location": location,
            "city_code": city_code,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "hotels": hotel_options,
            "price_range": {
                "min_per_night": min([h["price_per_night"] for h in hotel_options]) if hotel_options else 0,
                "max_per_night": max([h["price_per_night"] for h in hotel_options]) if hotel_options else 0
            }
        }

    except Exception as e:
        # Log detailed error information
        import traceback
        print(f"❌ Hotel search failed for '{location}':")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        
        # Return mock data if API fails
        return {
            "success": False,
            "error": str(e),
            "location": location,
            "hotels": [
                {"name": "City Center Hotel", "rating": "4", "price_per_night": 120, "total_price": 360, "currency": "SGD", "area": "Downtown"},
                {"name": "Historic District Inn", "rating": "3", "price_per_night": 85, "total_price": 255, "currency": "SGD", "area": "Old Town"},
                {"name": "Modern Business Hotel", "rating": "4", "price_per_night": 150, "total_price": 450, "currency": "SGD", "area": "Business District"},
                {"name": "Boutique Riverside Hotel", "rating": "5", "price_per_night": 220, "total_price": 660, "currency": "SGD", "area": "Riverside"},
                {"name": "Budget Traveler Hostel", "rating": "3", "price_per_night": 45, "total_price": 135, "currency": "SGD", "area": "Student Quarter"}
            ],
            "price_range": {"min_per_night": 45, "max_per_night": 220},
            "note": "Using fallback data due to API error"
        }
