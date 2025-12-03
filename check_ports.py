import serial.tools.list_ports

print("\nSuche nach verfügbaren COM-Ports...\n")
ports = serial.tools.list_ports.comports()

if not ports:
    print("❌ Keine COM-Ports gefunden!")
    print("\nMögliche Ursachen:")
    print("1. Arduino/D1 Mini nicht angeschlossen")
    print("2. USB-Treiber fehlt (CH340/CP2102)")
    print("3. USB-Kabel defekt (nur Ladekabel)")
else:
    print(f"✓ {len(ports)} Port(s) gefunden:\n")
    for i, port in enumerate(ports, 1):
        print(f"{i}. {port.device}")
        print(f"   Beschreibung: {port.description}")
        print(f"   Hersteller: {port.manufacturer if port.manufacturer else 'Unbekannt'}")
        if port.vid and port.pid:
            print(f"   VID:PID = {hex(port.vid)}:{hex(port.pid)}")
        print()

input("\nDrücke Enter zum Beenden...")
