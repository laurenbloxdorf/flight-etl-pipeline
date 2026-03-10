import requests

def extract_flights(bbox: tuple) -> list:
    """
    bbox = (min_lat, max_lat, min_lon, max_lon)
    Pulls live flight states from OpenSky Network (no API key needed).
    """
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": bbox[0],
        "lamax": bbox[1],
        "lomin": bbox[2],
        "lomax": bbox[3]
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("states", [])