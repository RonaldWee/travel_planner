"""
Airport and City code resolver - converts city/country names to IATA codes
"""

# Common destinations mapped to their primary airport codes (for flights)
DESTINATION_TO_AIRPORT = {
    # France
    "france": "CDG",  # Paris CDG
    "paris": "CDG",
    "paris, france": "CDG",
    
    # Japan
    "japan": "NRT",  # Tokyo Narita
    "tokyo": "NRT",
    "tokyo, japan": "NRT",
    
    # UK
    "uk": "LHR",
    "united kingdom": "LHR",
    "london": "LHR",
    "london, uk": "LHR",
    
    # USA
    "usa": "JFK",
    "united states": "JFK",
    "new york": "JFK",
    "los angeles": "LAX",
    "san francisco": "SFO",
    "chicago": "ORD",
    "miami": "MIA",
    
    # Asia
    "singapore": "SIN",
    "hong kong": "HKG",
    "bangkok": "BKK",
    "seoul": "ICN",
    
    # Europe
    "germany": "FRA",
    "berlin": "BER",
    "madrid": "MAD",
    "barcelona": "BCN",
    "rome": "FCO",
    "amsterdam": "AMS",
    
    # Add more as needed
}

# City codes for hotel searches (different from airport codes!)
DESTINATION_TO_CITY = {
    # France
    "france": "PAR",  # Paris city
    "paris": "PAR",
    "paris, france": "PAR",
    
    # Japan
    "japan": "TYO",  # Tokyo city
    "tokyo": "TYO",
    "tokyo, japan": "TYO",
    
    # UK
    "uk": "LON",
    "united kingdom": "LON",
    "london": "LON",
    "london, uk": "LON",
    
    # USA
    "usa": "NYC",
    "united states": "NYC",
    "new york": "NYC",
    "los angeles": "LAX",
    "san francisco": "SFO",
    "chicago": "CHI",
    "miami": "MIA",
    
    # Asia
    "singapore": "SIN",
    "hong kong": "HKG",
    "bangkok": "BKK",
    "seoul": "SEL",
    
    # Europe
    "germany": "FRA",
    "berlin": "BER",
    "madrid": "MAD",
    "barcelona": "BCN",
    "rome": "ROM",
    "amsterdam": "AMS",
    
    # Add more as needed
}

def resolve_airport_code(destination: str) -> str:
    """
    Convert destination name to airport code (for flights)
    
    Args:
        destination: City, country, or airport code
        
    Returns:
        IATA airport code
        
    Raises:
        ValueError: If destination cannot be resolved
    """
    dest_lower = destination.lower().strip()
    
    # If already a 3-letter code, return it
    if len(destination) == 3 and destination.isalpha():
        return destination.upper()
    
    # Try to find in mapping
    if dest_lower in DESTINATION_TO_AIRPORT:
        return DESTINATION_TO_AIRPORT[dest_lower]
    
    # Try partial matches (e.g., "Paris, France" -> "paris")
    for key, code in DESTINATION_TO_AIRPORT.items():
        if key in dest_lower or dest_lower in key:
            return code
    
    raise ValueError(
        f"Cannot resolve '{destination}' to an airport code. "
        f"Please use specific city names or 3-letter IATA codes (e.g., 'Paris' or 'CDG')"
    )

def resolve_city_code(destination: str) -> str:
    """
    Convert destination name to city code (for hotels)
    
    Args:
        destination: City, country, or city code
        
    Returns:
        IATA city code
        
    Raises:
        ValueError: If destination cannot be resolved
    """
    dest_lower = destination.lower().strip()
    
    # If already a 3-letter code, return it
    if len(destination) == 3 and destination.isalpha():
        return destination.upper()
    
    # Try to find in mapping
    if dest_lower in DESTINATION_TO_CITY:
        return DESTINATION_TO_CITY[dest_lower]
    
    # Try partial matches (e.g., "Tokyo, Japan" -> "tokyo")
    for key, code in DESTINATION_TO_CITY.items():
        if key in dest_lower or dest_lower in key:
            return code
    
    raise ValueError(
        f"Cannot resolve '{destination}' to a city code. "
        f"Please use specific city names or 3-letter IATA city codes (e.g., 'Tokyo' or 'TYO')"
    )
