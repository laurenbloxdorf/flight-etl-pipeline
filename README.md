# ✈️ Flight ETL Pipeline

A production-style ETL pipeline that ingests live flight data every 15 minutes, transforms it, and loads it into PostgreSQL — fully orchestrated with Apache Airflow and containerized with Docker.

---

## 🏗️ Architecture

```
OpenSky Network API
        │
        ▼
  [ Extract ]  →  Pulls live flight states over the continental US
        │
        ▼
  [ Transform ] →  Cleans nulls, normalizes timestamps, rounds coordinates
        │
        ▼
  [ Load ]      →  Upserts into PostgreSQL (conflict-safe)
        │
        ▼
   PostgreSQL
```

All three steps run as an **Airflow DAG** on a 15-minute schedule.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Apache Airflow 2.8 | Pipeline orchestration & scheduling |
| PostgreSQL 15 | Data storage |
| Python 3.x | ETL logic |
| Docker + Docker Compose | Containerization |
| OpenSky Network API | Live flight data source (free, no API key) |

---

## 📁 Project Structure

```
flight-etl-pipeline/
├── dags/
│   └── flight_etl_dag.py      # Airflow DAG definition
├── include/
│   ├── extract.py             # Pulls data from OpenSky API
│   ├── transform.py           # Cleans and normalizes raw data
│   └── load.py                # Upserts into PostgreSQL
├── tests/
│   └── test_transform.py      # Unit tests for transform logic
├── docker-compose.yml         # Spins up Airflow + PostgreSQL
└── requirements.txt
```

---

## 🚀 How to Run

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Git

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/flight-etl-pipeline.git
cd flight-etl-pipeline

# 2. Start all services
docker-compose up -d

# 3. Wait ~60 seconds, then create an Airflow admin user
docker exec -it flight-etl-pipeline-airflow-webserver-1 airflow users create \
  --username admin --password admin \
  --firstname Admin --lastname User \
  --role Admin --email admin@example.com

# 4. Open the Airflow UI
# Go to http://localhost:8080 (admin / admin)
# Enable the flight_etl DAG and trigger it
```

### Verify data is loading

```bash
docker exec -it flight-etl-pipeline-flights_db-1 psql -U flights -d flights_db \
  -c "SELECT icao24, callsign, origin_country, velocity, baro_altitude FROM flights LIMIT 10;"
```

---

## 📊 Data Schema

Table: `flights`

| Column | Type | Description |
|--------|------|-------------|
| `icao24` | TEXT | Unique aircraft identifier |
| `callsign` | TEXT | Flight callsign |
| `origin_country` | TEXT | Country of registration |
| `latitude` | FLOAT | Current latitude |
| `longitude` | FLOAT | Current longitude |
| `baro_altitude` | FLOAT | Barometric altitude (meters) |
| `velocity` | FLOAT | Ground speed (m/s) |
| `on_ground` | BOOLEAN | Whether aircraft is on ground |
| `last_contact` | TIMESTAMP | Last ADS-B signal received |
| `ingested_at` | TIMESTAMP | When the row was inserted |

Primary key: `(icao24, last_contact)` — duplicate-safe upserts.

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

Tests cover:
- Dropping flights with missing position data
- Callsign whitespace normalization
- Coordinate rounding precision

---

## 🔮 Future Improvements

- [ ] Add **dbt** for SQL-layer transformations and data modeling
- [ ] Add **Great Expectations** for data quality checks
- [ ] Connect **Metabase** or **Grafana** for a live flight dashboard
- [ ] Deploy to a cloud VM (Railway, Fly.io, or AWS EC2)
- [ ] Add alerting when pipeline fails (email or Slack)

---

## 📡 Data Source

[OpenSky Network](https://opensky-network.org/) — a non-profit providing free access to real-time and historical ADS-B flight data. No API key required for public endpoints.
