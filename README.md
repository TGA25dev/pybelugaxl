# 🐋 pybelugaxl

A Python library to track the Airbus BelugaXL flights in real time using FlightRadar24.

## Features
- Fetch current BelugaXL flights
- Filter by registration number, flight status, or departure/arrival airport
- Returns detailed flight information: position, speed, altitude, departure/arrival times

## Usage
```python
from pybelugaxl import get_beluga

flights = get_beluga(status="enroute")
for f in flights:
    print(f"{f.registration}: {f.from_airport} -> {f.to_airport}, Altitude: {f.altitude} ft")
```

## Attribution 
Data is provided by the unofficial [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI)
 library (MIT License).

## License
This project uses an MIT license, see [LICENSE](LICENSE) file for more information.