import os
import json
from .tracker import get_beluga

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

#TODO: Find some way to filter the data from the JSON file..
def get_fleet_data():
    """Get static data about the Beluga fleet."""
    with open(f"{_CURRENT_PATH}/data/fleet_data.json", "r") as json_file:
        data = json.load(json_file)
    
    return data