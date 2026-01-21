# Hospital IoT Monitoring System

Progetto per il corso "Intelligent Internet of Things" - Ingegneria Informatica, UNIMORE Mantova.

## Descrizione

Sistema IoT per il monitoraggio ospedaliero che gestisce:
- **5000 pazienti**: parametri vitali (frequenza cardiaca, temperatura, SpO₂)
- **500 stanze**: condizioni ambientali (temperatura, umidità, CO₂)
- **199 asset medici**: posizione, stato operativo, livello batteria

## Architettura

```
sensors/              → Simulatori sensori MQTT
  ├── patient_sensor.py
  ├── room_sensor.py
  └── asset_tracker.py

backend/              → Elaborazione dati
  ├── mqtt_subscriber.py   (riceve dati MQTT)
  ├── data_processor.py    (validazione + alert)
  └── database.py          (SQLite)

api_server.py         → REST API (Flask)
data/                 → Database SQLite
- Python 3.8+
- MQTT Broker (es. Mosquitto)
pip install flask paho-mqtt
# 1. Avvia MQTT broker
mosquitto
python backend/mqtt_subscriber.py
# 3. Avvia sensori (in terminali separati)
python sensors/patient_sensor.py
python sensors/room_sensor.py
python sensors/asset_tracker.py

# 4. Avvia API server
python api_server.py
```

## API Endpoints

| Endpoint | Descrizione |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/patients` | Lista pazienti |
| `GET /api/patients/<id>` | Dati paziente |
| `GET /api/rooms` | Stato stanze |
| `GET /api/assets` | Asset tracciati |
| `GET /api/alerts` | Alert attivi |
| `GET /api/statistics` | Statistiche sistema |

## Soglie Alert

| Parametro | Range Normale | Alert |
|-----------|---------------|-------|
| Temperatura corporea | 36.0 - 38.0°C | Warning (critico >39°C) |
| SpO₂ | 90 - 100% | Warning (critico <85%) |
| Frequenza cardiaca | 50 - 120 bpm | Warning |
| Temperatura stanza | 18.0 - 28.0°C | Warning |
| Umidità | 30 - 70% | Warning |
| CO₂ | 0 - 1000 ppm | Warning (critico >1500) |
| Batteria asset | >20% | Warning (critico <10%) |
