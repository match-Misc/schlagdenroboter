#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>

// NFC MFRC522 Pins für D1 Mini
#define RST_PIN D3     // Reset Pin (GPIO0)
#define SS_PIN D4      // SDA/SS Pin (GPIO2) - Chip Select

// WLAN-Konfiguration
const char* ssid = "MiR_Wlan";
const char* password = "match123";

// Server-URL - WICHTIG: Port 5000 für Flask Server!
const char* serverURL = "http://10.145.8.50:5000/api/heisser_draht";

// Variablen für die serielle Kommunikation
String arduinoData = "";  // Empfangene Daten vom Arduino

// NFC-Variablen
MFRC522 mfrc522(SS_PIN, RST_PIN);  // NFC-Modul initialisieren
bool nfcTagDetected = false;       // Status, ob NFC-Tag erkannt wurde
unsigned long lastNFCCheck = 0;    // Zeitstempel für NFC-Prüfung
const unsigned long nfcCheckInterval = 300; // NFC alle 300ms prüfen
String currentNfcId = "";          // Speichert die aktuelle NFC-ID

// Erstelle ein WiFiClient-Objekt
WiFiClient wifiClient;

// Setup-Funktion
void setup() {
  // Starte serielle Kommunikation mit Arduino Nano
  Serial.begin(115200);
  delay(100);
  
  // SPI-Bus initialisieren für D1 Mini
  // D5 = SCK, D6 = MISO, D7 = MOSI
  SPI.begin();
  delay(50);
  
  // NFC-Modul initialisieren
  mfrc522.PCD_Init();
  delay(50);
  
  // Prüfe, ob NFC-Modul antwortet
  byte version = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  if (version == 0x00 || version == 0xFF) {
    Serial.println("ERROR: NFC-Reader nicht gefunden!");
    Serial.print("Version: 0x");
    Serial.println(version, HEX);
  } else {
    Serial.println("NFC-Reader initialisiert.");
    Serial.print("Firmware Version: 0x");
    Serial.println(version, HEX);
  }
  
  Serial.println("Warte auf NFC-Tag...");
  
  // Verbindung mit dem WLAN herstellen
  WiFi.begin(ssid, password);
  Serial.print("Verbinde mit WiFi");
  
  int wifiTimeout = 0;
  while (WiFi.status() != WL_CONNECTED && wifiTimeout < 20) {
    delay(500);
    Serial.print(".");
    wifiTimeout++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nVerbunden mit WiFi!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi-Verbindung fehlgeschlagen!");
  }
}

void loop() {
  // NFC-Tag prüfen, wenn noch nicht erkannt
  if (!nfcTagDetected) {
    unsigned long currentMillis = millis();
    if (currentMillis - lastNFCCheck >= nfcCheckInterval) {
      lastNFCCheck = currentMillis;
      checkForNFCTag();
    }
  }
  
  // Wenn serielle Daten vom Arduino Nano empfangen (Spieldaten)
  if (Serial.available()) {
    arduinoData = Serial.readStringUntil('\n');  // Lese bis Zeilenende
    arduinoData.trim();  // Entferne Leerzeichen und Zeilenumbrüche
    
    // Prüfe ob es ein RESET-Kommando ist
    if (arduinoData.equals("RESET_NFC")) {
      // NFC-Status zurücksetzen für neue Runde
      nfcTagDetected = false;
      currentNfcId = "";
      
      // NFC-Modul neu initialisieren für nächsten Scan
      mfrc522.PCD_Init();
      delay(50);
      
      Serial.println("DEBUG: NFC-Status zurückgesetzt");
      return;
    }
    
    Serial.print("DEBUG: Empfangene Daten: ");
    Serial.println(arduinoData);

    // Daten im Format: "correctedTime,errors,difficulty"
    int correctedTime = 0;
    int errors = 0;
    int difficulty = 0;
    
    // Versuche, die Daten anhand der Kommas zu teilen
    int comma1 = arduinoData.indexOf(',');
    int comma2 = arduinoData.indexOf(',', comma1 + 1);
    
    if (comma1 != -1 && comma2 != -1) {
      correctedTime = arduinoData.substring(0, comma1).toInt();
      errors = arduinoData.substring(comma1 + 1, comma2).toInt();
      difficulty = arduinoData.substring(comma2 + 1).toInt();
      
      Serial.print("DEBUG: Time=");
      Serial.print(correctedTime);
      Serial.print(", Errors=");
      Serial.print(errors);
      Serial.print(", Difficulty=");
      Serial.println(difficulty);

      // Sende die Werte an den Server
      sendToServer(currentNfcId, correctedTime, errors, difficulty);
      
      // Nach dem Senden NFC-Status zurücksetzen
      nfcTagDetected = false;
      currentNfcId = "";
      
      // NFC-Modul neu initialisieren
      mfrc522.PCD_Init();
      delay(50);
      Serial.println("DEBUG: Bereit für neuen NFC-Tag");
    } else {
      Serial.println("ERROR: Fehler beim Parsen der Daten");
    }
  }
}

void checkForNFCTag() {
  // Prüfe, ob eine neue Karte vorhanden ist
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Versuche, die Karte zu lesen
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // NFC-Tag wurde erkannt
  Serial.println("DEBUG: NFC-Tag erkannt!");
  
  // Zeige UID des NFC-Tags an und speichere sie
  currentNfcId = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    // Formatiere jedes Byte als 2-stelligen Hex-Wert
    if (mfrc522.uid.uidByte[i] < 0x10) {
      currentNfcId += "0";
    }
    currentNfcId += String(mfrc522.uid.uidByte[i], HEX);
  }
  currentNfcId.toUpperCase();
  
  Serial.print("DEBUG: UID: ");
  Serial.println(currentNfcId);
  
  // Setze Flag und sende Signal an Arduino Nano
  nfcTagDetected = true;
  
  // WICHTIG: Sende "NFC_OK" an Arduino Nano (über Serial TX)
  Serial.println("NFC_OK");
  Serial.flush();  // Warte bis die Daten gesendet wurden
  
  // Halt PICC
  mfrc522.PICC_HaltA();
  // Stop encryption on PCD
  mfrc522.PCD_StopCrypto1();
}

void sendToServer(String nfcId, int correctedTime, int errors, int difficulty) {
  // Prüfe, ob WiFi verbunden ist
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(wifiClient, serverURL);
    http.addHeader("Content-Type", "application/json");
    
    float timeInSeconds = correctedTime;
    
    StaticJsonDocument<200> doc;
    doc["nfc_id"] = nfcId;
    doc["time"] = timeInSeconds;
    doc["errors"] = errors;
    doc["difficulty"] = getDifficultyString(difficulty);

    String jsonString;
    serializeJson(doc, jsonString);
    
    Serial.println("DEBUG: Sende an Server:");
    Serial.println(jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.print("DEBUG: HTTP Response: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("ERROR: POST fehlgeschlagen: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("ERROR: Nicht mit WiFi verbunden");
  }
}

String getDifficultyString(int difficulty) {
  switch (difficulty) {
    case 1:
      return "Einfach";
    case 2:
      return "Mittel";
    case 3:
      return "Schwer";
    default:
      return "Unbekannt";
  }
}
