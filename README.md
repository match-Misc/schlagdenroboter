# 🎮 Game Station Server - Leaderboard System

Ein Flask-basiertes Leaderboard-System für drei Spiele mit NFC-Chip-Verwaltung, Live-Scanner und automatischer Aktualisierung.

---

## 📋 Inhaltsverzeichnis

- [Übersicht](#-übersicht)
- [Schnellstart](#-schnellstart)
- [NFC-Integration](#-nfc-integration)
- [API-Endpunkte](#-api-endpunkte)
- [Admin-Panel](#-admin-panel)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Übersicht

### Spiele

| Spiel | Messwerte | Bewertung |
|-------|-----------|-----------|
| 🔥 **Heißer Draht** | Zeit, Fehler, Schwierigkeit | Niedrigste Zeit = Beste |
| 🎲 **Vier Gewinnt** | Anzahl Züge, Schwierigkeit | Wenigste Züge = Beste |
| 🧩 **Puzzle** | Zeit, Schwierigkeit | Kürzeste Zeit = Beste |

### Hauptfunktionen

- ✅ NFC-Chip Verwaltung - Spieler per NFC-Chip identifizieren
- ✅ Live-Scanner - Echtzeit NFC-Erkennung im Admin-Panel
- ✅ **Remote-Namenseingabe** - Namen von beliebigem PC zuweisen
- ✅ Auto-Refresh Leaderboards - Updates nur bei neuen Daten
- ✅ Netzwerk-Bridges - NFC-Scanner auf mehreren PCs

---

## ⚡ Schnellstart

```bash
# 1. Flask installieren
pip install flask

# 2. Server starten
python server.py

# 3. Browser öffnen
http://localhost:5000
```

### Mit NFC-Scanner

```bash
# Python-Pakete
pip install flask pyserial requests

# Bridge starten (auf PC mit Arduino)
python nfc_network_bridge.py

# Server starten (kann anderer PC sein)
python server.py
```

---

## 📡 NFC-Integration

### Überblick

Das System unterstützt drei Modi:

| Modus | Beschreibung |
|-------|-------------|
| **Lokal** | Arduino direkt am Server-PC |
| **Netzwerk** | Arduino an beliebigem PC + Bridge → Server |
| **WiFi** | D1 Mini sendet direkt per WiFi |

### Netzwerk-Scanner (Remote-PC)

Die `nfc_network_bridge.py` ermöglicht NFC-Scanning von **jedem PC im Netzwerk**:

```bash
python nfc_network_bridge.py
```

**Features:**
- 📡 Sendet NFC-Scans an entfernten Server
- 👤 **Interaktive Namenseingabe** - Namen direkt in der Konsole eingeben
- 🔄 Automatische COM-Port Erkennung
- 🌐 Funktioniert auf beliebigem PC im Netzwerk

**Konfiguration:**
```python
# In nfc_network_bridge.py:
SERVER_URL = "http://10.145.8.50:5000"  # Server-IP anpassen!
```

**Ablauf bei neuem Chip:**
```
📡 NFC-Tag erkannt: 1A2B3C4D
✓ Server-Antwort: success
  Status: Neuer Chip (noch kein Name)

========================================
  NEUER CHIP: 1A2B3C4D
========================================
Bitte Namen eingeben (oder Enter zum Überspringen):
  Name: Max Mustermann
✓ Name 'Max Mustermann' wurde zugewiesen!
========================================
```

### Hardware-Verkabelung

**Arduino Nano + MFRC522:**
```
MFRC522    Arduino Nano
SDA/SS  →  D10
SCK     →  D13
MOSI    →  D11
MISO    →  D12
RST     →  D9
3.3V    →  3.3V (⚠️ NICHT 5V!)
GND     →  GND
```

**D1 Mini + MFRC522:**
```
MFRC522    D1 Mini V4.0
SDA/SS  →  D8 (GPIO15)
SCK     →  D5 (GPIO14)
MOSI    →  D7 (GPIO13)
MISO    →  D6 (GPIO12)
RST     →  D3 (GPIO0)
3.3V    →  3.3V
GND     →  GND
```

---

## 🌐 API-Endpunkte

### Spieldaten senden

#### Heißer Draht
```bash
POST /api/heisser_draht
{
  "nfc_id": "1A2B3C4D",
  "time": 12.5,
  "errors": 2,
  "difficulty": "Mittel"
}
```

#### Vier Gewinnt
```bash
POST /api/vier_gewinnt
{
  "nfc_id": "1A2B3C4D",
  "moves": 25,
  "difficulty": "Schwer"
}
```

#### Puzzle
```bash
POST /api/puzzle
{
  "nfc_id": "1A2B3C4D",
  "time": 45.5,
  "difficulty": "Einfach"
}
```

### NFC-Verwaltung

#### NFC-Scan senden
```bash
POST /api/nfc_scan
{
  "nfc_id": "1A2B3C4D"
}
```

**Response:**
```json
{
  "status": "success",
  "nfc_id": "1A2B3C4D",
  "exists": true,
  "has_name": true,
  "player_name": "Max Mustermann"
}
```

#### Namen zuweisen (NEU!)
```bash
POST /api/assign_name
{
  "nfc_id": "1A2B3C4D",
  "name": "Max Mustermann"
}
```

**Response:**
```json
{
  "status": "success",
  "nfc_id": "1A2B3C4D",
  "name": "Max Mustermann",
  "message": "Name 'Max Mustermann' erfolgreich zugewiesen"
}
```

#### Letzten Scan abrufen
```bash
GET /api/last_nfc_scan
```

#### Update-Status (für Auto-Refresh)
```bash
GET /api/last_update
```

### PowerShell-Beispiele

```powershell
# Heißer Draht Daten senden
$body = @{
    nfc_id = "1A2B3C4D"
    time = 12.5
    errors = 2
    difficulty = "Mittel"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://10.145.8.50:5000/api/heisser_draht" `
    -Method POST -Body $body -ContentType "application/json"

# Namen zuweisen
$body = @{
    nfc_id = "1A2B3C4D"
    name = "Max Mustermann"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://10.145.8.50:5000/api/assign_name" `
    -Method POST -Body $body -ContentType "application/json"
```

---

## ⚙️ Admin-Panel

**URL:** `http://localhost:5000/admin`

### Funktionen

1. **📡 Live NFC-Scanner** - Echtzeit-Anzeige gescannter Tags
2. **📋 Chip-Verwaltung** - Namen ändern, löschen, neu zuweisen
3. **🔄 Chip-Neuzuweisung** - Archiviert Daten, Chip für neuen Spieler
4. **💣 Leaderboard-Reset** - Mit automatischem Backup
5. **📝 Chip manuell hinzufügen** - NFC-ID ohne Scanner eingeben

---

## 🔧 Troubleshooting

### Server nicht erreichbar von anderem PC

```powershell
# Windows Firewall-Regel
netsh advfirewall firewall add rule name="Flask Server" dir=in action=allow protocol=TCP localport=5000
```

### Kein Arduino gefunden

```bash
# Ports prüfen
python check_ports.py

# Treiber installieren (CH340)
# http://www.wch-ic.com/downloads/CH341SER_ZIP.html
```

### Namen werden nicht zugewiesen

Stelle sicher, dass:
1. Server läuft und erreichbar ist
2. Bridge die richtige SERVER_URL hat
3. Keine Firewall den Port 5000 blockiert

Test:
```powershell
# Von Remote-PC testen
Invoke-RestMethod -Uri "http://SERVER_IP:5000/api/last_update"
```

---

## 📁 Projektstruktur

```
├── server.py                    # Flask-Server
├── nfc_network_bridge.py        # Netzwerk-Bridge (mit Namenseingabe!)
├── arduino_bridge.py            # Lokale Bridge
├── check_ports.py               # COM-Port Diagnose
├── game_data.json               # Aktive Spieldaten
├── nfc_mapping.json             # NFC → Name Zuordnung
├── game_archive.json            # Archivierte Daten
├── arduino_nfc_reader/          # Arduino NFC-Code
├── d1mini_nfc_reader/           # D1 Mini NFC-Code
├── d1mini_heisser_draht/        # D1 Mini Spielcode
└── templates/                   # HTML-Templates
```

---

## 🚀 Quick Reference

| URL | Beschreibung |
|-----|--------------|
| `http://SERVER:5000/` | Homepage |
| `http://SERVER:5000/admin` | Admin-Panel |
| `http://SERVER:5000/leaderboard/heisser_draht` | Heißer Draht |
| `http://SERVER:5000/leaderboard/vier_gewinnt` | Vier Gewinnt |
| `http://SERVER:5000/leaderboard/puzzle` | Puzzle |

**GitHub:** https://github.com/match-Misc/schlagdenroboter
