import os
import json
import logging

from .tracker import get_beluga
from ._models import BelugaFleetData
from .exceptions import InvalidRegistrationError

logger = logging.getLogger(__name__)

_CURRENT_PATH=os.path.dirname(__file__)

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

def get_fleet_data(registration: str = None) -> list[BelugaFleetData]:
    """Get static data about the Beluga fleet.
    
    Args:
        registration (str, optional): Registration number to filter the data for a specific plane.
    
    Returns:
        list[BelugaFleetData]: A list of BelugaFleetData objects containing static data about the fleet or about a specific plane.
    """

    with open(f"{_CURRENT_PATH}/data/fleet_data.json", "r") as json_file:
        data = json.load(json_file)
        result = []

        total_planes = (data.get("fleet").keys())
        total_planes_count = len(total_planes)
        for x in total_planes:
            if "F-GX" not in x:
                total_planes_count -= 1

        fleet = data.get("fleet")
        base_airport_icao = fleet.get("base_airport_icao")
        plane_type_icao = fleet.get("plane_type_icao")
        operator_icao = fleet.get("operator_icao")

        sources = data.get("sources", [])

        if registration:
            registration = registration.upper()
            if len(registration) < 5 or len(registration) > 7:
                raise InvalidRegistrationError("Invalid registration. Please provide a valid plane registration number.")
        
            plane_data = fleet.get(registration)
            if plane_data:
                result.append(
                    BelugaFleetData(
                        total_planes=total_planes_count,
                        base_airport_icao=base_airport_icao,
                        plane_type_icao=plane_type_icao,
                        operator_icao=operator_icao,
                        xl_number=plane_data.get("xl_number"),
                        msn=plane_data.get("msn"),
                        status=plane_data.get("status"),
                        source=sources
                    )
                )

            else:
                logger.warning(f"No data found for registration {registration}")
                result = []
        else:
            result.append(
                BelugaFleetData(
                    total_planes=total_planes_count,
                    base_airport_icao=base_airport_icao,
                    plane_type_icao=plane_type_icao,
                    operator_icao=operator_icao,
                    xl_number=None,
                    msn=None,
                    status=None,
                    source=sources
                )
            )
    
        return result