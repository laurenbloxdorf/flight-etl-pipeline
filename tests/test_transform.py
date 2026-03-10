import sys
sys.path.insert(0, "./include")
from transform import transform_flights

def test_drops_flights_with_no_position():
    raw = [["abc123", "UAL123", "United States", None, 1700000000,
            None, None, 10000, False, 250, 90, 0, None, 9800, None, False, 0]]
    result = transform_flights(raw)
    assert result == []

def test_cleans_callsign_whitespace():
    raw = [["abc123", "UAL123  ", "United States", 1700000000, 1700000000,
            -87.6, 41.8, 10000, False, 250, 90, 0, None, 9800, None, False, 0]]
    result = transform_flights(raw)
    assert result[0]["callsign"] == "UAL123"

def test_rounds_coordinates():
    raw = [["abc123", "UAL123", "United States", 1700000000, 1700000000,
            -87.623456789, 41.812345678, 10000, False, 250, 90, 0, None, 9800, None, False, 0]]
    result = transform_flights(raw)
    assert result[0]["longitude"] == -87.6235
    assert result[0]["latitude"] == 41.8123