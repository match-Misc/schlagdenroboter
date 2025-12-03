

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Datenbank-Dateien
NFC_MAPPING_FILE = "nfc_mapping.json"
GAME_DATA_FILE = "game_data.json"
ARCHIVE_FILE = "game_archive.json"

# NFC-Mapping: {nfc_id: player_name}
nfc_mapping = {}

# Spieldaten: {nfc_id: {heisser_draht: [], vier_gewinnt: [], puzzle: []}}
game_data = {}

# Archivierte Spieldaten: [{name, heisser_draht: [], vier_gewinnt: [], puzzle: [], archived_date}]
game_archive = []

# Letzter gescannter NFC-Chip (für Live-Scanner im Admin-Panel)
last_scanned_nfc = {
    "nfc_id": None,
    "timestamp": None,
    "exists": False,
    "has_name": False,
    "player_name": None
}

# Timestamp der letzten Datenänderung
last_data_update = datetime.now().isoformat()

# Laden der gespeicherten Daten
def load_data():
    global nfc_mapping, game_data, game_archive
    
    if os.path.exists(NFC_MAPPING_FILE):
        with open(NFC_MAPPING_FILE, "r", encoding="utf-8") as file:
            nfc_mapping = json.load(file)
    else:
        nfc_mapping = {}
    
    if os.path.exists(GAME_DATA_FILE):
        with open(GAME_DATA_FILE, "r", encoding="utf-8") as file:
            game_data = json.load(file)
    else:
        game_data = {}
    
    if os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as file:
            game_archive = json.load(file)
    else:
        game_archive = []

# Speichern der Daten
def save_nfc_mapping():
    with open(NFC_MAPPING_FILE, "w", encoding="utf-8") as file:
        json.dump(nfc_mapping, file, indent=4, ensure_ascii=False)

def save_game_data():
    global last_data_update
    with open(GAME_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(game_data, file, indent=4, ensure_ascii=False)
    last_data_update = datetime.now().isoformat()

def save_archive():
    global last_data_update
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as file:
        json.dump(game_archive, file, indent=4, ensure_ascii=False)
    last_data_update = datetime.now().isoformat()

# Initialisierung
load_data()

# Hilfsfunktion: NFC-ID zu Name
def get_player_name(nfc_id):
    return nfc_mapping.get(nfc_id, f"NFC-{nfc_id}")

# Hilfsfunktion: Spieldaten für NFC-ID initialisieren
def init_player_data(nfc_id):
    if nfc_id not in game_data:
        game_data[nfc_id] = {
            "heisser_draht": [],
            "vier_gewinnt": [],
            "puzzle": []
        }

# Hilfsfunktion: Prüfen ob Spieler alle Spiele abgeschlossen hat
def has_completed_all_games(nfc_id):
    if nfc_id not in game_data:
        return False
    data = game_data[nfc_id]
    return (len(data.get("heisser_draht", [])) > 0 and 
            len(data.get("vier_gewinnt", [])) > 0 and 
            len(data.get("puzzle", [])) > 0)

# Hauptseite - Gesamt-Leaderboard mit Top 5 aller Spiele
@app.route('/')
def home():
    # Top 5 für jedes Spiel
    heisser_draht_top5 = get_top5_heisser_draht()
    vier_gewinnt_top5 = get_top5_vier_gewinnt()
    puzzle_top5 = get_top5_puzzle()
    
    return render_template('home.html', 
                          heisser_draht=heisser_draht_top5,
                          vier_gewinnt=vier_gewinnt_top5,
                          puzzle=puzzle_top5)

# Leaderboard für Heißer Draht
@app.route('/leaderboard/heisser_draht')
def leaderboard_heisser_draht():
    top5 = get_top5_heisser_draht()
    bottom5 = get_bottom5_heisser_draht()
    return render_template('leaderboard_heisser_draht.html', top5=top5, bottom5=bottom5)

# Leaderboard für Vier Gewinnt
@app.route('/leaderboard/vier_gewinnt')
def leaderboard_vier_gewinnt():
    top5 = get_top5_vier_gewinnt()
    bottom5 = get_bottom5_vier_gewinnt()
    return render_template('leaderboard_vier_gewinnt.html', top5=top5, bottom5=bottom5)

# Leaderboard für Puzzle
@app.route('/leaderboard/puzzle')
def leaderboard_puzzle():
    top5 = get_top5_puzzle()
    bottom5 = get_bottom5_puzzle()
    return render_template('leaderboard_puzzle.html', top5=top5, bottom5=bottom5)

# Hilfsfunktionen für Top 5 / Bottom 5
def get_top5_heisser_draht():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        for entry in data.get("heisser_draht", []):
            all_entries.append({
                "name": entry.get("name", get_player_name(nfc_id)),
                "nfc_id": nfc_id,
                "time": entry["time"],
                "errors": entry["errors"],
                "difficulty": entry["difficulty"],
                "timestamp": entry["timestamp"]
            })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        for entry in archive_entry.get("heisser_draht", []):
            all_entries.append({
                "name": entry.get("name", archive_entry.get("name", "Unbekannt")),
                "nfc_id": "archived",
                "time": entry["time"],
                "errors": entry["errors"],
                "difficulty": entry["difficulty"],
                "timestamp": entry["timestamp"]
            })
    all_entries.sort(key=lambda x: x["time"])
    return all_entries[:5]

def get_bottom5_heisser_draht():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        for entry in data.get("heisser_draht", []):
            all_entries.append({
                "name": entry.get("name", get_player_name(nfc_id)),
                "nfc_id": nfc_id,
                "time": entry["time"],
                "errors": entry["errors"],
                "difficulty": entry["difficulty"],
                "timestamp": entry["timestamp"]
            })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        for entry in archive_entry.get("heisser_draht", []):
            all_entries.append({
                "name": entry.get("name", archive_entry.get("name", "Unbekannt")),
                "nfc_id": "archived",
                "time": entry["time"],
                "errors": entry["errors"],
                "difficulty": entry["difficulty"],
                "timestamp": entry["timestamp"]
            })
    # Sortiere nach Timestamp absteigend (neueste zuerst)
    all_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return all_entries[:5]

def get_top5_vier_gewinnt():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        vier_gewinnt_games = data.get("vier_gewinnt", [])
        if len(vier_gewinnt_games) > 0:
            # Filtere nur Spiele mit "moves" (neue Daten)
            games_with_moves = [g for g in vier_gewinnt_games if "moves" in g]
            if len(games_with_moves) == 0:
                continue  # Überspringe alte Daten ohne moves
            
            last_name = games_with_moves[-1].get("name", get_player_name(nfc_id))
            total_moves = sum(e.get("moves", 0) for e in games_with_moves)
            game_count = len(games_with_moves)
            avg_moves = total_moves / game_count if game_count > 0 else 999
            best_moves = min(e.get("moves", 999) for e in games_with_moves)
            
            all_entries.append({
                "name": last_name,
                "nfc_id": nfc_id,
                "avg_moves": avg_moves,
                "best_moves": best_moves,
                "total": game_count,
                "games": games_with_moves
            })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        vier_gewinnt_games = archive_entry.get("vier_gewinnt", [])
        if len(vier_gewinnt_games) > 0:
            # Filtere nur Spiele mit "moves"
            games_with_moves = [g for g in vier_gewinnt_games if "moves" in g]
            if len(games_with_moves) == 0:
                continue  # Überspringe alte Daten ohne moves
            
            last_name = games_with_moves[-1].get("name", archive_entry.get("name", "Unbekannt"))
            total_moves = sum(e.get("moves", 0) for e in games_with_moves)
            game_count = len(games_with_moves)
            avg_moves = total_moves / game_count if game_count > 0 else 999
            best_moves = min(e.get("moves", 999) for e in games_with_moves)
            
            all_entries.append({
                "name": last_name,
                "nfc_id": "archived",
                "avg_moves": avg_moves,
                "best_moves": best_moves,
                "total": game_count,
                "games": games_with_moves
            })
    # Sortiere nach besten Zügen (niedrigste zuerst), dann nach Durchschnitt
    all_entries.sort(key=lambda x: (x["best_moves"], x["avg_moves"]))
    return all_entries[:5]

def get_bottom5_vier_gewinnt():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        vier_gewinnt_games = data.get("vier_gewinnt", [])
        for game in vier_gewinnt_games:
            # Nur Spiele mit "moves"
            if "moves" in game:
                all_entries.append({
                    "name": game.get("name", get_player_name(nfc_id)),
                    "nfc_id": nfc_id,
                    "moves": game["moves"],
                    "difficulty": game.get("difficulty", "Unbekannt"),
                    "timestamp": game["timestamp"]
                })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        vier_gewinnt_games = archive_entry.get("vier_gewinnt", [])
        for game in vier_gewinnt_games:
            if "moves" in game:
                all_entries.append({
                    "name": game.get("name", archive_entry.get("name", "Unbekannt")),
                    "nfc_id": "archived",
                    "moves": game["moves"],
                    "difficulty": game.get("difficulty", "Unbekannt"),
                    "timestamp": game["timestamp"]
                })
    # Sortiere nach Timestamp absteigend (neueste zuerst)
    all_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return all_entries[:5]

def get_top5_puzzle():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        for entry in data.get("puzzle", []):
            all_entries.append({
                "name": entry.get("name", get_player_name(nfc_id)),
                "nfc_id": nfc_id,
                "time": entry["time"],
                "difficulty": entry.get("difficulty", "unknown"),
                "timestamp": entry["timestamp"]
            })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        for entry in archive_entry.get("puzzle", []):
            all_entries.append({
                "name": entry.get("name", archive_entry.get("name", "Unbekannt")),
                "nfc_id": "archived",
                "time": entry["time"],
                "difficulty": entry.get("difficulty", "unknown"),
                "timestamp": entry["timestamp"]
            })
    all_entries.sort(key=lambda x: x["time"])
    return all_entries[:5]

def get_bottom5_puzzle():
    all_entries = []
    # Aktive Spieldaten
    for nfc_id, data in game_data.items():
        for entry in data.get("puzzle", []):
            all_entries.append({
                "name": entry.get("name", get_player_name(nfc_id)),
                "nfc_id": nfc_id,
                "time": entry["time"],
                "difficulty": entry.get("difficulty", "unknown"),
                "timestamp": entry["timestamp"]
            })
    # Archivierte Spieldaten
    for archive_entry in game_archive:
        for entry in archive_entry.get("puzzle", []):
            all_entries.append({
                "name": entry.get("name", archive_entry.get("name", "Unbekannt")),
                "nfc_id": "archived",
                "time": entry["time"],
                "difficulty": entry.get("difficulty", "unknown"),
                "timestamp": entry["timestamp"]
            })
    # Sortiere nach Timestamp absteigend (neueste zuerst)
    all_entries.sort(key=lambda x: x["timestamp"], reverse=True)
    return all_entries[:5]

# API-Endpunkt: Heißer Draht Daten empfangen
@app.route('/api/heisser_draht', methods=['POST'])
def receive_heisser_draht():
    data = request.json
    print("Heißer Draht Daten empfangen:", data)
    
    if not data or 'nfc_id' not in data or 'time' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    
    nfc_id = str(data['nfc_id'])
    init_player_data(nfc_id)
    
    entry = {
        "name": get_player_name(nfc_id),  # Name direkt speichern
        "time": data['time'],
        "errors": data.get('errors', 0),
        "difficulty": data.get('difficulty', 'unknown'),
        "timestamp": datetime.now().isoformat()
    }
    
    game_data[nfc_id]["heisser_draht"].append(entry)
    save_game_data()
    
    return jsonify({"status": "success", "player_name": get_player_name(nfc_id)})

# API-Endpunkt: Vier Gewinnt Daten empfangen
@app.route('/api/vier_gewinnt', methods=['POST'])
def receive_vier_gewinnt():
    data = request.json
    print("Vier Gewinnt Daten empfangen:", data)
    
    if not data or 'nfc_id' not in data or 'moves' not in data:
        return jsonify({"status": "error", "message": "Invalid data - nfc_id and moves required"}), 400
    
    nfc_id = str(data['nfc_id'])
    init_player_data(nfc_id)
    
    entry = {
        "name": get_player_name(nfc_id),  # Name direkt speichern
        "moves": int(data['moves']),  # Anzahl der Züge
        "difficulty": data.get('difficulty', 'Mittel'),
        "timestamp": datetime.now().isoformat()
    }
    
    game_data[nfc_id]["vier_gewinnt"].append(entry)
    save_game_data()
    
    return jsonify({"status": "success", "player_name": get_player_name(nfc_id), "moves": entry['moves']})

# API-Endpunkt: Puzzle Daten empfangen
@app.route('/api/puzzle', methods=['POST'])
def receive_puzzle():
    data = request.json
    print("Puzzle Daten empfangen:", data)
    
    if not data or 'nfc_id' not in data or 'time' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
    
    nfc_id = str(data['nfc_id'])
    init_player_data(nfc_id)
    
    entry = {
        "name": get_player_name(nfc_id),  # Name direkt speichern
        "time": data['time'],
        "difficulty": data.get('difficulty', 'unknown'),
        "timestamp": datetime.now().isoformat()
    }
    
    game_data[nfc_id]["puzzle"].append(entry)
    save_game_data()
    
    return jsonify({"status": "success", "player_name": get_player_name(nfc_id)})

# Verwaltungsseite
@app.route('/admin')
def admin():
    # Liste aller NFC-IDs mit Status
    nfc_list = []
    for nfc_id in set(list(nfc_mapping.keys()) + list(game_data.keys())):
        nfc_list.append({
            "nfc_id": nfc_id,
            "name": nfc_mapping.get(nfc_id, ""),
            "has_name": nfc_id in nfc_mapping,
            "completed_all": has_completed_all_games(nfc_id),
            "games_played": {
                "heisser_draht": len(game_data.get(nfc_id, {}).get("heisser_draht", [])),
                "vier_gewinnt": len(game_data.get(nfc_id, {}).get("vier_gewinnt", [])),
                "puzzle": len(game_data.get(nfc_id, {}).get("puzzle", []))
            }
        })
    nfc_list.sort(key=lambda x: x["nfc_id"])
    
    return render_template('admin.html', nfc_list=nfc_list)

# NFC-Namen zuweisen/ändern
@app.route('/admin/assign_name', methods=['POST'])
def assign_name():
    nfc_id = str(request.form.get('nfc_id'))
    name = request.form.get('name', '').strip()
    
    if not nfc_id or not name:
        return redirect(url_for('admin'))
    
    # Wenn NFC-ID bereits einen Namen hat und Spiele gespielt wurden
    if nfc_id in nfc_mapping and nfc_id in game_data:
        has_games = (len(game_data[nfc_id].get("heisser_draht", [])) > 0 or 
                    len(game_data[nfc_id].get("vier_gewinnt", [])) > 0 or 
                    len(game_data[nfc_id].get("puzzle", [])) > 0)
        
        if has_games:
            # Chip-Neuzuweisung: Archiviere alte Daten, dann Chip zurücksetzen
            old_name = nfc_mapping[nfc_id]
            archive_entry = {
                "name": old_name,
                "heisser_draht": game_data[nfc_id].get("heisser_draht", []),
                "vier_gewinnt": game_data[nfc_id].get("vier_gewinnt", []),
                "puzzle": game_data[nfc_id].get("puzzle", []),
                "archived_date": datetime.now().isoformat(),
                "original_nfc_id": nfc_id
            }
            game_archive.append(archive_entry)
            save_archive()
            
            # Neuen Namen zuweisen und Chip zurücksetzen
            nfc_mapping[nfc_id] = name
            game_data[nfc_id] = {
                "heisser_draht": [],
                "vier_gewinnt": [],
                "puzzle": []
            }
        else:
            # Nur Namensänderung ohne Spiele
            nfc_mapping[nfc_id] = name
            init_player_data(nfc_id)
    else:
        # Erstmalige Zuweisung
        nfc_mapping[nfc_id] = name
        init_player_data(nfc_id)
    
    save_nfc_mapping()
    save_game_data()
    
    return redirect(url_for('admin'))

# NFC-Chip löschen
@app.route('/admin/delete_nfc', methods=['POST'])
def delete_nfc():
    nfc_id = str(request.form.get('nfc_id', '')).strip()
    
    if not nfc_id:
        return redirect(url_for('admin'))
    
    # Prüfe ob Chip Spieldaten hat
    has_games = False
    if nfc_id in game_data:
        has_games = (
            len(game_data[nfc_id].get("heisser_draht", [])) > 0 or
            len(game_data[nfc_id].get("vier_gewinnt", [])) > 0 or
            len(game_data[nfc_id].get("puzzle", [])) > 0
        )
    
    # Wenn Spiele vorhanden, erst archivieren
    if has_games:
        player_name = nfc_mapping.get(nfc_id, "Unbekannt")
        archive_entry = {
            "name": player_name,
            "heisser_draht": game_data[nfc_id]["heisser_draht"],
            "vier_gewinnt": game_data[nfc_id]["vier_gewinnt"],
            "puzzle": game_data[nfc_id]["puzzle"],
            "archived_date": datetime.now().isoformat(),
            "original_nfc_id": nfc_id,
            "reason": "Chip gelöscht"
        }
        game_archive.append(archive_entry)
        save_archive()
    
    # Entferne Chip aus allen Datenstrukturen
    if nfc_id in nfc_mapping:
        del nfc_mapping[nfc_id]
    
    if nfc_id in game_data:
        del game_data[nfc_id]
    
    save_nfc_mapping()
    save_game_data()
    
    return redirect(url_for('admin'))

# Neuen NFC-Chip manuell hinzufügen
@app.route('/admin/add_nfc', methods=['POST'])
def add_nfc():
    nfc_id = str(request.form.get('nfc_id', '')).strip()
    name = request.form.get('name', '').strip()
    
    if not nfc_id:
        return redirect(url_for('admin'))
    
    # NFC-ID initialisieren
    init_player_data(nfc_id)
    
    # Wenn Name angegeben, direkt zuweisen
    if name:
        nfc_mapping[nfc_id] = name
        save_nfc_mapping()
    
    save_game_data()
    
    return redirect(url_for('admin'))

# API: NFC-Scan vom Arduino/ESP empfangen
@app.route('/api/nfc_scan', methods=['POST'])
def nfc_scan():
    global last_scanned_nfc
    
    data = request.get_json()
    nfc_id = str(data.get('nfc_id', '')).strip()
    
    if not nfc_id:
        return jsonify({"status": "error", "message": "Keine NFC-ID empfangen"}), 400
    
    print(f"NFC-Scan empfangen: {nfc_id}")
    
    # Prüfen ob Chip bereits existiert
    chip_exists = nfc_id in game_data
    chip_has_name = nfc_id in nfc_mapping
    
    # Wenn neu, initialisieren
    if not chip_exists:
        init_player_data(nfc_id)
        save_game_data()
    
    # Response mit Chip-Status
    response = {
        "status": "success",
        "nfc_id": nfc_id,
        "exists": chip_exists,
        "has_name": chip_has_name,
        "player_name": nfc_mapping.get(nfc_id, "Unbenannt")
    }
    
    # Speichere für Live-Scanner im Admin-Panel
    last_scanned_nfc = {
        "nfc_id": nfc_id,
        "timestamp": datetime.now().isoformat(),
        "exists": chip_exists,
        "has_name": chip_has_name,
        "player_name": nfc_mapping.get(nfc_id, "Unbenannt")
    }
    
    return jsonify(response)

# API: Letzten NFC-Scan abrufen (für Live-Scanner)
@app.route('/api/last_nfc_scan', methods=['GET'])
def get_last_nfc_scan():
    return jsonify(last_scanned_nfc)

# API: Chip-Details abrufen (für Live-Scanner)
@app.route('/api/chip_details/<nfc_id>', methods=['GET'])
def get_chip_details(nfc_id):
    nfc_id = str(nfc_id).strip()
    
    if nfc_id not in game_data:
        return jsonify({
            "exists": False,
            "has_name": False,
            "player_name": None,
            "games": {"heisser_draht": 0, "vier_gewinnt": 0, "puzzle": 0}
        })
    
    return jsonify({
        "exists": True,
        "has_name": nfc_id in nfc_mapping,
        "player_name": nfc_mapping.get(nfc_id, None),
        "games": {
            "heisser_draht": len(game_data[nfc_id].get("heisser_draht", [])),
            "vier_gewinnt": len(game_data[nfc_id].get("vier_gewinnt", [])),
            "puzzle": len(game_data[nfc_id].get("puzzle", []))
        }
    })

# API: Namen über Netzwerk zuweisen (für Remote-Bridges)
@app.route('/api/assign_name', methods=['POST'])
def api_assign_name():
    data = request.get_json()
    nfc_id = str(data.get('nfc_id', '')).strip()
    name = str(data.get('name', '')).strip()
    
    if not nfc_id or not name:
        return jsonify({"status": "error", "message": "NFC-ID und Name erforderlich"}), 400
    
    print(f"Remote-Namenzuweisung: {nfc_id} → {name}")
    
    # Prüfe ob Chip bereits existiert mit Spielen
    if nfc_id in nfc_mapping and nfc_id in game_data:
        has_games = (
            len(game_data[nfc_id].get("heisser_draht", [])) > 0 or
            len(game_data[nfc_id].get("vier_gewinnt", [])) > 0 or
            len(game_data[nfc_id].get("puzzle", [])) > 0
        )
        
        if has_games:
            # Archiviere alte Daten
            old_name = nfc_mapping[nfc_id]
            archive_entry = {
                "name": old_name,
                "heisser_draht": game_data[nfc_id].get("heisser_draht", []),
                "vier_gewinnt": game_data[nfc_id].get("vier_gewinnt", []),
                "puzzle": game_data[nfc_id].get("puzzle", []),
                "archived_date": datetime.now().isoformat(),
                "original_nfc_id": nfc_id
            }
            game_archive.append(archive_entry)
            save_archive()
            
            # Chip zurücksetzen für neuen Spieler
            game_data[nfc_id] = {
                "heisser_draht": [],
                "vier_gewinnt": [],
                "puzzle": []
            }
    
    # Namen zuweisen
    nfc_mapping[nfc_id] = name
    init_player_data(nfc_id)
    
    save_nfc_mapping()
    save_game_data()
    
    return jsonify({
        "status": "success",
        "nfc_id": nfc_id,
        "name": name,
        "message": f"Name '{name}' erfolgreich zugewiesen"
    })

# Letzten Update-Timestamp abrufen
@app.route('/api/last_update', methods=['GET'])
def get_last_update():
    return jsonify({"last_update": last_data_update})

# Urkunde generieren (für Spieler die alle Spiele abgeschlossen haben)
@app.route('/admin/certificate/<nfc_id>')
def generate_certificate_admin(nfc_id):
    if not has_completed_all_games(nfc_id):
        return "Spieler hat noch nicht alle Spiele abgeschlossen", 400
    
    player_data = {
        "name": get_player_name(nfc_id),
        "nfc_id": nfc_id,
        "heisser_draht": game_data[nfc_id]["heisser_draht"][-1] if game_data[nfc_id]["heisser_draht"] else None,
        "vier_gewinnt": game_data[nfc_id]["vier_gewinnt"][-1] if game_data[nfc_id]["vier_gewinnt"] else None,
        "puzzle": game_data[nfc_id]["puzzle"][-1] if game_data[nfc_id]["puzzle"] else None,
        "date": datetime.now().strftime('%d.%m.%Y')
    }
    
    return render_template('certificate_multi.html', player=player_data)

# Alle Chips löschen
@app.route('/admin/delete_all_chips', methods=['POST'])
def delete_all_chips():
    global nfc_mapping, game_data, game_archive
    
    # Backup erstellen
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_data = {
        "timestamp": timestamp,
        "reason": "delete_all_chips",
        "nfc_mapping": nfc_mapping.copy(),
        "game_data": game_data.copy(),
        "game_archive": game_archive.copy()
    }
    
    backup_filename = f"chips_backup_{timestamp}.json"
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=4, ensure_ascii=False)
    
    # Zähle Chips vor dem Löschen
    chip_count = len(set(list(nfc_mapping.keys()) + list(game_data.keys())))
    
    # Alle Daten archivieren
    for nfc_id in list(game_data.keys()):
        has_games = (
            len(game_data[nfc_id].get("heisser_draht", [])) > 0 or
            len(game_data[nfc_id].get("vier_gewinnt", [])) > 0 or
            len(game_data[nfc_id].get("puzzle", [])) > 0
        )
        if has_games:
            archive_entry = {
                "name": nfc_mapping.get(nfc_id, "Unbekannt"),
                "heisser_draht": game_data[nfc_id].get("heisser_draht", []),
                "vier_gewinnt": game_data[nfc_id].get("vier_gewinnt", []),
                "puzzle": game_data[nfc_id].get("puzzle", []),
                "archived_date": datetime.now().isoformat(),
                "original_nfc_id": nfc_id,
                "reason": "Alle Chips gelöscht"
            }
            game_archive.append(archive_entry)
    
    # Alle Chips und Mappings löschen
    nfc_mapping = {}
    game_data = {}
    
    save_nfc_mapping()
    save_game_data()
    save_archive()
    
    return jsonify({
        "success": True,
        "message": f"{chip_count} Chip(s) wurden gelöscht",
        "backup_file": backup_filename,
        "chips_deleted": chip_count
    })

# Leaderboard zurücksetzen
@app.route('/admin/reset_leaderboard', methods=['POST'])
def reset_leaderboard():
    game_type = request.form.get('game_type')  # 'all', 'heisser_draht', 'vier_gewinnt', 'puzzle'
    
    if not game_type:
        return jsonify({"success": False, "message": "Kein Spieltyp angegeben"}), 400
    
    # Backup erstellen vor dem Löschen
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_data = {
        "timestamp": timestamp,
        "game_type": game_type,
        "game_data": game_data.copy(),
        "game_archive": game_archive.copy()
    }
    
    backup_filename = f"leaderboard_backup_{game_type}_{timestamp}.json"
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=4, ensure_ascii=False)
    
    # Leaderboard(s) zurücksetzen
    if game_type == 'all':
        # Alle Spieldaten löschen
        for nfc_id in game_data:
            game_data[nfc_id] = {
                "heisser_draht": [],
                "vier_gewinnt": [],
                "puzzle": []
            }
        # Archiv leeren
        game_archive.clear()
        message = "Alle Leaderboards wurden zurückgesetzt"
    
    elif game_type in ['heisser_draht', 'vier_gewinnt', 'puzzle']:
        # Einzelnes Spiel zurücksetzen
        for nfc_id in game_data:
            game_data[nfc_id][game_type] = []
        
        # Aus Archiv entfernen
        for archive_entry in game_archive:
            archive_entry[game_type] = []
        
        game_names = {
            'heisser_draht': 'Heißer Draht',
            'vier_gewinnt': 'Vier Gewinnt',
            'puzzle': 'Puzzle'
        }
        message = f"Leaderboard '{game_names[game_type]}' wurde zurückgesetzt"
    
    else:
        return jsonify({"success": False, "message": "Ungültiger Spieltyp"}), 400
    
    # Daten speichern
    save_game_data()
    save_archive()
    
    return jsonify({
        "success": True,
        "message": message,
        "backup_file": backup_filename
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
