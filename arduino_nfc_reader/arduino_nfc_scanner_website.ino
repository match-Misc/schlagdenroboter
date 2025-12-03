/*
 * NFC Scanner für Website-Integration
 * 
 * Hardware:
 * - Arduino Nano (oder Uno, Mega)
 * - MFRC522 RFID Reader (13.56 MHz)
 * 
 * Pin-Mapping:
 * MFRC522    Arduino Nano
 * ========   ============
 * SDA/SS  →  D10
 * SCK     →  D13
 * MOSI    →  D11
 * MISO    →  D12
 * RST     →  D9
 * 3.3V    →  3.3V (NICHT 5V!)
 * GND     →  GND
 * 
 * Funktion:
 * - Liest NFC-Tags
 * - Sendet UID an PC über Serial (9600 Baud)
 * - Format: "NFC_ID:XXXXXXXX"
 * - PC-Software (nfc_network_bridge.py) sendet an Server
 */

#include <SPI.h>
#include <MFRC522.h>

// Pin-Konfiguration
#define RST_PIN 9
#define SS_PIN 10

// MFRC522 initialisieren
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Variablen
unsigned long lastScanTime = 0;
const unsigned long SCAN_COOLDOWN = 2000;  // 2 Sekunden zwischen Scans
String lastNfcId = "";

void setup() {
  // Serielle Kommunikation starten
  Serial.begin(9600);
  while (!Serial);
  
  // SPI initialisieren
  SPI.begin();
  
  // MFRC522 initialisieren
  mfrc522.PCD_Init();
  delay(50);
  
  // Firmware-Version prüfen
  byte version = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  
  Serial.println("=================================");
  Serial.println("  NFC Scanner für Website");
  Serial.println("=================================");
  
  if (version == 0x00 || version == 0xFF) {
    Serial.println("ERROR: MFRC522 nicht gefunden!");
    Serial.print("Firmware Version: 0x");
    Serial.println(version, HEX);
    Serial.println("Prüfe Verkabelung!");
  } else {
    Serial.println("MFRC522 bereit!");
    Serial.print("Firmware Version: 0x");
    Serial.println(version, HEX);
  }
  
  Serial.println("=================================");
  Serial.println("Warte auf NFC-Tags...");
  Serial.println();
}

void loop() {
  // Prüfe ob neue Karte vorhanden
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  
  // Versuche Karte zu lesen
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Cooldown prüfen
  unsigned long currentTime = millis();
  if (currentTime - lastScanTime < SCAN_COOLDOWN) {
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
    return;
  }
  
  // NFC-ID auslesen und formatieren
  String nfcId = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) {
      nfcId += "0";
    }
    nfcId += String(mfrc522.uid.uidByte[i], HEX);
  }
  nfcId.toUpperCase();
  
  // Nur senden wenn neue ID
  if (nfcId != lastNfcId) {
    // NFC-ID an PC senden (für nfc_network_bridge.py)
    Serial.print("NFC_ID:");
    Serial.println(nfcId);
    
    // Debug-Info
    Serial.print("  -> Tag erkannt: ");
    Serial.print(nfcId);
    Serial.print(" (");
    Serial.print(mfrc522.uid.size);
    Serial.println(" Bytes)");
    
    lastNfcId = nfcId;
    lastScanTime = currentTime;
  }
  
  // Karte anhalten
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  
  // Kurze Pause
  delay(100);
}
