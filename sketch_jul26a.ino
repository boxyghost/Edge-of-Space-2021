#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Wire.h>

TinyGPSPlus gps;



void setup() {
    Serial.begin(9600);
    Serial2.begin(9600);
}

void loop() {
    if(Serial2.available() > 0) {
        if(gps.encode(Serial2.read())) {
            if(gps.location.isUpdated()) {
                Serial.println("Lat," + String(gps.location.lat(), 6) + ",Lon," + String(gps.location.lng(), 6));
                //Serial.println( + String(gps.location.lat(), 6) + ", Lon:" + String(gps.location.lng(), 6))
            }
            delay(100);
        }
    }
    
}
