---
title: Home
icon: material/home 
status: new
---

# 🐋 pybelugaxl Documentation

## Overview 
**pybelugaxl** allows you to:

- Track live BelugaXL aircraft positions and flight status
- Filter flights by registration, status, origin and destination
- Get detailed flight information including altitude, speed, heading
- Get global information about the fleet
- Easily fetch pictures of the planes

## Installation
Use `pip` to install the module with the following command:

```bash
pip install pybelugaxl
```

## Quick Start

Here's a simple example to get all active BelugaXL flights that are currently listed on FlightRadar24:

???+ note "No Beluga flights right now?"
    If no BelugaXL planes are currently flying you can still set the `demo` parameter to `True` to get mock data. 

    ```python
    # Get fake Beluga flights for demo purposes
    flights = get_beluga(demo=True)
    ```

For regular usage, use:
```python
from pybelugaxl import get_beluga

# Get all Beluga flights
flights = get_beluga()

for flight in flights:
    print(f"{flight.registration}: {flight.from_airport} → {flight.to_airport}")
    print(f"    Altitude: {flight.altitude} ft, Speed: {flight.ground_speed} kt")
```

Filter by criteria:
```python
# Get only flights that are enroute
enroute_flights = get_beluga(status="enroute")

# Get flights from a specific airport
toulouse_flights = get_beluga(from_airport_icao="LFBO")

# Track a specific aircraft
specific_beluga = get_beluga(registration="F-GXLJ")
```

## Documentation

### Functions

#### get_beluga
##### Parameters:

- `registration` *(str, optional)*: Filter by aircraft registration (e.g., “F-GXLJ”)
- `status` *(str, optional)*: Filter by flight status, either "enroute" or "on_ground"
- `from_airport_icao` *(str, optional)*: Filter by departure airport ICAO code (e.g., “LFBO”)
- `to_airport_icao` *(str, optional)*: Filter by destination airport ICAO code
- `zone` *(str | tuple, optional)*: Filter by zone name or a tuple of latitude, longitude, range in km (e.g., "france" or (48.8566, 2.3522, 100))
- `demo` *(bool, optional)*: Whether demo mode should be enabled or not, in demo mode mock data is returned

#### is_beluga_in_zone
##### Parameters:
- `zone` *(str | tuple)*: Filter by zone name or a tuple of latitude, longitude, range in km (e.g., "france" or (48.8566, 2.3522, 100))
- `registration` *(str, optional)*: Filter by aircraft registration (e.g., “F-GXLJ”)
- `status` *(str, optional)*: Filter by flight status, either "enroute" or "on_ground"
- `from_airport_icao` *(str, optional)*: Filter by departure airport ICAO code (e.g., “LFBO”)
- `to_airport_icao` *(str, optional)*: Filter by destination airport ICAO code

##### Returns:
- *bool*: True if there's a beluga flight within the specified zone, False otherwise

#### get_beluga_fleet_status
This function takes no parameters and returns the current status of the BelugaXL fleet (number of planes in the air, on the ground, etc..).

#### get_fleet_data
##### Parameters:
- `registration` *(str, optional)*: Filter by aircraft registration (e.g., “F-GXLJ”)

##### Returns:
- *list[BelugaFleetData]*: A list of BelugaFleetData objects containing static data about the fleet or about a specific plane.

#### get_images
##### Parameters:
- `registration` *(str, optional)*: Filter by aircraft registration (e.g., “F-GXLJ”) If not provided, a random BelugaXL registration is selected
- `limit` *(int, optional)*: The number of images to retrieve (default is 3, max is 15)

### Data Models

#### BelugaState
Represents the current state of a Beluga aircraft.
##### Attributes
- `id`: Unique flight identifier
- `registration`: Aircraft registration number
- `from_airport`: Departure airport name
- `to_airport`: Destination airport name
- `scheduled_departure`: Scheduled departure time *(Unix timestamp)*
- `scheduled_arrival`: Scheduled arrival time *(Unix timestamp)*
- `real_departure`: Actual departure time *(Unix timestamp)*
- `real_arrival`: Actual arrival time *(Unix timestamp, None if not landed)*
- `eta`: Estimated time of arrival *(Unix timestamp)*
- `altitude`: Current altitude in feet
- `ground_speed`: Current ground speed in knots
- `heading`: Current heading in degrees (0-360)
- `position`: Current position as (latitude, longitude)
- `status`: Flight status - "enroute", "on_ground", or "unknown"
- `last_update`: Last data update time *(Unix timestamp)*

#### BelugaPhoto
An image of a Beluga aircraft.
##### Attributes
- `registration`: Aircraft registration number
- `url`: URL of the image
- `location`: Location where the photo was taken
- `photographer`: Name of the photographer
- `date_taken`: Date the photo was taken
- `date_uploaded`: Date the photo was uploaded

#### BelugaFleetData
Static data about the Beluga fleet or about a specific plane in the fleet
##### Attributes
- `total_planes`: Total number of Beluga planes in the fleet
- `base_airport_icao`: ICAO code of the base airport for the fleet
- `plane_type_icao`: ICAO code of the plane type
- `operator_icao`: ICAO code of the operator of the fleet
- `xl_number`: The unique number of the plane in the fleet
- `msn`: Manufacturer Serial Number of the plane
- `status`: Current status of the plane
- `source`: Sources of the data

### Exceptions
To be added one day <small>(probably never..)</small>