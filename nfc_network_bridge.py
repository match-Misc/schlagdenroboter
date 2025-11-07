"""
NFC Scanner Bridge - Netzwerkfähig
Sendet NFC-Scans an einen entfernten Server
Kann auf jedem PC im Netzwerk laufen
"""

import serial
import serial.tools.list_ports
import requests
import time
import json

# ========== KONFIGURATION ==========
SERVER_URL = "http://10.145.8.50:5000"  # Server-IP und Port anpassen!
BAUDRATE = 9600
COOLDOWN_SECONDS = 3
# ===================================

class NetworkNFCBridge:
    def __init__(self, server_url, baudrate=9600, cooldown=3):
        self.server_url = server_url.rstrip('/')
        self.baudrate = baudrate
        self.cooldown = cooldown
        self.last_scan_time = 0
        self.arduino_port = None
        self.ser = None
        
    def find_arduino(self):
        """Automatische Erkennung des Arduino/D1 Mini Ports"""
        ports = serial.tools.list_ports.comports()
        
        # Bekannte Arduino/ESP8266 USB-IDs
        arduino_ids = [
            (0x2341, None),  # Arduino
            (0x1A86, 0x7523), # CH340
            (0x0403, 0x6001), # FTDI
            (0x10C4, 0xEA60), # Silicon Labs
        ]
        
        print("Suche nach Arduino/NFC-Reader...")
        for port in ports:
            print(f"  Gefunden: {port.device} - {port.description}")
            
            # Prüfe bekannte Vendor/Product IDs
            for vid, pid in arduino_ids:
                if port.vid == vid and (pid is None or port.pid == pid):
                    print(f"✓ Arduino/ESP8266 gefunden auf {port.device}")
                    return port.device
        
        # Fallback: Erster COM-Port
        if ports:
            print(f"⚠ Verwende ersten verfügbaren Port: {ports[0].device}")
            return ports[0].device
        
        return None
    
    def connect(self):
        """Verbindung zum Arduino herstellen"""
        self.arduino_port = self.find_arduino()
        
        if not self.arduino_port:
            print("❌ Kein Arduino gefunden!")
            print("Bitte Arduino/D1 Mini anschließen und Programm neu starten.")
            return False
        
        try:
            self.ser = serial.Serial(self.arduino_port, self.baudrate, timeout=1)
            time.sleep(2)  # Arduino Reset abwarten
            print(f"✓ Verbunden mit {self.arduino_port}")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Verbinden: {e}")
            return False
    
    def send_to_server(self, nfc_id):
        """Sendet NFC-ID an den Server"""
        try:
            url = f"{self.server_url}/api/nfc_scan"
            data = {"nfc_id": nfc_id}
            
            response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Server-Antwort: {result.get('status', 'OK')}")
                
                # Zeige Spieler-Info an
                if result.get('has_name'):
                    print(f"  Spieler: {result.get('player_name')}")
                else:
                    print(f"  Status: Neuer Chip (noch kein Name)")
                
                return True
            else:
                print(f"⚠ Server-Fehler: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Keine Verbindung zum Server: {self.server_url}")
            print("   Prüfe Server-IP und stelle sicher, dass der Server läuft!")
            return False
        except Exception as e:
            print(f"❌ Fehler: {e}")
            return False
    
    def process_nfc_data(self, line):
        """Verarbeitet NFC-Daten vom Arduino"""
        line = line.strip()
        
        # NFC-ID Format: "NFC_ID:XXXXXXXX"
        if line.startswith("NFC_ID:"):
            nfc_id = line.replace("NFC_ID:", "").strip()
            
            # Cooldown prüfen
            current_time = time.time()
            if current_time - self.last_scan_time < self.cooldown:
                return
            
            self.last_scan_time = current_time
            
            print(f"\n📡 NFC-Tag erkannt: {nfc_id}")
            self.send_to_server(nfc_id)
        else:
            # Debug-Ausgaben vom Arduino
            if line:
                print(f"  Arduino: {line}")
    
    def run(self):
        """Hauptschleife"""
        print("\n" + "="*50)
        print("  NFC Scanner Bridge (Netzwerk)")
        print("="*50)
        print(f"Server: {self.server_url}")
        print(f"Cooldown: {self.cooldown} Sekunden")
        print("="*50 + "\n")
        
        if not self.connect():
            return
        
        print("\n✓ Bridge aktiv - Warte auf NFC-Tags...")
        print("  (Drücke Strg+C zum Beenden)\n")
        
        try:
            while True:
                if self.ser.in_waiting > 0:
                    try:
                        line = self.ser.readline().decode('utf-8', errors='ignore')
                        self.process_nfc_data(line)
                    except UnicodeDecodeError:
                        pass
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n⏹ Bridge gestoppt")
        except Exception as e:
            print(f"\n❌ Fehler: {e}")
        finally:
            if self.ser:
                self.ser.close()
                print("✓ Verbindung geschlossen")

def test_server_connection(server_url):
    """Testet die Verbindung zum Server"""
    print(f"Teste Verbindung zu {server_url}...")
    try:
        response = requests.get(f"{server_url}/", timeout=3)
        if response.status_code == 200:
            print("✓ Server erreichbar!\n")
            return True
        else:
            print(f"⚠ Server antwortet mit Status {response.status_code}\n")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Server nicht erreichbar!")
        print(f"   Bitte prüfen:")
        print(f"   1. Server läuft auf {server_url}")
        print(f"   2. IP-Adresse korrekt")
        print(f"   3. Firewall-Einstellungen\n")
        return False
    except Exception as e:
        print(f"❌ Fehler beim Testen: {e}\n")
        return False

if __name__ == "__main__":
    # Server-Verbindung testen
    if not test_server_connection(SERVER_URL):
        print("Möchtest du trotzdem fortfahren? (j/n): ", end="")
        choice = input().lower()
        if choice != 'j':
            print("Programm beendet.")
            exit(1)
    
    # Bridge starten
    bridge = NetworkNFCBridge(SERVER_URL, BAUDRATE, COOLDOWN_SECONDS)
    bridge.run()
