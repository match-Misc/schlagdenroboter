# 📡 NFC Network Bridge

Ein Python-Programm, das NFC-Scanner auf **jedem PC im Netzwerk** ermöglicht.

## 🎯 Was macht das Programm?

- Liest NFC-Tags über Arduino/D1 Mini + MFRC522
- Sendet NFC-IDs über das Netzwerk an den Server
- Kann auf **beliebig vielen PCs** gleichzeitig laufen
- Automatische Arduino-Erkennung

## 📦 Installation

### Voraussetzungen

1. **Python 3.8+** installiert
2. **Arduino/D1 Mini** mit NFC-Reader (MFRC522)
3. **USB-Verbindung** zum PC

### Setup

1. Kopiere diese Dateien auf den PC:
   - `nfc_network_bridge.py`
   - `start_network_bridge.bat` (Windows)

2. Öffne `nfc_network_bridge.py` und passe die Server-IP an:
   ```python
   SERVER_URL = "http://10.145.8.50:5000"  # Deine Server-IP!
   ```

3. Installiere Python-Pakete (wird automatisch gemacht):
   ```bash
   pip install pyserial requests
   ```

## 🚀 Verwendung

### Windows

Doppelklick auf:
```
start_network_bridge.bat
```

### Linux/Mac

```bash
python3 nfc_network_bridge.py
```

## 📋 Arduino-Code

Verwende einen dieser Sketches auf dem Arduino/D1 Mini:

### Option 1: Arduino Nano (empfohlen für USB)
```
arduino_nano_nfc_roboter.ino
```

### Option 2: D1 Mini
```
d1mini_nfc_roboter.ino
```

**Wichtig:** Der Arduino muss NFC-IDs im Format `NFC_ID:XXXXXXXX` über Serial ausgeben!

## 🔧 Konfiguration

In `nfc_network_bridge.py`:

```python
SERVER_URL = "http://10.145.8.50:5000"  # Server-Adresse
BAUDRATE = 9600                          # Serial Baudrate
COOLDOWN_SECONDS = 3                     # Pause zwischen Scans
```

## 📊 Funktionsweise

```
┌─────────────┐       USB        ┌──────────────┐
│   Arduino   │ ────────────────> │   Client-PC  │
│   + MFRC522 │   (Serial 9600)   │   (Bridge)   │
└─────────────┘                   └──────┬───────┘
                                         │
                                         │ HTTP POST
                                         │ /api/nfc_scan
                                         ▼
                                  ┌──────────────┐
                                  │  Server-PC   │
                                  │ Flask Server │
                                  │  Port 5000   │
                                  └──────────────┘
```

## 🖥️ Mehrere Scanner gleichzeitig

Du kannst **beliebig viele** PCs mit NFC-Scannern betreiben:

1. **PC 1**: Bridge läuft → Scanner 1
2. **PC 2**: Bridge läuft → Scanner 2
3. **PC 3**: Bridge läuft → Scanner 3
4. **Server-PC**: Bridge läuft → Scanner am Server

Alle senden an denselben Server!

## ✅ Erwartete Ausgabe

```
==================================================
  NFC Scanner Bridge (Netzwerk)
==================================================
Server: http://10.145.8.50:5000
Cooldown: 3 Sekunden
==================================================

Suche nach Arduino/NFC-Reader...
  Gefunden: COM3 - USB Serial Port
✓ Arduino/ESP8266 gefunden auf COM3
✓ Verbunden mit COM3

✓ Bridge aktiv - Warte auf NFC-Tags...
  (Drücke Strg+C zum Beenden)

📡 NFC-Tag erkannt: A1B2C3D4E5F6
✓ Server-Antwort: success
  Spieler: Max Mustermann
```

## 🐛 Troubleshooting

### "Kein Arduino gefunden"
- Prüfe USB-Verbindung
- Schließe Arduino IDE Serial Monitor
- Installiere CH340-Treiber (bei Clone-Boards)

### "Keine Verbindung zum Server"
- Prüfe Server-IP in `SERVER_URL`
- Server muss laufen: `python server.py`
- Firewall-Einstellungen prüfen
- Ping zum Server: `ping 10.145.8.50`

### "Server nicht erreichbar"
Auf dem Server-PC:
```bash
# Firewall-Regel für Port 5000 hinzufügen (Windows)
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000

# Oder Server auf allen Interfaces starten
python server.py --host 0.0.0.0
```

### "Permission denied" (Linux)
```bash
sudo chmod 666 /dev/ttyUSB0
# oder User zu dialout-Gruppe hinzufügen:
sudo usermod -a -G dialout $USER
```

## 📝 Unterschied zur normalen Bridge

| Feature | `arduino_bridge.py` | `nfc_network_bridge.py` |
|---------|-------------------|------------------------|
| **Läuft auf** | Nur Server-PC | Jedem PC im Netzwerk |
| **Sendet an** | localhost:5000 | Server-IP:5000 |
| **Mehrere Scanner** | ❌ Nein | ✅ Ja |
| **Netzwerk nötig** | ❌ Nein | ✅ Ja |

## 🎯 Anwendungsfall

**Szenario:**
- Server läuft auf PC-A (IP: 10.145.8.50)
- NFC-Scanner am Spiel "Heißer Draht" auf PC-B
- NFC-Scanner am Spiel "Vier Gewinnt" auf PC-C
- NFC-Scanner am Spiel "Puzzle" auf PC-D

**Lösung:**
1. Auf PC-B, PC-C, PC-D: `nfc_network_bridge.py` starten
2. Alle verbinden sich mit Server auf PC-A
3. Jeder Scanner funktioniert unabhängig!

## 📄 Lizenz

Entwickelt für die Leibniz Universität Hannover.
