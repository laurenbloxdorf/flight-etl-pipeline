from datetime import datetime

COLUMNS = [
    "icao24", "callsign", "origin_country", "time_position",
    "last_contact", "longitude", "latitude", "baro_altitude",
    "on_ground", "velocity", "true_track", "vertical_rate",
    "sensors", "geo_altitude", "squawk", "spi", "position_source"
]

def transform_flights(raw_states: list) -> list:
    transformed = []
    for state in raw_states:
        flight = dict(zip(COLUMNS, state))

        # Drop flights with no position data
        if flight["latitude"] is None or flight["longitude"] is None:
            continue

        # Clean callsign whitespace
        flight["callsign"] = (flight["callsign"] or "").strip() or None

        # Convert unix timestamps to datetime
        for col in ["time_position", "last_contact"]:
            if flight[col]:
                flight[col] = datetime.utcfromtimestamp(flight[col])

        # Round floats to 4 decimal places
        for col in ["latitude", "longitude", "baro_altitude", "velocity"]:
            if flight[col] is not None:
                flight[col] = round(float(flight[col]), 4)

        transformed.append(flight)

    return transformed