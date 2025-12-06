# 🏥 IOT_hospital — Sistema di Monitoraggio Ospedaliero (Simulazione Software)

## 📌 Descrizione del Progetto

**IOT_hospital** è una simulazione software progettata per rappresentare un sistema di **monitoraggio intelligente** destinato a un ambiente ospedaliero.

L'obiettivo principale è dimostrare come tecnologie moderne come **IoT, Python, MQTT e API RESTful** possano migliorare la gestione dei pazienti e delle risorse mediche attraverso la **raccolta e l'elaborazione dei dati in tempo reale**.

---

## 🔧 Componenti e Funzionamento

Nel sistema vengono simulati diversi **sensori virtuali**, ciascuno con un ruolo specifico:

### 👨‍⚕️ Sensori di paziente

* Battito cardiaco
* Temperatura corporea
* Saturazione di ossigeno (SpO₂)

### 🌡️ Sensori ambientali

* Temperatura
* Umidità
* Qualità dell'aria

### 🏷️ Tracciamento attrezzature mediche

* Posizione
* Stato operativo

Tutti i dispositivi comunicano tramite protocollo **MQTT**, utilizzando un broker **Mosquitto** installato in locale.

Un **backend Python**:

* Riceve i dati dai sensori
* Li elabora e li analizza
* Genera **allarmi** in caso di valori anomali
* Espone un'**API RESTful** per la consultazione dei dati

Una **dashboard web** consente di visualizzare in tempo reale:

* Parametri raccolti
* Allarmi generati

---

## 📦 Moduli del Sistema

| Nome                         | Tipologia            | Descrizione                                                                                                   |
| ---------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------- |
| **PatientSensor (virtuale)** | Sensore              | Rileva in modo simulato battito cardiaco, temperatura corporea e saturazione di ossigeno (SpO₂) del paziente. |
| **RoomSensor (virtuale)**    | Sensore              | Simula temperatura, umidità e qualità dell'aria all'interno di una stanza ospedaliera.                        |
| **AssetTracker (virtuale)**  | Sensore              | Simula posizione e stato operativo delle attrezzature mediche.                                                |
| **AlertSystem**              | Attuatore (software) | Genera avvisi in caso di valori critici rilevati dai sensori.                                                 |

---

## 🚀 Tecnologie Utilizzate

* **Python 3.11+**
* **MQTT (Mosquitto broker)**
* **Flask** - Framework web
* **Paho-MQTT** - Client MQTT Python
* **Chart.js** - Grafici interattivi
* **Bootstrap 5** - Framework CSS
* **API RESTful**
* **Dashboard web realtime**
* Sensori e attuatori **virtuali**

---

## 📊 Funzionalità Principali

* ✅ Simulazione realistica dei principali parametri ospedalieri
* ✅ Comunicazione dati in tempo reale tramite MQTT
* ✅ Sistema di allarme automatico basato su soglie critiche
* ✅ Dashboard interattiva per monitoraggio live
* ✅ API REST per accedere ai dati memorizzati
* ✅ Gestione di 5000 pazienti virtuali
* ✅ Monitoraggio di 500 stanze ospedaliere
* ✅ Tracciamento di 199 asset medici

---

## 🛠️ Installazione

### Prerequisiti

* Python 3.11 o superiore
* MQTT Broker (Mosquitto)
* Git

### Passaggi di Installazione

```bash
# 1. Clona il repository
git clone https://github.com/Ednajm/iot_hospital.git
cd iot_hospital

# 2. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# 3. Installa le dipendenze
pip install flask flask-cors flask-restful paho-mqtt pandas

# 4. Installa Mosquitto MQTT Broker
sudo apt install mosquitto mosquitto-clients  # Ubuntu/Debian
# oppure
brew install mosquitto  # macOS

# 5. Avvia Mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

---

## ▶️ Avvio del Sistema

### Metodo 1: Avvio Rapido (Solo Dashboard)

```bash
# 1. Attiva l'ambiente virtuale
source venv/bin/activate

# 2. Avvia il server
python app.py

# 3. Apri il browser su http://localhost:5000
```

### Metodo 2: Avvio Completo (Tutti i componenti)

#### Terminale 1 - MQTT Broker
```bash
mosquitto -v
```

#### Terminale 2 - Dashboard Server
```bash
cd IOT_HOSPITAL
source venv/bin/activate
python app.py
```

#### Terminale 3 - Sensori Pazienti
```bash
cd IOT_HOSPITAL
source venv/bin/activate
python sensors/patient_sensor.py
```

#### Terminale 4 - Sensori Ambientali
```bash
cd IOT_HOSPITAL
source venv/bin/activate
python sensors/room_sensor.py
```

#### Terminale 5 - Tracciamento Asset
```bash
cd IOT_HOSPITAL
source venv/bin/activate
python sensors/asset_tracker.py
```

---

## 📁 Struttura del Progetto

```
IOT_HOSPITAL/
│
├── app.py                      # Server Flask principale
├── Dashboard/                  # Dashboard web completa
│   ├── dashboard_server.py     # Server alternativo con API
│   ├── static/
│   │   ├── script.js          # Logica frontend
│   │   └── style.css          # Stili grafici
│   └── templates/
│       ├── index.html         # Dashboard principale
│       ├── patients.html      # Gestione pazienti
│       ├── rooms.html         # Gestione stanze
│       ├── assets.html        # Gestione asset
│       ├── alerts.html        # Sistema allarmi
│       └── analytics.html     # Analytics
│
├── backend/                    # Backend Services
│   ├── api_server.py          # API RESTful
│   ├── database.py            # Gestione database
│   ├── data_processor.py      # Elaborazione dati
│   └── mqtt_subscriber.py     # Subscriber MQTT
│
├── sensors/                    # Sensori IoT Simulati
│   ├── patient_sensor.py      # Sensori pazienti virtuali
│   ├── room_sensor.py         # Sensori ambientali virtuali
│   └── asset_tracker.py       # Tracciamento asset virtuale
│
├── requirements.txt            # Dipendenze Python
├── .gitignore                 # File da ignorare
├── README.md                  # Documentazione completa
└── readme.md                  # Questo file
```

---

## 🌐 Accesso all'Applicazione

Una volta avviato il sistema, puoi accedere a:

* **Dashboard Principale**: http://localhost:5000
* **Gestione Pazienti**: http://localhost:5000/patients
* **Gestione Stanze**: http://localhost:5000/rooms
* **Gestione Asset**: http://localhost:5000/assets
* **Sistema Allarmi**: http://localhost:5000/alerts
* **Analytics**: http://localhost:5000/analytics
* **API Status**: http://localhost:5000/api/status

---

## 🔌 API Endpoints Disponibili

```http
GET  /api/status              # Status del sistema
GET  /api/patients            # Lista pazienti
GET  /api/rooms               # Lista stanze
GET  /api/assets              # Lista asset
GET  /api/alerts              # Allarmi attivi
GET  /api/health              # Health check
```

---

## 📈 Parametri Monitorati

### Parametri Pazienti
* **Battito Cardiaco**: 60-120 bpm (allarme se fuori range)
* **Temperatura**: 36.0-38.5°C (allarme se > 38°C)
* **SpO₂**: 90-100% (allarme se < 92%)

### Parametri Ambientali
* **Temperatura stanza**: 20-26°C
* **Umidità**: 40-65%
* **CO₂**: 400-800 ppm (allarme se > 1000 ppm)

### Tracciamento Asset
* **Posizione**: Lab, ICU, Emergency, Rooms
* **Stato**: Active, Standby, Maintenance
* **Batteria**: 20-100% (allarme se < 25%)

---

## 🚨 Sistema di Allarmi

Il sistema genera automaticamente allarmi quando:

* Parametri vitali superano soglie critiche
* Livelli ambientali diventano pericolosi
* Asset necessitano manutenzione
* Batterie sono in esaurimento

Gli allarmi sono classificati in:
* 🔴 **Critical** - Richiede attenzione immediata
* 🟡 **Warning** - Situazione da monitorare
* 🔵 **Info** - Notifica informativa

---

## 🧪 Testing del Sistema

```bash
# Test MQTT Broker
mosquitto_sub -t "hospital/#" -v

# Test pubblicazione dati
mosquitto_pub -t "hospital/test" -m "Hello IOT Hospital"

# Verifica stato servizi
sudo systemctl status mosquitto
curl http://localhost:5000/api/status
```

---

## 🔍 Troubleshooting

### Il server non si avvia
```bash
# Verifica che la porta 5000 sia libera
lsof -i :5000

# Verifica ambiente virtuale
which python  # Dovrebbe puntare a venv/bin/python
```

### MQTT non funziona
```bash
# Verifica stato Mosquitto
sudo systemctl status mosquitto

# Riavvia il servizio
sudo systemctl restart mosquitto

# Test connessione
mosquitto_sub -t "test" -v
```

### Dipendenze mancanti
```bash
# Reinstalla tutte le dipendenze
pip install -r requirements.txt

# Oppure manualmente
pip install flask flask-cors paho-mqtt pandas
```

---

## 📚 Documentazione Aggiuntiva

Per documentazione tecnica completa, consulta [README.md](README.md)

---

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. Fork del progetto
2. Crea un branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT.

---

## 👨‍💻 Autore

**El Houssine (Ednajm)**  
Corso di Ingegneria Informatica — Progetto IoT 2025  
📧 Email: 334694@studenti.unimore.it  
🔗 GitHub: [github.com/Ednajm/iot_hospital](https://github.com/Ednajm/iot_hospital)

---

## 🙏 Ringraziamenti

* Università degli Studi di Modena e Reggio Emilia
* Corso di Ingegneria Informatica
* Community open source Python
* Mosquitto MQTT Broker
* Flask Framework
* Chart.js Library

---

<div align="center">

**⭐ Se ti è piaciuto questo progetto, lascia una stella su GitHub! ⭐**

Made with ❤️ for IoT Healthcare Education

</div>
