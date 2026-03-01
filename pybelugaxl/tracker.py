from FlightRadar24 import FlightRadar24API
from pybelugaxl._models import BelugaState
import logging
import os
import json
import json

logger = logging.getLogger(__name__)

fr_api = FlightRadar24API()

_AIRBUS_INT_TRANSPORT_ICAO = "BGA"
_BELUGA_AIRCRAFT_TYPE = "A337"
_ZONES = fr_api.get_zones()
_EUROPE_BOUNDS = fr_api.get_bounds(_ZONES["europe"])
_CURRENT_PATH=os.path.dirname(__file__)

def _get_all_zone_names(zones_dict, parent_key='') -> dict:
    """Recursively extract all zone names including subzones."""
    zone_names = {}
    for key, value in zones_dict.items():
        zone_names[key] = value
        if isinstance(value, dict) and 'subzones' in value:
            subzones = _get_all_zone_names(value['subzones'], key)
            zone_names.update(subzones)
    return zone_names

_ALL_ZONES = _get_all_zone_names(_ZONES)

def get_beluga(registration:str=None, status:str=None, from_airport_icao:str=None, to_airport_icao:str=None, zone:str=None) -> list[BelugaState]:
    """
    Get detailed information about Beluga flights, with optional filtering by registration, status, and airports.
    
    Args:
        registration (str, optional): The registration number of the Beluga to filter by. ("F-GXLG" for example).
        status (str, optional): The status of the flight to filter by. Must be either "enroute" or "on_ground".
        from_airport_icao (str, optional): The ICAO code of the departure airport to filter by.
        to_airport_icao (str, optional): The ICAO code of the destination airport to filter by.
    
    Returns:
        list: Detailed information about the Beluga flight
    """
    if registration:
        registration = registration.upper()
        if len(registration) < 5 or len(registration) > 7:
            raise ValueError("Invalid registration. Please provide a valid plane registration number.")
        
    if to_airport_icao:
        to_airport_icao = to_airport_icao.upper()
        if len(to_airport_icao) != 4:
            raise ValueError("Invalid to_airport_icao. Please provide a valid 4-letter ICAO code.")

    if from_airport_icao:
        from_airport_icao = from_airport_icao.upper()
        if len(from_airport_icao) != 4:
            raise ValueError("Invalid from_airport_icao. Please provide a valid 4-letter ICAO code.")
        
    if status:
        status = status.lower()

        if status not in ["enroute", "on_ground"]:
            raise ValueError("Invalid status. Must be 'enroute' or 'on_ground'")
    
    if zone:
        if isinstance(zone, str):
            zone = zone.lower() 
            if zone not in _ALL_ZONES: 
                raise ValueError(f"Invalid zone. Must be one of: {', '.join(sorted(_ALL_ZONES.keys()))}")
            zone = fr_api.get_bounds(_ALL_ZONES[zone])
        
        elif isinstance(zone, tuple) and len(zone) == 3:
            if not (-90 <= zone[0] <= 90) or not (-180 <= zone[1] <= 180) or not (-10000 <= zone[2] <= 10000):
                raise ValueError("Invalid bounds. Latitude must be between -90 and 90, and longitude must be between -180 and 180. Range must be between -10000 and 10000 km.")
            try:
                zone = fr_api.get_bounds_by_point(zone[0], zone[1], radius=zone[2])

            except Exception as e:
                logger.error(f"Error getting bounds for the provided coordinates: {e}")
                raise ValueError(f"Error getting bounds for the provided coordinates: {e}")
            
        else:
            raise ValueError("Invalid zone. Must be a string representing a zone name or a tuple of (latitude, longitude, range in km).")
        
    beluga_flights = fr_api.get_flights(
        aircraft_type = _BELUGA_AIRCRAFT_TYPE,
        airline = _AIRBUS_INT_TRANSPORT_ICAO,
        bounds = _EUROPE_BOUNDS if not zone else zone,
        registration = registration,
        details=True
    )
    logger.debug(f"Found {len(beluga_flights)} flights")

    results = []

    for flight in beluga_flights:
        flight_details = fr_api.get_flight_details(flight)
        flight.set_flight_details(flight_details) #get all details of the plane

        #Filters, if condition is not met, flight is skipped
        if from_airport_icao and flight.origin_airport_icao != from_airport_icao:
            continue

        if to_airport_icao and flight.destination_airport_icao != to_airport_icao:
            continue

        if status and BelugaState._status(flight.altitude, flight.ground_speed) != status:
            continue

        results.append(
            BelugaState( #add results to the class
                id=flight.id,
                registration=flight.registration,
                from_airport=flight.origin_airport_name,
                to_airport=flight.destination_airport_name,
                scheduled_departure=flight.time_details["scheduled"]["departure"] if flight.time_details["scheduled"] else None,
                scheduled_arrival=flight.time_details["scheduled"]["arrival"] if flight.time_details["scheduled"] else None,
                real_departure=flight.time_details["real"]["departure"] if flight.time_details["real"] else None,
                real_arrival=flight.time_details["real"]["arrival"] if flight.time_details["real"] else None,
                eta=flight.time_details["other"]["eta"] if flight.time_details["other"] and "eta" in flight.time_details["other"] else None,
                altitude=flight.altitude, #feets
                ground_speed=flight.ground_speed, #knots
                heading=flight.heading, #degrees
                position=(flight.latitude, flight.longitude),
                status=BelugaState._status(flight.altitude, flight.ground_speed),
                last_update=flight.time_details["other"]["updated"]

            )
        )
    logger.debug(f"Returning {len(results)} flights after filtering")
    return results

def is_beluga_in_zone(zone: str | tuple, registration: str = None, status:str=None, from_airport_icao:str=None, to_airport_icao:str=None) -> bool: 
    """ Check if a beluga flight is within a specified zone. Valid data is latitude, longitude coordinates or zone name.
    
    Args: 
        zone (str | tuple): The name of the zone to check against. Or a tuple of (latitude, longitude, range in km) to define a custom zone. For example: "france" or (48.8566, 2.3522, 100).
        registration (str, optional): The registration number of the Beluga to filter by. ("F-GXLG" for example).
        status (str, optional): The status of the flight to filter by. Must be either "enroute" or "on_ground".
        from_airport_icao (str, optional): The ICAO code of the departure airport to filter by.
        to_airport_icao (str, optional): The ICAO code of the destination airport to filter by.
        
    Returns: 
        bool: True if there's a beluga flight within the specified zone, False otherwise. """ 
    
    
    beluga_flights = get_beluga(registration=registration, zone=zone, status=status, from_airport_icao=from_airport_icao, to_airport_icao=to_airport_icao)
    if beluga_flights:
        return len(beluga_flights) > 0 #if 1 or more flights are found, return True
    
    return False

def get_beluga_fleet_status() -> dict:
    """Get the current status of the entire Beluga fleet, including the number of planes in the air and on the ground."""
    beluga_flights = get_beluga()
    fleet_status = {
        "total": len(beluga_flights),
        "enroute": sum(1 for flight in beluga_flights if flight.status == "enroute"),
        "on_ground": sum(1 for flight in beluga_flights if flight.status == "on_ground"),
        "unknown": sum(1 for flight in beluga_flights if flight.status == "unknown")
    }
    return fleet_status

def get_fleet_data():
    """Get static data about the Beluga fleet."""
    with open(f"{_CURRENT_PATH}/data/fleet_data.json", "r") as json_file:
        data = json.load(json_file)
    
    return data