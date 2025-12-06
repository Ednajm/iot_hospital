# iot_hospital
Il file patient_sensor.py simula il comportamento di un sensore medico IoT che monitora i parametri vitali di un paziente in un ambiente ospedaliero intelligente.
Questo script genera dati realistici e li invia periodicamente tramite il protocollo MQTT al broker Mosquitto, dove potranno essere ricevuti dal sistema di backend del progetto IOT_hospital.

⚙️ Funzionalità principali

Genera dati simulati per:

💓 Battito cardiaco (heart_rate)

🌡️ Temperatura corporea (temperature)

🫁 Saturazione di ossigeno (spo2)

Invia i dati in formato JSON tramite MQTT.
flowchart TD
    Start([INIZIO PROGRAMMA]) --> Import[Importa librerie:<br/>mqtt, time, random, json]
    Import --> CreateClient[Crea client MQTT]
    CreateClient --> Connect[Connetti a broker<br/>localhost:1883]
    Connect --> LoopStart{CICLO<br/>INFINITO}
    
    LoopStart --> GenData[GENERA DATI:<br/>patient_id = 1<br/>heart_rate = random60-120<br/>temperature = random36.0-39.0<br/>spo2 = random90-100]
    
    GenData --> ConvertJSON[Converti dati<br/>in formato JSON]
    
    ConvertJSON --> Publish[Pubblica messaggio<br/>sul topic:<br/>'hospital/patient/1']
    
    Publish --> Print[Stampa:<br/>'Messaggio inviato: '<br/>+ messaggio]
    
    Print --> Wait[Aspetta 5 secondi]
    
    Wait --> LoopStart
    
    style Start fill:#90EE90
    style LoopStart fill:#FFD700
    style GenData fill:#87CEEB
    style ConvertJSON fill:#DDA0DD
    style Publish fill:#FFA07A
    style Print fill:#F0E68C
    style Wait fill:#98FB98
