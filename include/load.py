import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host": "flights_db",  # Docker service name
    "port": 5432,
    "dbname": "flights_db",
    "user": "flights",
    "password": "flights"
}

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS flights (
    icao24          TEXT,
    callsign        TEXT,
    origin_country  TEXT,
    time_position   TIMESTAMP,
    last_contact    TIMESTAMP,
    longitude       FLOAT,
    latitude        FLOAT,
    baro_altitude   FLOAT,
    on_ground       BOOLEAN,
    velocity        FLOAT,
    true_track      FLOAT,
    vertical_rate   FLOAT,
    geo_altitude    FLOAT,
    squawk          TEXT,
    ingested_at     TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (icao24, last_contact)
);
"""

def load_flights(flights: list):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE)

    rows = [(
        f["icao24"], f["callsign"], f["origin_country"],
        f["time_position"], f["last_contact"], f["longitude"],
        f["latitude"], f["baro_altitude"], f["on_ground"],
        f["velocity"], f["true_track"], f["vertical_rate"],
        f["geo_altitude"], f["squawk"]
    ) for f in flights]

    execute_values(cur, """
        INSERT INTO flights (
            icao24, callsign, origin_country, time_position,
            last_contact, longitude, latitude, baro_altitude,
            on_ground, velocity, true_track, vertical_rate,
            geo_altitude, squawk
        ) VALUES %s
        ON CONFLICT (icao24, last_contact) DO NOTHING;
    """, rows)

    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(rows)} flights.")