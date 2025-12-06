"""
🏥 IOT Hospital - Asset Tracker (Virtuale)
Simula tracciamento attrezzature mediche: posizione, stato, batteria

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
TOTAL_ASSETS = 199
UPDATE_INTERVAL = 15  # secondi (meno frequente, asset si muovono lentamente)

# Parametri asset (come da README)
# Posizione: Lab, ICU, Emergency, Rooms
# Stato: Active, Standby, Maintenance
# Batteria: 20-100% (allarme se < 25%)

class AssetTracker:
    def __init__(self):
        self.client = mqtt.Client()
        self.asset_ids = [f"Asset{i:03d}" for i in range(1, TOTAL_ASSETS + 1)]
        self.locations = ["Lab", "ICU", "Emergency", "Rooms"]
        self.statuses = ["Active", "Standby", "Maintenance"]
        
        # Mantieni stato di ogni asset per simulazione realistica
        self.asset_states = {}
        for asset_id in self.asset_ids:
            self.asset_states[asset_id] = {
                "location": random.choice(self.locations),
                "status": random.choice(self.statuses),
                "battery": random.randint(60, 100)
            }
        
        print(f"🏷️  Asset Tracker inizializzato: {TOTAL_ASSETS} asset virtuali")
    
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
    
    def update_asset_state(self, asset_id):
        """
        Aggiorna stato asset in modo realistico
        Gli asset cambiano posizione/stato gradualmente
        """
        state = self.asset_states[asset_id]
        
        # Batteria diminuisce lentamente (più veloce se Active)
        if state["status"] == "Active":
            state["battery"] = max(20, state["battery"] - random.randint(1, 3))
        elif state["status"] == "Standby":
            state["battery"] = max(20, state["battery"] - random.randint(0, 1))
        else:  # Maintenance - ricarica
            state["battery"] = min(100, state["battery"] + random.randint(5, 10))
        
        # Cambio location occasionale (10% probabilità)
        if random.random() < 0.1:
            state["location"] = random.choice(self.locations)
        
        # Cambio stato in base a condizioni
        if state["battery"] < 25 and state["status"] != "Maintenance":
            # Batteria bassa -> vai in manutenzione
            state["status"] = "Maintenance"
        elif state["battery"] > 80 and state["status"] == "Maintenance":
            # Batteria ricaricata -> torna operativo
            state["status"] = random.choice(["Active", "Standby"])
        elif random.random() < 0.05:  # 5% cambio casuale
            state["status"] = random.choice(self.statuses)
        
        return state
    
    def publish_data(self):
        """Pubblica dati asset su MQTT"""
        # Pubblica dati per un sottoinsieme di asset
        active_assets = random.sample(self.asset_ids, min(50, len(self.asset_ids)))
        
        for asset_id in active_assets:
            state = self.update_asset_state(asset_id)
            
            data = {
                "asset_id": asset_id,
                "location": state["location"],
                "status": state["status"],
                "battery": state["battery"],
                "timestamp": datetime.now().isoformat()
            }
            
            topic = f"hospital/asset/{asset_id}"
            message = json.dumps(data)
            
            self.client.publish(topic, message)
            
            # Stampa con indicatore visivo se batteria bassa o in manutenzione
            if state["battery"] < 25:
                status = "🔋"
            elif state["status"] == "Maintenance":
                status = "🔧"
            else:
                status = "✓"
            
            print(f"{status} {asset_id}: Location={state['location']:9s}, "
                  f"Status={state['status']:11s}, Battery={state['battery']:3d}%")
    
    def start(self):
        """Avvia tracker in modalità continua"""
        print("="*70)
        print("🔄 Asset Tracker attivo - Invio dati ogni {} secondi".format(UPDATE_INTERVAL))
        print("📊 Parametri monitorati:")
        print("   • Posizione: Lab, ICU, Emergency, Rooms")
        print("   • Stato: Active, Standby, Maintenance")
        print("   • Batteria: 20-100% (allarme < 25%)")
        print("="*70)
        
        try:
            while True:
                self.publish_data()
                time.sleep(UPDATE_INTERVAL)
        except KeyboardInterrupt:
            print("\n⚠️  Interruzione da utente")
            self.stop()
    
    def stop(self):
        """Ferma tracker"""
        print("🛑 Arresto asset tracker...")
        self.client.loop_stop()
        self.client.disconnect()

def main():
    tracker = AssetTracker()
    
    if tracker.connect():
        tracker.start()
    else:
        print("❌ Impossibile avviare l'asset tracker")

if __name__ == "__main__":
    main()

    

