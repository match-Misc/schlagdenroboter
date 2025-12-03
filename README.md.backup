# 🎮 Game Station Server - Leaderboard System# 🎮 Game Station Server - Leaderboard System



Ein Flask-basiertes Leaderboard-System für drei Spiele mit NFC-Chip-basierter Spielerverwaltung und Live-Scanner-Integration.Ein Flask-basiertes Leaderboard-System für drei verschiedene Spiele mit NFC-Chip-basierter Spielerverwaltung.



## 📋 Inhaltsverzeichnis## 📋 Inhaltsverzeichnis



- [Übersicht](#übersicht)- [Übersicht](#übersicht)

- [Installation](#installation)- [Systemarchitektur](#systemarchitektur)

- [Server starten](#server-starten)- [Installation](#installation)

- [NFC-Reader Integration](#nfc-reader-integration)- [NFC-Reader Integration](#nfc-reader-integration)

- [API-Endpunkte](#api-endpunkte)- [Server starten](#server-starten)

- [Admin-Panel](#admin-panel)- [Spiele & Endpunkte](#spiele--endpunkte)

- [Troubleshooting](#troubleshooting)- [Verwaltungssystem](#verwaltungssystem)

- [Datenspeicherung](#datenspeicherung)

---- [Testing](#testing)

- [Troubleshooting](#troubleshooting)

## 🎯 Übersicht

---

### Spiele

## 🎯 Übersicht

- 🔥 **Heißer Draht** - Zeit, Fehler, Schwierigkeitsgrad

- 🎲 **Vier Gewinnt** - Anzahl Züge, SchwierigkeitsgradDas System verwaltet Leaderboards für drei Spiele:

- 🧩 **Puzzle** - Zeit, Schwierigkeitsgrad- 🔥 **Heißer Draht** - Geschicklichkeitsspiel mit Zeit, Fehlern und Schwierigkeitsgrad

- 🎲 **Vier Gewinnt** - Strategiespiel mit Siegquote und Schwierigkeitsgrad

### Features- 🧩 **Puzzle** - Logikspiel mit Zeit und Schwierigkeitsgrad



✅ NFC-Chip Verwaltung mit Live-Scanner  ### Key Features

✅ Chip-Wiederverwendung mit Archivierung  

✅ Echtzeit-Leaderboards (Top 5 / Bottom 5)  ✅ **NFC-Chip Verwaltung** - Spieler werden über NFC-Chips identifiziert  

✅ Urkunden-Generator für Thermaldrucker  ✅ **Chip-Wiederverwendung** - Chips können nach Abschluss neu zugewiesen werden  

✅ Leaderboard-Reset mit Backup  ✅ **Daten-Archivierung** - Alte Spielerdaten bleiben in Leaderboards erhalten  

✅ Responsive Design✅ **Echtzeit-Leaderboards** - Top 5 und Letzte 5 für jedes Spiel  

✅ **Urkunden-Generator** - Thermaldrucker-optimierte Zertifikate (4"x6")  

---✅ **Responsive Design** - Optimiert für Raspberry Pi 3 B+



## 🚀 Installation---



### Voraussetzungen## 🏗️ Systemarchitektur



```bash### Projektstruktur

Python 3.8+

Flask```

```Heißer Draht Server/

├── server.py                          # Haupt-Flask-Server

### Setup├── game_data.json                     # Aktive Spielerdaten

├── nfc_mapping.json                   # NFC-ID → Spielername Zuordnung

```bash├── game_archive.json                  # Archivierte Spieler-Sessions

# 1. Repository klonen├── API_DOKUMENTATION.md               # Detaillierte API-Docs

git clone https://github.com/mxnmyr/schlagdenroboter.git├── README.md                          # Diese Datei

cd schlagdenroboter│

├── static/                            # Statische Dateien

# 2. Flask installieren│   ├── logo.png                       # Firmenlogo

pip install flask│   └── luh_logo.png                   # Universitätslogo

│

# 3. Server starten└── templates/                         # HTML-Templates

python server.py    ├── home.html                      # Hauptseite (Top 5 alle Spiele)

# oder    ├── leaderboard_heisser_draht.html # Heißer Draht Details

start_server.bat    ├── leaderboard_vier_gewinnt.html  # Vier Gewinnt Details

    ├── leaderboard_puzzle.html        # Puzzle Details

# 4. Browser öffnen    ├── admin.html                     # Verwaltungsseite

http://localhost:5000    └── certificate_multi.html         # Multi-Game Urkunde

``````



---### Datenfluss



## 🎮 Server starten```

┌─────────────┐

### Windows│ Arduino/ESP │ ──POST──> ┌──────────────┐

│  NFC Reader │           │ Flask Server │

```bash└─────────────┘           │  (server.py) │

start_server.bat                          └───────┬──────┘

```                                  │

                    ┌─────────────┼─────────────┐

### Linux/Mac                    ▼             ▼             ▼

            ┌──────────┐  ┌──────────┐  ┌──────────┐

```bash            │game_data │  │nfc_map   │  │archive   │

python3 server.py            │  .json   │  │ping.json │  │  .json   │

```            └──────────┘  └──────────┘  └──────────┘

                    │             │             │

### Zugriff                    └─────────────┼─────────────┘

                                  ▼

- **Hauptseite:** http://localhost:5000                          ┌───────────────┐

- **Admin-Panel:** http://localhost:5000/admin                          │  Leaderboards │

- **Leaderboards:**                          │  (HTML/CSS)   │

  - Heißer Draht: http://localhost:5000/leaderboard/heisser_draht                          └───────────────┘

  - Vier Gewinnt: http://localhost:5000/leaderboard/vier_gewinnt```

  - Puzzle: http://localhost:5000/leaderboard/puzzle

### Datenbank-Schema

---

#### nfc_mapping.json

## 📡 NFC-Reader Integration```json

{

### Option 1: Wemos D1 Mini V4.0 (Empfohlen)  "12345ABC": "Max Mustermann",

  "67890DEF": "Anna Schmidt"

**Vorteile:**}

- 3.3V Logik (perfekt für MFRC522)```

- WiFi integriert

- Günstiger und kompakter#### game_data.json

```json

**Pin-Mapping:**{

```  "12345ABC": {

MFRC522    →    D1 Mini V4.0    "heisser_draht": [

================================      {

SDA/SS     →    D8        "name": "Max Mustermann",

SCK        →    D5        "time": 12.5,

MOSI       →    D7        "errors": 2,

MISO       →    D6        "difficulty": "Mittel",

RST        →    D3        "timestamp": "2025-10-10T14:30:00.000000"

3.3V       →    3.3V      }

GND        →    GND    ],

```    "vier_gewinnt": [

      {

**Setup:**        "name": "Max Mustermann",

        "result": "won",

1. **Arduino IDE vorbereiten:**        "difficulty": "Schwer",

```        "timestamp": "2025-10-10T14:35:00.000000"

File → Preferences → Additional Board Manager URLs      }

→ http://arduino.esp8266.com/stable/package_esp8266com_index.json    ],

```    "puzzle": [

      {

2. **ESP8266 Board installieren:**        "name": "Max Mustermann",

```        "time": 38.75,

Tools → Board → Boards Manager → "ESP8266" installieren        "difficulty": "Schwer",

```        "timestamp": "2025-10-10T14:40:00.000000"

      }

3. **MFRC522 Library installieren:**    ]

```  }

Sketch → Include Library → Manage Libraries → "MFRC522" installieren}

``````



4. **Board konfigurieren:**#### game_archive.json

``````json

Tools → Board: "LOLIN(WEMOS) D1 mini (clone)"[

Tools → Upload Speed: 115200  {

Tools → Port: [Dein COM-Port]    "name": "Max Mustermann",

```    "heisser_draht": [...],

    "vier_gewinnt": [...],

5. **Code hochladen:**    "puzzle": [...],

- Öffne `d1mini_nfc_roboter.ino`    "archived_date": "2025-10-10T15:00:00.000000",

- Klicke auf Upload    "original_nfc_id": "12345ABC"

- Serial Monitor öffnen (9600 Baud)  }

]

**Code:** `d1mini_nfc_roboter.ino````



### Option 2: Arduino Nano---



**Pin-Mapping:**## 🚀 Installation

```

MFRC522    →    Arduino Nano### Voraussetzungen

================================

SDA/SS     →    D10- Python 3.8+

SCK        →    D13- Flask

MOSI       →    D11- Webbrowser (für Leaderboard-Anzeige)

MISO       →    D12

RST        →    D9### Setup

3.3V       →    3.3V (NICHT 5V!)

GND        →    GND```powershell

```# 1. Repository klonen oder Ordner öffnen

cd "C:\...\Heißer Draht Server"

**Code:** `arduino_nano_nfc_roboter.ino`

# 2. Abhängigkeiten installieren

### Arduino Bridgepip install flask

pip install pyserial requests  # Für Arduino NFC-Reader

Für serielle Kommunikation zwischen Arduino und Server:

# 3. Server starten

```bashpython server.py

# Python Bridge starten```

python arduino_bridge.py

# oder### Erste Schritte

start_arduino_bridge.bat

```1. **Server starten** → Server läuft auf `http://localhost:5000`

2. **Admin-Panel öffnen** → `http://localhost:5000/admin`

**Funktion:**3. **NFC-Reader einrichten** → Siehe [NFC-Reader Integration](#nfc-reader-integration)

- Auto-Erkennung des COM-Ports4. **NFC-Chips registrieren** → Mit Arduino scannen oder manuell eingeben

- Liest NFC-IDs über Serial5. **Spiele spielen** → Daten über API senden

- Sendet automatisch an `/api/nfc_scan`6. **Leaderboards anzeigen** → Automatische Updates

- Cooldown-Mechanismus (3 Sekunden)

---

### Output-Format

## 📡 NFC-Reader Integration

```

NFC_ID:A1B2C3D4E5F6Das System unterstützt **automatisches Einlesen von NFC-Tags** über Arduino!

  -> Tag erkannt: A1B2C3D4E5F6 (7 Bytes)

```### Hardware-Setup



### Unterstützte NFC-Tags**Benötigt:**

- Arduino Uno/Nano/Mega (oder ESP8266/ESP32 mit WiFi)

✅ MIFARE Classic 1K/4K  - MFRC522 RFID/NFC Reader Modul

✅ MIFARE Ultralight  - NFC-Tags (ISO14443A)

✅ NTAG213/215/216  

❌ 125 kHz Tags (EM4100)**Verkabelung:**

```

---Arduino Uno    →    MFRC522

3.3V           →    VCC (⚠️ NICHT 5V!)

## 🌐 API-EndpunkteGND            →    GND

Pin 9          →    RST

### 1. Heißer DrahtPin 10         →    SDA

Pin 11         →    MOSI

**Endpunkt:** `POST /api/heisser_draht`Pin 12         →    MISO

Pin 13         →    SCK

**Request:**```

```json

{### Software-Setup

  "nfc_id": "1A2B3C4D",

  "time": 12.5,**1. Arduino-Bibliothek installieren:**

  "errors": 2,```

  "difficulty": "Mittel"Arduino IDE → Bibliotheken verwalten → "MFRC522" installieren

}```

```

**2. Arduino-Code hochladen:**

**PowerShell:**```

```powershellDatei öffnen: arduino_nfc_reader.ino

$body = @{Upload auf Arduino

    nfc_id = "1A2B3C4D"```

    time = 12.5

    errors = 2**3. Python-Bridge starten:**

    difficulty = "Mittel"```powershell

} | ConvertTo-Json# Terminal 1: Server

python server.py

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/heisser_draht" `

    -Method POST -Body $body -ContentType "application/json"# Terminal 2: Arduino-Bridge

```python arduino_bridge.py

```

### 2. Vier Gewinnt

**4. NFC-Tags scannen:**

**Endpunkt:** `POST /api/vier_gewinnt`- NFC-Tag an Reader halten

- Bridge sendet ID automatisch an Server

**Request:**- Admin-Panel zeigt neuen Chip an

```json- Namen zuweisen → Fertig!

{

  "nfc_id": "1A2B3C4D",### Optionen

  "moves": 25,

  "difficulty": "Mittel"**Option A: Serieller Modus (Arduino Uno/Nano)**

}- Arduino per USB an Computer

```- `arduino_bridge.py` läuft auf Computer

- Sendet Daten per HTTP an Server

**PowerShell:**

```powershell**Option B: WiFi-Modus (ESP8266/ESP32)**

$body = @{- ESP verbindet sich direkt mit WiFi

    nfc_id = "1A2B3C4D"- Sendet Daten direkt an Server

    moves = 25- Kein Computer nötig!

    difficulty = "Mittel"- WiFi-Credentials in `arduino_nfc_reader.ino` eintragen

} | ConvertTo-Json

**Option C: Manuell (ohne Hardware)**

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/vier_gewinnt" `- Admin-Panel → "NFC-Chip manuell hinzufügen"

    -Method POST -Body $body -ContentType "application/json"- NFC-ID eintippen

```

### 📖 Detaillierte Anleitung

### 3. Puzzle

**→ Siehe `NFC_INTEGRATION.md` für:**

**Endpunkt:** `POST /api/puzzle`- Schritt-für-Schritt Hardware-Setup

- Verkabelungs-Diagramme

**Request:**- Troubleshooting

```json- ESP8266/ESP32 WiFi-Konfiguration

{- Arduino-Code Erklärungen

  "nfc_id": "1A2B3C4D",

  "time": 45.5,---

  "difficulty": "Mittel"

}## 🎮 Spiele & Endpunkte

```

### 1. 🔥 Heißer Draht

**PowerShell:**

```powershell**Beschreibung:** Geschicklichkeitsspiel - Draht berühren ohne Kontakt

$body = @{

    nfc_id = "1A2B3C4D"**API-Endpunkt:** `POST /api/heisser_draht`

    time = 45.5

    difficulty = "Mittel"**Datenformat:**

} | ConvertTo-Json```json

{

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/puzzle" `  "nfc_id": "12345ABC",

    -Method POST -Body $body -ContentType "application/json"  "time": 12.50,

```  "errors": 2,

  "difficulty": "Mittel"

### 4. NFC-Scan (für Live-Scanner)}

```

**Endpunkt:** `POST /api/nfc_scan`

**PowerShell Befehl:**

**Request:**```powershell

```json$body = @{

{    "nfc_id" = "12345ABC"

  "nfc_id": "1A2B3C4D"    "time" = 12.50

}    "errors" = 2

```    "difficulty" = "Mittel"

} | ConvertTo-Json

**Response:**

```jsonInvoke-RestMethod -Uri "http://127.0.0.1:5000/api/heisser_draht" `

{    -Method POST -Body $body -ContentType "application/json"

  "status": "success",```

  "exists": true,

  "has_name": true,**Bewertung:**

  "player_name": "Max Mustermann"- **Top 5:** Schnellste Zeit (weniger ist besser)

}- **Bottom 5:** Langsamste Zeit (mehr ist schlechter)

```- Angezeigt: Zeit, Fehler, Schwierigkeitsgrad, Zeitstempel



### 5. Letzter NFC-Scan abrufen---



**Endpunkt:** `GET /api/last_nfc_scan`### 2. 🎲 Vier Gewinnt



**Response:****Beschreibung:** Strategiespiel - Vier in einer Reihe

```json

{**API-Endpunkt:** `POST /api/vier_gewinnt`

  "nfc_id": "1A2B3C4D",

  "timestamp": "2025-10-21T14:30:00",**Datenformat:**

  "exists": true,```json

  "has_name": true,{

  "player_name": "Max Mustermann"  "nfc_id": "12345ABC",

}  "result": "won",

```  "difficulty": "Schwer"

}

---```



## ⚙️ Admin-Panel**Hinweis:** `result` muss `"won"` oder `"lost"` sein



### Zugriff**PowerShell Befehl:**

```powershell

http://localhost:5000/admin$body = @{

    "nfc_id" = "12345ABC"

### Funktionen    "result" = "won"

    "difficulty" = "Schwer"

#### 1. Live NFC-Scanner} | ConvertTo-Json



**Verwendung:**Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/vier_gewinnt" `

1. Klicke "Scanner starten"    -Method POST -Body $body -ContentType "application/json"

2. Halte NFC-Tag an Reader```

3. Tag wird automatisch erkannt und angezeigt

4. Namen direkt zuweisen oder ändern**Bewertung:**

5. Chip löschen möglich- **Top 5:** Höchste Siegquote (Siege/Gesamt × 100%)

- **Bottom 5:** Niedrigste Siegquote

**Polling:** Browser fragt alle 500ms den Server nach neuen Scans ab- Angezeigt: Siege, Gesamt-Spiele, Quote, Zeitstempel (letztes Spiel)



#### 2. NFC-Chip manuell hinzufügen---



- NFC-ID eingeben### 3. 🧩 Puzzle

- Optional: Spielername direkt zuweisen

- Klick auf "Hinzufügen"**Beschreibung:** Logikspiel - Puzzle in kürzester Zeit lösen



#### 3. Chip-Verwaltung**API-Endpunkt:** `POST /api/puzzle`



**Übersicht-Tabelle zeigt:****Datenformat:**

- NFC-ID```json

- Spielername{

- Spielfortschritt (🔥 🎲 🧩)  "nfc_id": "12345ABC",

- Urkunden-Status  "time": 38.75,

  "difficulty": "Schwer"

**Aktionen:**}

- ✏️ Namen ändern```

- 🔄 Neu zuweisen (archiviert alte Daten)

- 🗑️ Löschen (mit Bestätigung)**PowerShell Befehl:**

```powershell

#### 4. Namen zuweisen/ändern$body = @{

    "nfc_id" = "12345ABC"

- Namen direkt in der Tabelle eingeben    "time" = 38.75

- Klick auf "Zuweisen" oder "Ändern"    "difficulty" = "Schwer"

- Erfolgt sofort ohne Reload} | ConvertTo-Json



#### 5. Chip-NeuzuweisungInvoke-RestMethod -Uri "http://127.0.0.1:5000/api/puzzle" `

    -Method POST -Body $body -ContentType "application/json"

**Funktion:**```

- Archiviert alle Spieldaten des Spielers

- Leert den Chip für neuen Spieler**Bewertung:**

- Alte Daten bleiben in Leaderboards sichtbar- **Top 5:** Schnellste Zeit (weniger ist besser)

- **Bottom 5:** Langsamste Zeit

**Ablauf:**- Angezeigt: Zeit, Schwierigkeitsgrad, Zeitstempel

1. Klick auf "🔄 Neu zuweisen"

2. Bestätigung---

3. Chip ist leer und bereit

## ⚙️ Verwaltungssystem

#### 6. Chip löschen

### Admin-Panel

**Funktion:**

- Löscht NFC-Zuordnung**URL:** `http://localhost:5000/admin`

- Archiviert Spieldaten (wenn vorhanden)

- Mit Sicherheitsabfrage#### Funktionen:



**Ablauf:**1. **➕ Neuen NFC-Chip hinzufügen**

1. Klick auf "🗑️" oder Quick-Delete im Scanner   - NFC-ID eingeben (Pflichtfeld)

2. Bestätigung   - Spielername eingeben (optional)

3. Chip wird gelöscht   - Chip wird sofort zur Tabelle hinzugefügt



#### 7. Leaderboard zurücksetzen2. **Namen zuweisen/ändern**

   - **"➕ Zuweisen"** - Bei neuen, unbenannten Chips

**Optionen:**   - **"✏️ Ändern"** - Bei benannten Chips ohne Spiele

- 🔥 Heißer Draht einzeln   - **"🔄 Neu zuweisen (Chip zurücksetzen)"** - Bei Chips mit Spielen

- 🎲 Vier Gewinnt einzeln

- 🧩 Puzzle einzeln3. **Chip-Neuzuweisung (Wichtig!)**

- 💣 Alle Leaderboards   - Wenn ein Chip neu zugewiesen wird:

     - ✅ Alte Spieldaten werden ins **Archiv** verschoben

**Sicherheit:**     - ✅ Alter Name bleibt in **Leaderboards** sichtbar

- Automatisches Backup vor Reset     - ✅ Chip beginnt mit **leeren Spieldaten**

- Bestätigungsdialoge (2x bei "Alle")     - ✅ Neuer Spieler kann von vorne beginnen

- Backup-Datei: `leaderboard_backup_[typ]_[timestamp].json`

4. **🏅 Urkunde generieren**

**Wiederherstellung:**   - Verfügbar wenn Spieler **alle 3 Spiele** abgeschlossen hat

```python   - Optimiert für **MUNBYN Thermaldrucker** (4"x6")

import json   - Zeigt Ergebnisse aller 3 Spiele



# Backup laden#### Chip-Status Badges:

with open('leaderboard_backup_all_20251021_143022.json', 'r') as f:

    backup = json.load(f)| Badge | Bedeutung |

|-------|-----------|

# Wiederherstellen| ✓ Alle Spiele | Spieler hat alle 3 Spiele abgeschlossen |

with open('game_data.json', 'w') as f:| ⏳ In Bearbeitung | Spieler hat Namen, aber noch nicht alle Spiele |

    json.dump(backup['game_data'], f, indent=4)| ⚠ Unbenannt | Chip existiert, aber hat keinen Namen |

```

---

---

## 💾 Datenspeicherung

## 📊 Datenspeicherung

### Persistente JSON-Dateien

### Dateien

| Datei | Beschreibung | Auto-Erstellt |

#### nfc_mapping.json|-------|-------------|---------------|

```json| `nfc_mapping.json` | NFC-ID → Spielername | ✅ |

{| `game_data.json` | Aktive Spieler-Daten | ✅ |

  "1A2B3C4D": "Max Mustermann",| `game_archive.json` | Archivierte Sessions | ✅ |

  "5E6F7G8H": "Anna Schmidt"

}### Daten-Lebenszyklus

```

```

#### game_data.json1. Neuer Spieler

```json   └─> nfc_mapping.json: NFC-ID → Name

{   └─> game_data.json: Leere Spieldaten

  "1A2B3C4D": {

    "heisser_draht": [2. Spiele spielen

      {   └─> game_data.json: Spieldaten werden hinzugefügt

        "name": "Max Mustermann",   └─> Name wird in jedem Eintrag gespeichert

        "time": 12.5,

        "errors": 2,3. Chip neu zuweisen

        "difficulty": "Mittel",   └─> game_archive.json: Alte Daten archivieren

        "timestamp": "2025-10-21T14:30:00"   └─> nfc_mapping.json: Neuer Name zuweisen

      }   └─> game_data.json: Spieldaten zurücksetzen

    ],

    "vier_gewinnt": [4. Leaderboards

      {   └─> Zeigen: game_data + game_archive

        "name": "Max Mustermann",   └─> Namen bleiben erhalten!

        "moves": 25,```

        "difficulty": "Mittel",

        "timestamp": "2025-10-21T14:35:00"### Backup-Strategie

      }

    ],**Empfohlen:** Regelmäßige Backups der JSON-Dateien

    "puzzle": [

      {```powershell

        "name": "Max Mustermann",# Backup erstellen

        "time": 45.5,$date = Get-Date -Format "yyyy-MM-dd_HHmmss"

        "difficulty": "Mittel",Copy-Item "*.json" -Destination "backup_$date/"

        "timestamp": "2025-10-21T14:40:00"```

      }

    ]---

  }

}## 🧪 Testing

```

### Kompletter Test-Workflow

#### game_archive.json

```json```powershell

[# === TEST 1: Spieler erstellen ===

  {Write-Host "`n=== TEST 1: Spieler hinzufügen ==="

    "name": "Alter Spieler",$form = @{nfc_id='TEST001'; name='Max Testmann'}

    "heisser_draht": [...],Invoke-WebRequest -Uri "http://127.0.0.1:5000/admin/add_nfc" `

    "vier_gewinnt": [...],    -Method POST -Body $form -UseBasicParsing | Out-Null

    "puzzle": [...],Write-Host "✓ Max Testmann hinzugefügt"

    "archived_date": "2025-10-21T14:00:00"

  }# === TEST 2: Heißer Draht ===

]Write-Host "`n=== TEST 2: Heißer Draht ==="

```$body1 = @{

    "nfc_id" = "TEST001"

### Archivierungs-System    "time" = 12.50

    "errors" = 2

**Wann wird archiviert?**    "difficulty" = "Mittel"

- Bei Chip-Neuzuweisung} | ConvertTo-Json

- Bei Chip-Löschung (wenn Spieldaten vorhanden)

$result1 = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/heisser_draht" `

**Warum archivieren?**    -Method POST -Body $body1 -ContentType "application/json"

- Leaderboards zeigen weiterhin alte SpielerWrite-Host "✓ Heißer Draht: $($result1.status) - $($result1.player_name)"

- Daten gehen nicht verloren

- Historische Statistiken möglich# === TEST 3: Vier Gewinnt ===

Write-Host "`n=== TEST 3: Vier Gewinnt ==="

**Archivierte Daten:**$body2 = @{

- In Leaderboards als "archived" markiert    "nfc_id" = "TEST001"

- Können nicht mehr bearbeitet werden    "result" = "won"

- Bleiben dauerhaft erhalten    "difficulty" = "Schwer"

} | ConvertTo-Json

---

$result2 = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/vier_gewinnt" `

## 🔧 Troubleshooting    -Method POST -Body $body2 -ContentType "application/json"

Write-Host "✓ Vier Gewinnt: $($result2.status) - $($result2.player_name)"

### Server startet nicht

# === TEST 4: Puzzle ===

**Problem:** `ModuleNotFoundError: No module named 'flask'`Write-Host "`n=== TEST 4: Puzzle ==="

$body3 = @{

**Lösung:**    "nfc_id" = "TEST001"

```bash    "time" = 38.75

pip install flask    "difficulty" = "Schwer"

```} | ConvertTo-Json



---$result3 = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/puzzle" `

    -Method POST -Body $body3 -ContentType "application/json"

### NFC-Reader wird nicht erkanntWrite-Host "✓ Puzzle: $($result3.status) - $($result3.player_name)"



**Problem:** COM-Port nicht gefundenWrite-Host "`n=== ALLE TESTS ERFOLGREICH ==="

Write-Host "Max Testmann hat alle 3 Spiele abgeschlossen!"

**Lösung (Windows):**Write-Host "Urkunde verfügbar unter: http://127.0.0.1:5000/admin"

```powershell```

# COM-Ports anzeigen

Get-WmiObject -Query "SELECT * FROM Win32_SerialPort"### Test: Chip-Neuzuweisung



# CH340 Treiber installieren (für Clone-Boards)```powershell

# Download: http://www.wch-ic.com/downloads/CH341SER_ZIP.html# === TEST 5: Chip neu zuweisen ===

```Write-Host "`n=== TEST 5: Chip-Neuzuweisung ==="



**Lösung (Linux):**# Alten Spielstand prüfen

```bashWrite-Host "Vor Neuzuweisung:"

ls /dev/ttyUSB*Get-Content "game_data.json" -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 3

ls /dev/ttyACM*

# Chip neu zuweisen

# Berechtigungen setzen$form = @{nfc_id='TEST001'; name='Anna Neustadt'}

sudo chmod 666 /dev/ttyUSB0Invoke-WebRequest -Uri "http://127.0.0.1:5000/admin/assign_name" `

```    -Method POST -Body $form -UseBasicParsing | Out-Null

Write-Host "✓ Chip TEST001 wurde Anna Neustadt zugewiesen"

---

# Archiv prüfen

### Arduino Bridge findet keinen PortWrite-Host "`nArchiv:"

Get-Content "game_archive.json" -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 3

**Problem:** "Kein Arduino gefunden"

# Neuen Spielstand prüfen

**Ursachen:**Write-Host "`nNach Neuzuweisung:"

1. Serial Monitor der Arduino IDE ist offen → **Schließen!**Get-Content "game_data.json" -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 3

2. Falsches Board ausgewählt

3. USB-Kabel nur zum Laden (kein Datenkabel)Write-Host "`n✓ Max Testmanns Daten im Archiv"

4. Treiber fehltWrite-Host "✓ Chip bereit für Anna Neustadt"

```

**Lösung:**

```python### Schnelltests

# arduino_bridge.py anpassen - Manuellen Port setzen:

ARDUINO_PORT = "COM3"  # Oder dein Port```powershell

```# Test 1: Server läuft?

Invoke-RestMethod -Uri "http://127.0.0.1:5000/" -Method GET -TimeoutSec 5

---

# Test 2: Admin-Panel erreichbar?

### ESP8266/D1 Mini Upload fehltInvoke-RestMethod -Uri "http://127.0.0.1:5000/admin" -Method GET



**Problem:** "espcomm_sync failed"# Test 3: API antwortet?

$testBody = @{"nfc_id"="QUICK_TEST"; "time"=10.5; "errors"=0; "difficulty"="Leicht"} | ConvertTo-Json

**Lösung:**Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/heisser_draht" -Method POST -Body $testBody -ContentType "application/json"

1. Board: "LOLIN(WEMOS) D1 mini (clone)" auswählen```

2. Upload Speed: 115200

3. Flash-Button beim Upload gedrückt halten---



---## 🌐 Web-Interface



### NFC-Tags werden nicht erkannt### Seiten-Übersicht



**Checkliste:**| URL | Beschreibung |

- [ ] 3.3V (NICHT 5V!) am MFRC522|-----|-------------|

- [ ] Alle Pins korrekt verbunden (siehe Pin-Mapping)| `/` | **Hauptseite** - Top 5 aller 3 Spiele nebeneinander |

- [ ] MFRC522 Library installiert| `/leaderboard/heisser_draht` | **Heißer Draht Details** - Top 5 & Letzte 5 nebeneinander |

- [ ] Serial Monitor zeigt "Firmware Version: 0x92"| `/leaderboard/vier_gewinnt` | **Vier Gewinnt Details** - Top 5 & Letzte 5 nebeneinander |

- [ ] Tag ist ISO14443A kompatibel| `/leaderboard/puzzle` | **Puzzle Details** - Top 5 & Letzte 5 nebeneinander |

- [ ] Tag-Abstand: 1-5 cm| `/admin` | **Verwaltung** - NFC-Chips verwalten, Urkunden drucken |

| `/admin/certificate/<nfc_id>` | **Urkunde** - Multi-Game Zertifikat für Thermaldrucker |

**Test:**

```cpp### Design-Features

// Serial Monitor sollte zeigen:

// "RFID Reader: Firmware Version: 0x92 = v2.0"- 🎨 **Farbe:** #b1cb21 (Firmenfarbe Gelb-Grün)

// Falls nicht → Verkabelung prüfen!- 🏆 **Top 3:** Gold, Silber, Bronze Farbgebung

```- 📱 **Responsive:** Optimiert für Desktop & Tablet

- 🖥️ **Performance:** Optimiert für Raspberry Pi 3 B+

---- 🖨️ **Drucker:** 4"x6" Thermaldrucker-Layout



### Leaderboard zeigt keine Daten### Leaderboard-Anzeige



**Problem:** JSON-Dateien leer oder korrupt**Top 5:**

- Nummerierte Liste (1, 2, 3, 4, 5)

**Lösung:**- Gold/Silber/Bronze für Top 3

```bash- Alle Statistiken sichtbar

# 1. Server stoppen

# 2. Backup erstellen**Letzte 5:**

copy game_data.json game_data.json.backup- 📅 Kalender-Icon statt Nummern

- 🕒 Zeitstempel (Datum + Uhrzeit)

# 3. Neu initialisieren- Alle Statistiken + Timestamp

echo {} > game_data.json

echo {} > nfc_mapping.json---

echo [] > game_archive.json

## 🔧 Troubleshooting

# 4. Server neu starten

python server.py### Problem: Server startet nicht

```

```powershell

---# Lösung 1: Prüfe Python-Installation

python --version

### Live-Scanner funktioniert nicht

# Lösung 2: Flask neu installieren

**Problem:** Scanner zeigt keine Scans anpip install --upgrade flask



**Checkliste:**# Lösung 3: Port bereits belegt?

1. Arduino Bridge läuft? → `start_arduino_bridge.bat`# Ändere Port in server.py Zeile 474:

2. Serial Monitor geschlossen? → Arduino IDE schließen!# app.run(host='0.0.0.0', port=5001, debug=True)

3. COM-Port korrekt? → Ports prüfen```

4. Scanner gestartet? → "Scanner starten" klicken

5. Browser-Konsole (F12) auf Fehler prüfen### Problem: Daten werden nicht gespeichert



**Test:**```powershell

```powershell# Lösung: Prüfe Schreibrechte

# Manuellen Scan simulierenTest-Path -Path "." -PathType Container

$body = @{ nfc_id = "TEST123" } | ConvertTo-JsonGet-Acl "." | Format-List

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/nfc_scan" `

    -Method POST -Body $body -ContentType "application/json"# Falls nötig: Als Administrator ausführen

```

# Dann im Admin-Panel: Scanner starten

# TEST123 sollte erscheinen### Problem: NFC-ID wird nicht erkannt

```

```powershell

---# Prüfe JSON-Format

$testBody = @{"nfc_id"="TEST"; "time"=10.5; "errors"=0; "difficulty"="Test"} | ConvertTo-Json

### Leaderboard-Reset funktioniert nichtWrite-Host $testBody



**Problem:** Reset-Button reagiert nicht# Prüfe Server-Log

# Konsole zeigt: "Heißer Draht Daten empfangen: {...}"

**Lösung:**```

1. Browser-Konsole öffnen (F12)

2. Auf JavaScript-Fehler prüfen### Problem: Leaderboard zeigt alte Namen

3. Seite neu laden (Ctrl+F5)

4. Alternativ manuell via PowerShell:**Ursache:** Daten wurden VOR der Archiv-Implementierung gespeichert

```powershell

Invoke-WebRequest -Uri "http://127.0.0.1:5000/admin/reset_leaderboard" `**Lösung:**

    -Method POST -Body @{game_type='heisser_draht'} -UseBasicParsing```powershell

```# Option 1: Daten neu senden (empfohlen)

# Spiele erneut durchführen

---

# Option 2: JSON manuell bearbeiten

### Urkunden werden nicht generiert# Füge "name" Feld zu jedem Eintrag hinzu



**Problem:** "Spieler hat noch nicht alle Spiele abgeschlossen"# Option 3: Neustart mit leeren Daten

Remove-Item "*.json"

**Bedingungen für Urkunde:**# Server neu starten

- ✅ Heißer Draht: mindestens 1 Spiel```

- ✅ Vier Gewinnt: mindestens 1 Spiel

- ✅ Puzzle: mindestens 1 Spiel### Problem: Urkunde wird nicht angezeigt



**Prüfen:****Checkliste:**

```powershell- [ ] Spieler hat **alle 3 Spiele** abgeschlossen?

# Game-Daten anzeigen- [ ] NFC-ID korrekt in Admin-Panel?

Get-Content game_data.json | ConvertFrom-Json | ConvertTo-Json -Depth 10- [ ] Browser-Cache geleert? (Strg+F5)

```

```powershell

---# Prüfe Spieler-Status

$data = Get-Content "game_data.json" -Raw | ConvertFrom-Json

## 🎯 Workflow-Beispiel$nfcId = "TEST001"

Write-Host "Heißer Draht: $($data.$nfcId.heisser_draht.Count)"

### Kompletter AblaufWrite-Host "Vier Gewinnt: $($data.$nfcId.vier_gewinnt.Count)"

Write-Host "Puzzle: $($data.$nfcId.puzzle.Count)"

1. **Server starten:**# Alle > 0 → Urkunde verfügbar

```bash```

start_server.bat

```---



2. **Arduino Bridge starten:**## 📊 Server-Konfiguration

```bash

start_arduino_bridge.bat### Flask Debug-Modus

```

**Standard:** Debug-Modus ist aktiviert (`debug=True`)

3. **Admin-Panel öffnen:**

```**Vorteile:**

http://localhost:5000/admin- ✅ Auto-Reload bei Code-Änderungen

```- ✅ Detaillierte Fehler-Seiten

- ✅ Entwickler-Konsole

4. **Scanner starten:**

- Klick auf "Scanner starten"**Für Produktion:**

```python

5. **Spieler registrieren:**# In server.py Zeile 474 ändern:

- NFC-Tag vorhaltenapp.run(host='0.0.0.0', port=5000, debug=False)

- Name eingeben```

- "Zuweisen" klicken

### Netzwerk-Zugriff

6. **Spiel 1 - Heißer Draht:**

```powershell**Lokal:** `http://127.0.0.1:5000`  

$body = @{**Netzwerk:** `http://<RASPBERRY_PI_IP>:5000`

    nfc_id = "1A2B3C4D"

    time = 12.5```powershell

    errors = 2# IP-Adresse finden

    difficulty = "Mittel"ipconfig

} | ConvertTo-Json# Suche nach "IPv4-Adresse"

```

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/heisser_draht" `

    -Method POST -Body $body -ContentType "application/json"### Performance-Tipps

```

1. **Raspberry Pi Optimierung:**

7. **Spiel 2 - Vier Gewinnt:**   - Swap-Speicher erhöhen

```powershell   - Unnötige Services deaktivieren

$body = @{   - Lite-Version von Raspberry Pi OS verwenden

    nfc_id = "1A2B3C4D"

    moves = 252. **Browser-Optimierung:**

    difficulty = "Mittel"   - Cache aktivieren

} | ConvertTo-Json   - Hardware-Beschleunigung aktivieren

   - Chromium im Kiosk-Modus

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/vier_gewinnt" `

    -Method POST -Body $body -ContentType "application/json"3. **Datenbank-Optimierung:**

```   - Alte Archiv-Einträge periodisch löschen

   - JSON-Dateien komprimieren (optional)

8. **Spiel 3 - Puzzle:**

```powershell---

$body = @{

    nfc_id = "1A2B3C4D"## 📝 Arduino/ESP32 Integration

    time = 45.5

    difficulty = "Mittel"### Beispiel-Code (ESP32)

} | ConvertTo-Json

```cpp

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/puzzle" `#include <WiFi.h>

    -Method POST -Body $body -ContentType "application/json"#include <HTTPClient.h>

```#include <ArduinoJson.h>



9. **Leaderboard prüfen:**const char* ssid = "YOUR_WIFI_SSID";

```const char* password = "YOUR_WIFI_PASSWORD";

http://localhost:5000/const char* serverUrl = "http://192.168.1.100:5000/api/heisser_draht";

```

void sendGameData(String nfcId, float time, int errors, String difficulty) {

10. **Urkunde generieren:**  HTTPClient http;

```  http.begin(serverUrl);

http://localhost:5000/admin  http.addHeader("Content-Type", "application/json");

→ Klick auf "🏆 Urkunde" beim Spieler  

```  StaticJsonDocument<200> doc;

  doc["nfc_id"] = nfcId;

---  doc["time"] = time;

  doc["errors"] = errors;

## 📁 Projektstruktur  doc["difficulty"] = difficulty;

  

```  String jsonString;

Heißer Draht Server/  serializeJson(doc, jsonString);

├── server.py                      # Flask-Server  

├── arduino_bridge.py              # Serial-zu-HTTP Bridge  int httpResponseCode = http.POST(jsonString);

├── d1mini_nfc_roboter.ino         # NFC-Reader Code (D1 Mini)  

├── arduino_nano_nfc_roboter.ino   # NFC-Reader Code (Nano)  if (httpResponseCode > 0) {

├── arduino_nfc_reader.ino         # Legacy (mit WiFi)    Serial.print("✓ Daten gesendet: ");

├── start_server.bat               # Server-Starter (Windows)    Serial.println(httpResponseCode);

├── start_arduino_bridge.bat       # Bridge-Starter (Windows)  } else {

├── posten.py                      # Datenposting-Tool    Serial.print("❌ Fehler: ");

├── game_data.json                 # Spielerdaten    Serial.println(httpResponseCode);

├── nfc_mapping.json               # NFC-Zuordnungen  }

├── game_archive.json              # Archivierte Daten  

├── all_time_leaderboard.json      # Historische Daten  http.end();

├── README.md                      # Diese Datei}

├── static/

│   ├── logo.pngvoid setup() {

│   └── luh_logo.png  Serial.begin(115200);

└── templates/  WiFi.begin(ssid, password);

    ├── home.html  

    ├── leaderboard_heisser_draht.html  while (WiFi.status() != WL_CONNECTED) {

    ├── leaderboard_vier_gewinnt.html    delay(500);

    ├── leaderboard_puzzle.html    Serial.print(".");

    ├── leaderboard_list.html  }

    ├── all_time_leaderboard.html  Serial.println("\n✓ WiFi verbunden");

    ├── admin.html}

    ├── add_name.html

    ├── select_certificate.htmlvoid loop() {

    ├── certificate.html  // NFC-Chip lesen

    └── certificate_multi.html  String nfcId = readNFCChip();

```  

  // Spiel spielen

---  float gameTime = playGame();

  int gameErrors = countErrors();

## 🎓 Technische Details  

  // Daten senden

### Framework  sendGameData(nfcId, gameTime, gameErrors, "Mittel");

  

- **Backend:** Flask (Python)  delay(5000);

- **Frontend:** HTML, CSS, JavaScript}

- **Datenbank:** JSON-Dateien```

- **Hardware:** Arduino/ESP8266 + MFRC522

---

### Browser-Kompatibilität

## 🎨 Design-Anpassungen

✅ Chrome/Edge (empfohlen)  

✅ Firefox  ### Farben ändern

✅ Safari  

⚠️ IE11 (eingeschränkt)**Datei:** Alle `.html` Templates im `<style>` Bereich



### Performance```css

/* Hauptfarbe ändern */

- Polling-Intervall: 500msbackground: linear-gradient(135deg, #b1cb21 0%, #7a9615 100%);

- Cooldown NFC-Scan: 2-3 Sekunden/* Zu: */

- Leaderboard-Berechnung: <10msbackground: linear-gradient(135deg, #FF0000 0%, #AA0000 100%);

- Simultane Nutzer: 20+

/* Button-Farbe ändern */

### Sicherheitbackground: linear-gradient(135deg, #b1cb21 0%, #8fa619 100%);

```

- Keine Authentifizierung (lokales Netzwerk)

- Admin-Panel ohne Login### Logos ändern

- Automatische Backups bei Reset

- Archivierung verhindert Datenverlust**Dateien:**

- `static/logo.png` - Firmenlogo (rechts oben)

---- `static/luh_logo.png` - Partner-Logo (links oben)



## 📝 Lizenz**Empfohlene Größe:** 150x150px, PNG mit Transparenz



Dieses Projekt wurde für die Leibniz Universität Hannover entwickelt.### Texte anpassen



---**Titel ändern:** In `templates/home.html`:

```html

## 🎉 Viel Erfolg!<h1>🎮 Schlag den Roboter</h1>

<!-- Zu: -->

Bei Fragen oder Problemen:<h1>🎮 Ihr Titel hier</h1>

1. Troubleshooting-Abschnitt prüfen```

2. Browser-Konsole (F12) auf Fehler checken

3. Server-Logs im Terminal anschauen---

4. JSON-Dateien auf Korrektheit prüfen

## 📚 Weiterführende Links

**Server läuft:** http://localhost:5000  

**Admin-Panel:** http://localhost:5000/admin- **API-Dokumentation:** `API_DOKUMENTATION.md`

- **Flask Dokumentation:** https://flask.palletsprojects.com/

Happy Gaming! 🚀- **Jinja2 Template Engine:** https://jinja.palletsprojects.com/

- **Raspberry Pi Setup:** https://www.raspberrypi.org/documentation/

---

## 👥 Support & Kontakt

**Bei Fragen oder Problemen:**

1. ✅ Prüfe diese README
2. ✅ Prüfe `API_DOKUMENTATION.md`
3. ✅ Prüfe Server-Logs in der Konsole
4. ✅ Teste mit Beispiel-Befehlen aus dieser README

---

## 📄 Lizenz & Credits

**Entwickelt für:** Match-Event, Leibniz Universität Hannover  
**Version:** 1.0  
**Datum:** Oktober 2025  
**Framework:** Flask + Jinja2  
**Design:** Responsive CSS mit Firmenfarben

---

## 📚 Zusätzliche Dokumentation

- **[LEADERBOARD_RESET.md](LEADERBOARD_RESET.md)** - Leaderboards zurücksetzen (einzeln oder alle)
- **[NFC_INTEGRATION.md](NFC_INTEGRATION.md)** - Arduino NFC-Reader Integration
- **[LIVE_SCANNER_ANLEITUNG.md](LIVE_SCANNER_ANLEITUNG.md)** - Live NFC-Scanner Anleitung
- **[API_DOKUMENTATION.md](API_DOKUMENTATION.md)** - Vollständige API-Referenz
- **[TROUBLESHOOTING_QUICK.md](TROUBLESHOOTING_QUICK.md)** - Schnelle Problemlösungen
- **[TEST_UMBENENNEN.md](TEST_UMBENENNEN.md)** - Spieler umbenennen

---

## ✅ Quick Start Checkliste

- [ ] Python 3.8+ installiert
- [ ] Flask installiert (`pip install flask`)
- [ ] Server gestartet (`python server.py`)
- [ ] Browser geöffnet (`http://localhost:5000`)
- [ ] Admin-Panel geöffnet (`http://localhost:5000/admin`)
- [ ] Test-NFC-Chip hinzugefügt
- [ ] Test-Daten gesendet (siehe [Testing](#testing))
- [ ] Leaderboards geprüft
- [ ] Archiv-System getestet (Chip-Neuzuweisung)
- [ ] Urkunde generiert
- [ ] Reset-Funktion getestet (optional)

**🎉 Viel Erfolg mit dem Game Station Server!**
