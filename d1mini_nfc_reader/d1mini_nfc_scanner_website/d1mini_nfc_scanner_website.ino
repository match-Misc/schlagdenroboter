/*
 * NFC Scanner für Website-Integration (D1 Mini Version)
 * 
 * Hardware:
 * - Wemos D1 Mini (ESP8266)
 * - MFRC522 RFID Reader (13.56 MHz)
 * 
 * Pin-Mapping:
 * MFRC522    D1 Mini V4.0
 * ========   =============
 * SDA/SS  →  D8 (GPIO15)
 * SCK     →  D5 (GPIO14)
 * MOSI    →  D7 (GPIO13)
 * MISO    →  D6 (GPIO12)
 * RST     →  D3 (GPIO0)
 * 3.3V    →  3.3V
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

// Pin-Konfiguration für D1 Mini
#define RST_PIN D3   // GPIO0
#define SS_PIN D8    // GPIO15

// MFRC522 initialisieren
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Variablen
unsigned long lastScanTime = 0;
const unsigned long SCAN_COOLDOWN = 2000;  // 2 Sekunden zwischen Scans
String lastNfcId = "";

void setup() {
  // Serielle Kommunikation starten
  Serial.begin(9600);
  delay(100);
  
  // SPI initialisieren (D1 Mini verwendet Hardware-SPI)
  // D5 = SCK, D6 = MISO, D7 = MOSI
  SPI.begin();
  delay(50);
  
  // MFRC522 initialisieren
  mfrc522.PCD_Init();
  delay(50);
  
  // Firmware-Version prüfen
  byte version = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  
  Serial.println("=================================");
  Serial.println("  NFC Scanner für Website");
  Serial.println("  (D1 Mini Version)");
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
