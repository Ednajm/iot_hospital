"""
🏥 IOT Hospital - Main Application Entry Point
Sistema di Monitoraggio Ospedaliero in Tempo Reale

Questo è il punto di ingresso principale che avvia il sistema completo.
Per componenti specifici, usa:
- backend/api_server.py - API RESTful Server
- backend/mqtt_subscriber.py - MQTT Data Subscriber
- sensors/patient_sensor.py - Sensori Pazienti
- sensors/room_sensor.py - Sensori Ambientali
- sensors/asset_tracker.py - Tracciamento Asset

Author: El Houssine (Ednajm)
Corso di Ingegneria Informatica — Progetto IoT 2025
"""

import sys
import os

def print_banner():
    """Stampa banner applicazione"""
    print("=" * 70)
    print("🏥 IOT HOSPITAL - Sistema di Monitoraggio Ospedaliero")
    print("=" * 70)
    print("📌 Descrizione:")
    print("   Simulazione software di sistema IoT per ambiente ospedaliero")
    print()
    print("🔧 Componenti:")
    print("   • PatientSensor (virtuale) - Battito, temperatura, SpO2")
    print("   • RoomSensor (virtuale) - Temperatura, umidità, qualità aria")
    print("   • AssetTracker (virtuale) - Posizione e stato attrezzature")
    print("   • AlertSystem - Sistema di allarmi automatici")
    print("   • API RESTful - Consultazione dati in tempo reale")
    print("   • MQTT Subscriber - Raccolta e elaborazione dati")
    print()
    print("🚀 Tecnologie:")
    print("   Python • MQTT (Mosquitto) • SQLite • Flask API")
    print("=" * 70)

def print_menu():
    """Stampa menu principale"""
    print("\n📋 MENU PRINCIPALE:")
    print("   1. Avvia API Server (backend/api_server.py)")
    print("   2. Avvia MQTT Subscriber (backend/mqtt_subscriber.py)")
    print("   3. Avvia Sensori Pazienti (sensors/patient_sensor.py)")
    print("   4. Avvia Sensori Ambientali (sensors/room_sensor.py)")
    print("   5. Avvia Asset Tracker (sensors/asset_tracker.py)")
    print("   6. Test Database (backend/database.py)")
    print("   7. Test Data Processor (backend/data_processor.py)")
    print("   0. Esci")
    print()

def run_component(module_path):
    """Esegue un componente specifico"""
    import subprocess
    
    print(f"\n🚀 Avvio {module_path}...")
    print("=" * 70)
    
    try:
        subprocess.run([sys.executable, module_path])
    except KeyboardInterrupt:
        print(f"\n⚠️  {module_path} interrotto")
    except Exception as e:
        print(f"❌ Errore avvio {module_path}: {e}")

def check_requirements():
    """Verifica dipendenze installate"""
    required_packages = ['flask', 'paho.mqtt', 'flask_cors']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("⚠️  Dipendenze mancanti:")
        for pkg in missing:
            print(f"   • {pkg}")
        print("\n💡 Installa con: pip install -r requirements.txt")
        return False
    
    return True

def check_mosquitto():
    """Verifica se Mosquitto è in esecuzione"""
    import subprocess
    
    try:
        result = subprocess.run(['pgrep', '-x', 'mosquitto'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Mosquitto MQTT Broker: Running")
            return True
        else:
            print("⚠️  Mosquitto MQTT Broker: Not running")
            print("💡 Avvia con: sudo systemctl start mosquitto")
            print("   oppure: mosquitto -v")
            return False
    except Exception:
        print("⚠️  Impossibile verificare stato Mosquitto")
        return False

def interactive_mode():
    """Modalità interattiva con menu"""
    print_banner()
    
    print("\n🔍 Verifica sistema...")
    deps_ok = check_requirements()
    mqtt_ok = check_mosquitto()
    
    if not deps_ok:
        print("\n❌ Installa le dipendenze prima di continuare")
        return
    
    if not mqtt_ok:
        response = input("\n⚠️  Mosquitto non in esecuzione. Continuare? (s/n): ")
        if response.lower() != 's':
            return
    
    while True:
        print_menu()
        choice = input("Scegli opzione (0-7): ").strip()
        
        if choice == '1':
            run_component('backend/api_server.py')
        elif choice == '2':
            run_component('backend/mqtt_subscriber.py')
        elif choice == '3':
            run_component('sensors/patient_sensor.py')
        elif choice == '4':
            run_component('sensors/room_sensor.py')
        elif choice == '5':
            run_component('sensors/asset_tracker.py')
        elif choice == '6':
            run_component('backend/database.py')
        elif choice == '7':
            run_component('backend/data_processor.py')
        elif choice == '0':
            print("\n👋 Arrivederci!")
            break
        else:
            print("❌ Opzione non valida")

def quick_start():
    """Avvio rapido con informazioni"""
    print_banner()
    
    print("\n📚 GUIDA RAPIDA:")
    print()
    print("▶️  AVVIO SISTEMA COMPLETO (5 terminali):")
    print()
    print("   Terminal 1 - MQTT Broker:")
    print("   $ mosquitto -v")
    print()
    print("   Terminal 2 - API Server:")
    print("   $ python backend/api_server.py")
    print()
    print("   Terminal 3 - MQTT Subscriber:")
    print("   $ python backend/mqtt_subscriber.py")
    print()
    print("   Terminal 4 - Sensori:")
    print("   $ python sensors/patient_sensor.py")
    print("   $ python sensors/room_sensor.py      # in un altro terminale")
    print("   $ python sensors/asset_tracker.py    # in un altro terminale")
    print()
    print("🌐 API disponibili su: http://localhost:5000/api/status")
    print()
    print("📊 ENDPOINTS API:")
    print("   GET /api/status           - System status")
    print("   GET /api/patients         - Lista pazienti")
    print("   GET /api/rooms            - Lista stanze")
    print("   GET /api/assets           - Lista asset")
    print("   GET /api/alerts/active    - Allarmi attivi")
    print("   GET /api/statistics       - Statistiche sistema")
    print()
    print("🧪 TEST COMPONENTI:")
    print("   $ python backend/database.py         # Test database")
    print("   $ python backend/data_processor.py   # Test soglie allarmi")
    print()
    print("=" * 70)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--help' or command == '-h':
            quick_start()
        elif command == '--interactive' or command == '-i':
            interactive_mode()
        elif command == '--api':
            run_component('backend/api_server.py')
        elif command == '--subscriber':
            run_component('backend/mqtt_subscriber.py')
        elif command == '--sensors':
            print("Avvia i sensori in terminali separati:")
            print("  python sensors/patient_sensor.py")
            print("  python sensors/room_sensor.py")
            print("  python sensors/asset_tracker.py")
        else:
            print(f"❌ Comando sconosciuto: {command}")
            print("💡 Usa: python app.py --help")
    else:
        # Default: mostra guida rapida
        quick_start()
        print("\n💡 Per modalità interattiva: python app.py --interactive")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruzione utente - Arrivederci!")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)

    