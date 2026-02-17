# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Animals/Whale.png" alt="Whale" width="25" height="25" /> pybelugaxl

A Python library to track the Airbus BelugaXL flights in real time using FlightRadar24.

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Activities/Bullseye.png" alt="Bullseye" width="25" height="25" /> Features
- Fetch current BelugaXL flights
- Filter by registration number, flight status, or departure/arrival airport
- Return detailed flight information: position, speed, altitude, departure/arrival times
- Return a boolean if a specific aircraft is found in a given zone
- Get stats about the entire BelugaXL fleet

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Airplane%20Departure.png" alt="Airplane Departure" width="25" height="25" /> Usage
```python
from pybelugaxl import get_beluga, is_beluga_in_zone

flights = get_beluga(status="enroute")
for f in flights:
    print(f"{f.registration}: {f.from_airport} -> {f.to_airport}, Altitude: {f.altitude} ft")

in_zone = is_beluga_in_zone(zone="france", registration="F-GXLI")
print(in_zone)
```

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Light%20Bulb.png" alt="Light Bulb" width="25" height="25" /> Installation 
```bash
pip install pybelugaxl
```

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Link.png" alt="Link" width="25" height="25" /> Attribution 
Data is provided by the unofficial [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI)
 library (MIT License).

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Page%20with%20Curl.png" alt="Page with Curl" width="25" height="25" /> License
This project uses an MIT license, see [LICENSE](LICENSE) file for more information.