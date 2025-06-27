# Satellite Telemetry Analytics

## Overview
A data pipeline for processing and analyzing satellite constellation telemetry using:
- **Apache Spark** for distributed processing
- **Airflow** for workflow orchestration
- **MinIO** for object storage
(for testing and validation purposes only)

## Telemetry structure
Files are stored in JSON/Parquet format with the following schema:
```json
{
  "satellite_id": "SAT-042",
  "timestamp": "2023-10-01T12:00:00Z",
  "metrics": {
    "altitude_km": 550.2,
    "speed_km_s": 7.8,
    "battery_voltage": 16.5,
    "temperature_c": 32.7,
    "solar_flux": 1420.1
  },
  "status": "NOMINAL"
}
```

## Project Tasks

develop ETL-Pipelines

### 1. Telemetry Data Marts Preparation

**a. Satellite Metrics Summary**
- Calculate data volume per satellite
- Compute altitude statistics:
  - Average altitude
  - Maximum altitude  
  - Minimum altitude
- *Dimensions*: `satellite_id`

**b. Movement Analysis**
- Track speed change dynamics
- Aggregate in 15-minute intervals
- *Dimensions*: 
  - `satellite_id`
  - `interval_15_min`

**c. Thermal Analysis**  
- Calculate temperature change gradients (Δ°C/hour)
- Aggregate in 60-minute intervals
- *Dimensions*:
  - `satellite_id`
  - `interval_60_min`

### 2. Anomaly Detection

#### Temperature Anomalies
- **Absolute threshold**: >55°C
- **Rate of change**: >5°C per hour gradient

#### Velocity Anomalies
- Detect deviations from nominal speed range:
  - Lower bound: <7.4 km/s
  - Upper bound: >7.9 km/s

### 3. Anomaly Alerting
- send alert to telegram bot

## testing

```bash 
docker compose --env-file ../.env up --force-recreate --build -d
```

### alerts examples

🚨the temperature has exceeded the threshold value🚨
| satellite_id | interval_60_min        | temperature_c | grad  | row_number |
|--------------|------------------------|---------------|-------|------------|
| SAT-001      | 2025-10-30 23:00:00    | 58.928972     | 0.42  | 1          |
| SAT-002      | 2025-10-30 23:00:00    | 59.451953     | 0.09  | 1          |
| SAT-003      | 2025-10-30 23:00:00    | 55.210834     | -5.99 | 1          |

🚨rapid temperature change🚨
| satellite_id | interval_60_min        | temperature_c | grad  | row_number |
|--------------|------------------------|---------------|-------|------------|
| SAT-001      | 2025-10-30 13:00:00    | 62.828564     | 9.78  | 1          |
| SAT-002      | 2025-10-30 21:00:00    | 62.314217     | 6.56  | 1          |
| SAT-003      | 2025-10-30 21:00:00    | 57.235620     | -7.08 | 1          |

🚨abnormal decline or accelaration detected🚨
| satellite_id | interval                                 | avg_speed   | max_speed   | min_speed   | row_number |
|--------------|------------------------------------------|-------------|-------------|-------------|------------|
| SAT-001      | 2025-10-30 23:45:00:2025-10-31 00:00:00 | 7.707621    | 7.945778    | 7.387234    | 1          |
| SAT-002      | 2025-10-30 23:00:00:2025-10-30 23:15:00 | 7.708624    | 8.058455    | 7.481203    | 1          |
| SAT-003      | 2025-10-30 23:30:00:2025-10-30 23:45:00 | 7.699491    | 7.951850    | 7.394010    | 1          |
