"""
🏥 IOT Hospital - Room Sensor (Virtuale)
Simula sensori ambientali: temperatura, umidità, qualità aria (CO2)

Author: El Houssine (Ednajm)
Corso di Ingegneria Informatica — Progetto IoT 2025
"""

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# Configurazione
BROKER = "localhost"
PORT = 1883
TOTAL_ROOMS = 500
UPDATE_INTERVAL = 10  # secondi (meno frequente dei pazienti)

# Parametri ambientali (come da README)
# Temperatura stanza: 20-26°C
# Umidità: 40-65%
# CO2: 400-800 ppm (allarme se > 1000 ppm)

class RoomSensor:
    def __init__(self):
        self.client = mqtt.Client()
        self.rooms = [f"Room{i}" for i in range(1, TOTAL_ROOMS + 1)]
        print(f"🌡️  Sensore Ambientale inizializzato: {TOTAL_ROOMS} stanze virtuali")
    
    def connect(self):
        """Connetti al broker MQTT"""
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()
            print(f"✅ Connesso al broker MQTT: {BROKER}:{PORT}")
            return True
        except Exception as e:
            print(f"❌ Errore connessione: {e}")
            return False
    
    def generate_environmental_data(self):
        """
        Genera dati ambientali simulati
        Con probabilità di generare valori anomali per testare allarmi
        """
        # 85% valori normali, 15% anomali
        if random.random() < 0.85:
            # Valori normali
            temperature = round(random.uniform(21.0, 25.0), 1)
            humidity = random.randint(45, 60)
            co2 = random.randint(450, 750)
        else:
            # Valori anomali (per testare allarmi)
            anomaly_type = random.choice(['temp', 'humidity', 'co2'])
            
            if anomaly_type == 'temp':
                temperature = round(random.choice([
                    random.uniform(17.0, 19.9),
                    random.uniform(26.1, 30.0)
                ]), 1)
                humidity = random.randint(45, 60)
                co2 = random.randint(450, 750)
            elif anomaly_type == 'humidity':
                temperature = round(random.uniform(21.0, 25.0), 1)
                humidity = random.choice([
                    random.randint(25, 39),
                    random.randint(66, 80)
                ])
                co2 = random.randint(450, 750)
            else:  # co2
                temperature = round(random.uniform(21.0, 25.0), 1)
                humidity = random.randint(45, 60)
                co2 = random.randint(1001, 1500)
        
        return temperature, humidity, co2
    
    def publish_data(self):
        """Pubblica dati ambientali su MQTT"""
        # Pubblica dati per un sottoinsieme di stanze per ciclo
        active_rooms = random.sample(self.rooms, min(100, len(self.rooms)))
        
        for room_id in active_rooms:
            temperature, humidity, co2 = self.generate_environmental_data()
            
            data = {
                "room_id": room_id,
                "temperature": temperature,
                "humidity": humidity,
                "co2": co2,
                "timestamp": datetime.now().isoformat()
            }
            
            topic = f"hospital/room/{room_id}"
            message = json.dumps(data)
            
            self.client.publish(topic, message)
            
            # Stampa con indicatore visivo se anomalo
            status = "⚠️" if (temperature < 20 or temperature > 26 or 
                             humidity < 40 or humidity > 65 or co2 > 1000) else "✓"
            
            print(f"{status} {room_id}: Temp={temperature:4.1f}°C, "
                  f"Humidity={humidity:2d}%, CO2={co2:4d} ppm")
    
    def start(self):
        """Avvia sensore in modalità continua"""
        print("="*70)
        print("🔄 Sensore ambientale attivo - Invio dati ogni {} secondi".format(UPDATE_INTERVAL))
        print("📊 Parametri monitorati:")
        print("   • Temperatura: 20-26°C")
        print("   • Umidità: 40-65%")
        print("   • CO2: 400-800 ppm (allarme > 1000 ppm)")
        print("="*70)
        
        try:
            while True:
                self.publish_data()
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\n⚠️  Interruzione da utente")
            self.stop()
    
    def stop(self):
        """Ferma sensore"""
        print("🛑 Arresto sensore ambientale...")
        self.client.loop_stop()
        self.client.disconnect()

def main():
    sensor = RoomSensor()
    
    if sensor.connect():
        sensor.start()
    else:
        print("❌ Impossibile avviare il sensore ambientale")

if __name__ == "__main__":
    main()
   
