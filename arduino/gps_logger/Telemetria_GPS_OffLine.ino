//Telemetria_GPS_OffLine.ino
//Luis C Buratini
//Primeira Versão criada em 30/05/2026
#include <Wire.h>
#include <RTClib.h>
#include <SPI.h>
#include <SD.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

RTC_DS3231 rtc;
TinyGPSPlus gps;

SoftwareSerial gpsSerial(4, 3); 
// D4 = RX do Arduino, recebe TX do GPS
// D3 = TX do Arduino, envia para RX do GPS

const int chipSelect = 10;
const unsigned long intervaloLog = 5000;

unsigned long ultimoLog = 0;

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);

  Serial.println("Iniciando RTC + SD + GPS...");

  if (!rtc.begin()) {
    Serial.println("ERRO: RTC DS3231 nao encontrado.");
    while (1);
  }

  if (rtc.lostPower()) {
    Serial.println("RTC sem horario. Ajustando com data/hora da compilacao.");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  if (!SD.begin(chipSelect)) {
    Serial.println("ERRO: Cartao SD nao iniciado.");
    while (1);
  }

  File arquivo = SD.open("LOG.CSV", FILE_WRITE);

  if (arquivo) {
    if (arquivo.size() == 0) {
      arquivo.println("Data;Hora;Latitude;Longitude;GoogleMaps;Satelites;Velocidade_kmh");
    }
    arquivo.close();
  } else {
    Serial.println("ERRO: Nao foi possivel criar LOG.CSV.");
  }

  Serial.println("Sistema pronto.");
}

void loop() {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  if (millis() - ultimoLog >= intervaloLog) {
    ultimoLog = millis();
    gravarLog();
  }
}

void gravarLog() {
  DateTime agora = rtc.now();

  File arquivo = SD.open("LOG.CSV", FILE_WRITE);

  if (!arquivo) {
    Serial.println("ERRO: Nao foi possivel abrir LOG.CSV.");
    return;
  }

  imprimirData(arquivo, agora);
  arquivo.print(";");

  imprimirHora(arquivo, agora);
  arquivo.print(";");

  if (gps.location.isValid()) {
    double latitude = gps.location.lat();
    double longitude = gps.location.lng();

    arquivo.print(latitude, 6);
    arquivo.print(";");

    arquivo.print(longitude, 6);
    arquivo.print(";");

    arquivo.print("https://www.google.com/maps?q=");
    arquivo.print(latitude, 6);
    arquivo.print(",");
    arquivo.print(longitude, 6);
    arquivo.print(";");

  } else {
    arquivo.print("SEM_FIX;");
    arquivo.print("SEM_FIX;");
    arquivo.print("SEM_FIX;");
  }

  if (gps.satellites.isValid()) {
    arquivo.print(gps.satellites.value());
  } else {
    arquivo.print("0");
  }

  arquivo.print(";");

  if (gps.speed.isValid()) {
    arquivo.println(gps.speed.kmph());
  } else {
    arquivo.println("0");
  }

  arquivo.close();

  Serial.println("Linha gravada no LOG.CSV");
}

void imprimirData(File &arquivo, DateTime dataHora) {
  if (dataHora.day() < 10) arquivo.print("0");
  arquivo.print(dataHora.day());
  arquivo.print("/");

  if (dataHora.month() < 10) arquivo.print("0");
  arquivo.print(dataHora.month());
  arquivo.print("/");

  arquivo.print(dataHora.year());
}

void imprimirHora(File &arquivo, DateTime dataHora) {
  if (dataHora.hour() < 10) arquivo.print("0");
  arquivo.print(dataHora.hour());
  arquivo.print(":");

  if (dataHora.minute() < 10) arquivo.print("0");
  arquivo.print(dataHora.minute());
  arquivo.print(":");

  if (dataHora.second() < 10) arquivo.print("0");
  arquivo.print(dataHora.second());
}