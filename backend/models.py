"""
Pydantic models for Travel Planner API
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class BudgetLevel(str, Enum):
    """Budget level options"""
    TIGHT = "tight"
    MODERATE = "moderate"
    FLEXIBLE = "flexible"

class TripType(str, Enum):
    """Trip type options"""
    SOLO = "solo"
    COUPLE = "couple"
    FAMILY = "family"
    FRIENDS = "friends"

class TravelPlanRequest(BaseModel):
    """Request model for /plan endpoint"""
    destination: str = Field(..., description="Destination city or country")
    origin: Optional[str] = Field(None, description="Origin city/airport code")
    departure_date: Optional[str] = Field(None, description="Specific departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Specific return date (YYYY-MM-DD)")
    budget_level: BudgetLevel = Field(BudgetLevel.MODERATE, description="Budget level")
    interests: Optional[List[str]] = Field(default_factory=list, description="User interests")
    trip_type: TripType = Field(TripType.SOLO, description="Type of trip")
    duration_days: Optional[int] = Field(7, description="Trip duration in days")

    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Tokyo",
                "origin": "SIN",
                "departure_date": "2025-04-15",
                "budget_level": "moderate",
                "interests": ["culture", "food", "history"],
                "trip_type": "couple",
                "duration_days": 7
            }
        }

class FlightOption(BaseModel):
    """Flight option model"""
    price: float
    currency: str
    duration: str
    segments: int
    one_way: bool

class HotelOption(BaseModel):
    """Hotel option model"""
    name: str
    rating: str
    price_per_night: float
    total_price: float
    currency: str
    area: str

class Attraction(BaseModel):
    """Attraction/POI model"""
    name: str
    rating: float
    types: Optional[List[str]] = []
    vicinity: Optional[str] = None
    location: Optional[str] = None  # Alternative to vicinity
    coordinates: Dict[str, float]
    description: Optional[str] = None
    recommended_duration: Optional[str] = None
    best_time: Optional[str] = None

class BudgetEstimate(BaseModel):
    """Budget estimation model"""
    daily_total: float
    meals: float
    transport: float
    accommodation: float
    airport_transfer: Optional[float] = None

class TravelPlanResponse(BaseModel):
    """Response model for /plan endpoint"""
    destination: str
    origin: Optional[str] = None
    best_dates: str
    weather_summary: str
    flight_options: List[FlightOption]
    hotel_options: List[HotelOption]
    budget_estimate: Dict[str, BudgetEstimate]
    attractions: Dict[str, List[Attraction]]
    itinerary: str
    tips: Dict[str, Any]
    execution_time: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Tokyo",
                "origin": "SIN",
                "best_dates": "March-May, September-November",
                "weather_summary": "Spring (March-May) offers mild weather and cherry blossoms...",
                "flight_options": [
                    {
                        "price": 850.0,
                        "currency": "SGD",
                        "duration": "PT8H30M",
                        "segments": 1,
                        "one_way": False
                    }
                ],
                "hotel_options": [
                    {
                        "name": "Shibuya Grand Hotel",
                        "rating": "4",
                        "price_per_night": 180.0,
                        "total_price": 1260.0,
                        "currency": "SGD",
                        "area": "Shibuya"
                    }
                ],
                "budget_estimate": {
                    "tight": {
                        "daily_total": 80,
                        "meals": 30,
                        "transport": 15,
                        "accommodation": 35
                    }
                },
                "attractions": {
                    "culture": [
                        {
                            "name": "Senso-ji Temple",
                            "rating": 4.7,
                            "types": ["tourist_attraction"],
                            "vicinity": "Asakusa",
                            "coordinates": {"lat": 35.7148, "lng": 139.7967}
                        }
                    ]
                },
                "itinerary": "# 7-Day Tokyo Itinerary\n\n## Day 1: Arrival...",
                "tips": {
                    "culture": ["Remove shoes indoors", "Bow when greeting"],
                    "transport": ["Get a Suica card", "Trains stop around midnight"],
                    "safety": ["Very safe city", "Keep belongings secure"]
                }
            }
        }
