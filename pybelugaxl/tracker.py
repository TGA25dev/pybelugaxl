from FlightRadar24 import FlightRadar24API
from pybelugaxl._models import BelugaState
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

fr_api = FlightRadar24API()

_AIRBUS_INT_TRANSPORT_ICAO = "BGA"
_BELUGA_AIRCRAFT_TYPE = "A337"
_ZONES = fr_api.get_zones()
_EUROPE_BOUNDS = fr_api.get_bounds(_ZONES["europe"])

def get_beluga(registration:str=None, status:str=None, from_airport_icao:str=None, to_airport_icao:str=None) -> list[BelugaState]:
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
        
    beluga_flights = fr_api.get_flights(
        aircraft_type = _BELUGA_AIRCRAFT_TYPE,
        airline = _AIRBUS_INT_TRANSPORT_ICAO,
        bounds = _EUROPE_BOUNDS,
        registration = registration,
        details=True
    )
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
    
    logging.debug(f"Found {len(beluga_flights)} flights")

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
    logging.debug(f"Returning {len(results)} flights after filtering")
    return results