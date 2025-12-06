"""
🏥 IOT Hospital - Patient Sensor (Virtuale)
Simula sensori pazienti: battito cardiaco, temperatura, SpO2

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
TOTAL_PATIENTS = 5000
UPDATE_INTERVAL = 5  # secondi

# Parametri vitali (come da README)
# Battito cardiaco: 60-120 bpm (allarme se fuori range)
# Temperatura: 36.0-38.5°C (allarme se > 38°C)
# SpO2: 90-100% (allarme se < 92%)

class PatientSensor:
    def __init__(self):
        self.client = mqtt.Client()
        self.patient_ids = list(range(1, TOTAL_PATIENTS + 1))
        print(f"👨‍⚕️  Sensore Pazienti inizializzato: {TOTAL_PATIENTS} pazienti virtuali")
    
    def connect(self):
        """Connetti al broker MQTT"""
        try:
            self.client.connect(BROKER, PORT, 60)
            print(f"✅ Connesso al broker MQTT: {BROKER}:{PORT}")
            return True
        except Exception as e:
            print(f"❌ Errore connessione: {e}")
            return False
    
    def generate_vital_signs(self):
        """
        Genera parametri vitali simulati
        Con probabilità di generare valori anomali per testare allarmi
        """
        # 90% valori normali, 10% anomali
        if random.random() < 0.9:
            # Valori normali
            heart_rate = random.randint(65, 100)
            temperature = round(random.uniform(36.2, 37.8), 1)
            spo2 = random.randint(95, 100)
        else:
            # Valori anomali (per testare allarmi)
            anomaly_type = random.choice(['heart', 'temp', 'spo2'])
            
            if anomaly_type == 'heart':
                heart_rate = random.choice([random.randint(45, 59), random.randint(121, 140)])
                temperature = round(random.uniform(36.2, 37.8), 1)
                spo2 = random.randint(95, 100)
            elif anomaly_type == 'temp':
                heart_rate = random.randint(65, 100)
                temperature = round(random.uniform(38.1, 39.5), 1)
                spo2 = random.randint(95, 100)
            else:  # spo2
                heart_rate = random.randint(65, 100)
                temperature = round(random.uniform(36.2, 37.8), 1)
                spo2 = random.randint(85, 91)
        
        return heart_rate, temperature, spo2
    
    def publish_data(self):
        """Pubblica dati pazienti su MQTT"""
        # Seleziona un sottoinsieme casuale di pazienti per questo ciclo
        active_patients = random.sample(self.patient_ids, min(50, len(self.patient_ids)))
        
        for patient_id in active_patients:
            heart_rate, temperature, spo2 = self.generate_vital_signs()
            
            data = {
                "patient_id": patient_id,
                "heart_rate": heart_rate,
                "temperature": temperature,
                "spo2": spo2,
                "timestamp": datetime.now().isoformat()
            }
            
            topic = f"hospital/patient/{patient_id}"
            message = json.dumps(data)
            
            self.client.publish(topic, message)
            
            # Stampa con indicatore visivo se anomalo
            status = "⚠️" if (heart_rate < 60 or heart_rate > 120 or 
                             temperature > 38.0 or spo2 < 92) else "✓"
            
            print(f"{status} Paziente {patient_id:4d}: HR={heart_rate:3d} bpm, "
                  f"Temp={temperature:4.1f}°C, SpO2={spo2:3d}%")
    
    def start(self):
        """Avvia sensore in modalità continua"""
        print("="*70)
        print("🔄 Sensore pazienti attivo - Invio dati ogni {} secondi".format(UPDATE_INTERVAL))
        print("📊 Parametri monitorati:")
        print("   • Battito cardiaco: 60-120 bpm")
        print("   • Temperatura: 36.0-38.5°C")
        print("   • SpO2: 90-100%")
        print("="*70)
        
        self.client.loop_start()
        
        try:
            while True:
                self.publish_data()
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\n⚠️  Interruzione da utente")
            self.stop()
    
    def stop(self):
        """Ferma sensore"""
        print("🛑 Arresto sensore pazienti...")
        self.client.loop_stop()
        self.client.disconnect()

def main():
    sensor = PatientSensor()
    
    if sensor.connect():
        sensor.start()
    else:
        print("❌ Impossibile avviare il sensore pazienti")

if __name__ == "__main__":
    main() 