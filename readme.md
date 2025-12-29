# Hospital IoT Monitoring System

Project for the course "Intelligent Internet of Things", part of the Bachelor's Degree in Computer Engineering at the Mantova campus of UNIMORE, during the third year of study.

## Project Idea

The application scenario is Healthcare IoT for the smart monitoring of a hospital environment.  
The system is designed to improve patient safety and healthcare quality through real-time health monitoring, environmental control, and automated medical asset tracking.

## Involved Devices

The system involves multiple types of IoT devices.  
The project is designed to support **N devices for each type**, depending on the application scenario.

During the demo, a scalable configuration can be emulated to demonstrate the correct functioning of the system:

- **N Patient Monitoring Sensors**
- **N Environmental Monitoring Stations**
- **N Medical Asset Trackers**

## Device Overview

| Name | Type | Description |
|------|------|-------------|
| **Patient Monitoring Sensor** | Sensor | Wearable device associated with a single patient, equipped with:<br>- Heart rate monitor<br>- Body temperature sensor<br>- SpO₂ (blood oxygen saturation) sensor |
| **Environmental Monitoring Station** | Sensor | Multiple environmental monitoring stations deployed in hospital rooms, equipped with:<br>- Room temperature sensor<br>- Humidity sensor<br>- CO₂ level sensor<br>- Room identification |
| **Medical Asset Tracker** | Sensor & Actuator | IoT tracker for medical equipment and devices, equipped with:<br>- Location tracking (department identification)<br>- Operational status monitoring<br>- Battery level sensor |

---

## Real-Time Patient Health Monitoring

The Data Collector continuously collects vital signs data from all **Patient Monitoring Sensors**, enabling real-time tracking of each patient's health condition.

The system monitors three critical health parameters:
- **Heart Rate**: Normal range 60-120 bpm
- **Body Temperature**: Normal range 36.0-38.0°C
- **SpO₂**: Normal range ≥90%

For each data update:
- The patient's vital signs are analyzed
- The system checks whether any parameter exceeds safety thresholds

### Health Alert Management

**Under normal conditions**, all vital signs are within acceptable ranges.

**If critical thresholds are exceeded**, the system automatically detects the health anomaly:

- **High Temperature (>38°C)**: Alert generated for potential fever
- **Low SpO₂ (<90%)**: Alert generated for oxygen deficiency
- **Abnormal Heart Rate (<50 or >120 bpm)**: Alert generated for cardiac irregularities

When critical conditions are detected:
- An alert is generated with patient ID and room location
- Medical staff is notified to take immediate action
- All alerts are logged for medical review and analysis

This functionality ensures continuous patient safety monitoring and rapid response to emergencies.

---

## Environmental Monitoring and Automatic Room Classification

The **Environmental Monitoring Stations** continuously measure environmental conditions in each hospital room:

- **Temperature** (18-30°C acceptable range)
- **Humidity** (30-70% acceptable range)
- **CO₂ levels** (<1000 ppm safe threshold)

Each station is associated with a specific room and provides comprehensive environmental data.

The Data Collector compares the measured values with predefined safety thresholds.

**If one or more thresholds are exceeded:**
- The room is automatically flagged with an environmental alert
- Room ID and the specific environmental issue are recorded
- Facility management is notified to restore optimal conditions

### Environmental Safety Thresholds

| Parameter | Safe Range | Alert Condition |
|-----------|------------|-----------------|
| Temperature | 18-30°C | Outside range |
| Humidity | 30-70% | Outside range |
| CO₂ Level | <1000 ppm | ≥1000 ppm |

This approach ensures a healthy and safe environment for patients, adapting in real-time to changing conditions within the hospital.

---

## Medical Asset Tracking and Battery Management

The system tracks approximately **200 medical assets** distributed across different hospital departments:

- **Laboratory (lab_id)**
- **Intensive Care Unit (ICU_id)**
- **Emergency Department (emergency_id)**
- **Patient Rooms (room_id)**

### Asset Status Monitoring

The Data Collector continuously monitors each medical asset's:
1. **Current Location** (department)
2. **Operational Status**:
   - **Active**: Equipment in use
   - **Standby**: Equipment available but not in use
   - **Maintenance**: Equipment under maintenance
3. **Battery Level** (20-100%)

### Battery Management and Maintenance Alerts

**Battery behavior:**
- **Battery ≥25%** → Normal operation
- **Battery <25%** → Low battery alert generated

**When battery level drops below 25%**, the system reports a critical condition:
- Asset ID and current location are logged
- Maintenance staff is alerted to recharge or replace the device
- Asset availability status is updated

**Maintenance Status Alerts:**
- When an asset enters maintenance mode, an automatic notification is generated
- The asset's location and status are tracked throughout the maintenance period
- This ensures proper inventory management and equipment availability

This functionality ensures that critical medical equipment is always operational and available when needed.

---

## System Architecture

The system is built on a distributed architecture using **MQTT protocol** for real-time data communication:

### Data Flow
1. **Sensors** publish data to MQTT broker (localhost:1883):
   - `hospital/patient/1` - Patient vital signs from all patients
   - `hospital/room/{room_id}` - Environmental data from each room
   - `hospital/asset/{asset_id}` - Asset tracking data for each equipment

2. **MQTT Subscriber** (`mqtt_subscriber.py`) - Collects data from all MQTT topics

3. **Data Processor** (`data_processor.py`) - Analyzes CSV data files against safety thresholds and generates alerts stored in `alerts.json`

4. **Dashboard Server** (`app.py`) - Flask server providing status endpoints for monitoring

### Current Implementation

**Active Sensors:**
- **Patient Sensor**: Monitors 5000 patients with heart rate (60-120 bpm), temperature (36-39°C), and SpO₂ (90-100%)
- **Room Sensor**: Monitors 500 rooms with temperature (20-30°C), humidity (30-70%), and CO₂ (300-1000 ppm)
- **Asset Tracker**: Tracks 199 medical assets across 4 departments with location, status, and battery (20-100%)

**Data Publishing Interval:** 5 seconds per sensor cycle

### Scalability

The system is designed to handle:
- **5000 patients** with real-time vital signs monitoring
- **500 rooms** with environmental sensors
- **199 medical assets** with location and status tracking

Data is processed in real-time with 5-second update intervals, ensuring immediate detection of critical conditions.

---

## How to Run

### Prerequisites
- Python 3.x
- MQTT broker (Mosquitto) running on localhost:1883
- Required packages: `paho-mqtt`, `flask`, `pandas`

### Installation
```bash
pip install paho-mqtt flask pandas
```

### Start MQTT Broker
```bash
mosquitto
```

### Run Sensors (in separate terminals)
```bash
# Terminal 1 - Patient monitoring
python sensors/patient_sensor.py

# Terminal 2 - Room environmental monitoring
python sensors/room_sensor.py

# Terminal 3 - Asset tracking
python sensors/asset_tracker.py
```

### Run Backend Services
```bash
# Terminal 4 - MQTT subscriber
python backend/mqtt_subscriber.py

# Terminal 5 - Data processor (after collecting data)
python backend/data_processor.py

# Terminal 6 - Dashboard server
python app.py
```

### Access Dashboard
Open browser: `http://localhost:5000`

## Demo Configuration

The system currently operates with:
- **5000 simulated patients** publishing vital signs data
- **500 rooms** with environmental monitors
- **199 medical assets** tracked across 4 hospital departments

All devices publish data via MQTT every 5 seconds to simulate a real hospital IoT infrastructure.

---

## Technologies Used

- **MQTT** - Message broker for IoT communication
- **Python** - Backend processing and sensor simulation
- **Flask** - REST API server
- **Pandas** - Data processing and analysis
- **JSON** - Alert storage and data interchange

---

## Project Structure

```
IOT_HOSPITAL/
├── app.py                      # Dashboard server (Flask)
│                               # Endpoints: / (status), /api/status
├── readme.md                   # Project documentation
├── sensors/
│   ├── patient_sensor.py       # Patient vital signs simulator (5000 patients)
│   │                           # Publishes to: hospital/patient/1
│   │                           # Data: patient_id, heart_rate, temperature, spo2
│   ├── room_sensor.py          # Environmental sensor simulator (500 rooms)
│   │                           # Publishes to: hospital/room/{room_id}
│   │                           # Data: room_id, temperature, humidity, co2
│   └── asset_tracker.py        # Medical asset tracker simulator (199 assets)
│                               # Publishes to: hospital/asset/{asset_id}
│                               # Data: asset_id, location, status, battery
└── backend/
    ├── mqtt_subscriber.py      # MQTT data collector (subscribes to all topics)
    ├── data_processor.py       # Alert generation and threshold analysis
    │                           # Reads: patients_data.csv, room_data.csv, asset_data.csv
    │                           # Outputs: alerts.json
    ├── database.py             # Database interface (placeholder)
    └── api_server.py           # REST API endpoints (Flask - in development)
```

---

## Future Enhancements

- Real-time dashboard with live data visualization
- Historical data analysis and trend detection
- Integration with hospital information systems (HIS)
- Machine learning for predictive health alerts
- Mobile application for medical staff notifications
- Integration with nurse call systems
