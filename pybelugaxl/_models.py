from dataclasses import dataclass

@dataclass(frozen=True)
class BelugaState:
    """
    Represents the current state of a Beluga aircraft.
    
    Attributes:
        id: Unique flight identifier
        registration: Aircraft registration number
        from_airport: Departure airport name
        to_airport: Destination airport name
        scheduled_departure: Scheduled departure time (Unix timestamp)
        scheduled_arrival: Scheduled arrival time (Unix timestamp)
        real_departure: Actual departure time (Unix timestamp)
        real_arrival: Actual arrival time (Unix timestamp, None if not landed)
        eta: Estimated time of arrival (Unix timestamp)
        altitude: Current altitude in feet
        ground_speed: Current ground speed in knots
        heading: Current heading in degrees (0-360)
        position: Current position as (latitude, longitude)
        status: Flight status - "enroute", "on_ground", or "unknown"
        last_update: Last data update time (Unix timestamp)
    """
    id: str
    registration: str
    from_airport: str
    to_airport: str
    scheduled_departure: str
    scheduled_arrival: str
    real_departure: str
    real_arrival: str
    eta: int
    altitude: int
    ground_speed: int
    heading: int
    position: tuple[int, int]
    status: str
    last_update: int

    @staticmethod
    def _status(altitude: int, ground_speed: int) -> str:
        if altitude > 1000 and ground_speed > 100:
            return "enroute"
        
        if altitude < 100 and ground_speed < 10:
            return "on_ground"
        
        return "unknown"
    
@dataclass(frozen=True)
class BelugaPhoto:
    """
    An image of a Beluga aircraft.
    
    Attributes:
        registration: Aircraft registration number
        url: URL of the image
        location: Location where the photo was taken
        photographer: Name of the photographer
        date_taken: Date the photo was taken
        date_uploaded: Date the photo was uploaded
    """

    registration: str
    url: str
    location: str
    photographer: str
    date_taken: str
    date_uploaded: str


@dataclass(frozen=True)
class BelugaFleetData:
    """
    Static data about the Beluga fleet or about a specific plane in the fleet
    
    Attributes:
        total_planes: Total number of Beluga planes in the fleet
        base_airport_icao: ICAO code of the base airport for the fleet
        plane_type_icao: ICAO code of the planes type
        operator_icao: ICAO code of the operator of the fleet
        
        xl_number: The unique number of the plane in the fleet
        msn: Manufacturer Serial Number of the plane
        status: Current status of the plane

        source: Sources of the data
    """
    total_planes: int
    base_airport_icao: str
    plane_type_icao: str
    operator_icao: str
    xl_number: str | None
    msn: int | None
    status: str | None
    source: list[dict[str, str]]
