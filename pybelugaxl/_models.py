from dataclasses import dataclass

@dataclass(frozen=True)
class BelugaState:
    id: str
    registration: str
    from_airport: str
    to_airport: str
    scheduled_departure: str
    scheduled_arrival: str
    real_departure: str
    real_arrival: str
    estimated_arrival: str
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

