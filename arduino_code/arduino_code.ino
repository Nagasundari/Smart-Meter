int analogPin = A0;
int adcVal = 0; //variable to store the value read
double scaleFactor = 100.0;

#include "EEPROMAnything.h"

// <oled setup>
#include <Adafruit_GFX.h>
#include "Fonts/FreeSerif9pt7b.h"
#include <SPI.h>
#include <Wire.h>

int count = 0;
double usage = 0.0;

void setup()
{
    Serial.begin(9600);
    Serial3.begin(115200);
    //Setup serial
    EEPROM_readAnything(0, usage);
}

String data = "";

void loop()
{

    int peakAdc = 0;
    for (int i = 0; i < 150; ++i)
    {
        adcVal = analogRead(analogPin);
        peakAdc = max(adcVal, peakAdc);
    }
    double vout = (peakAdc / 1023.0) * 5000.0;
    double peakCurrent = (vout - 2500) / scaleFactor;
    double effCurrent = peakCurrent * 0.707;
    effCurrent = effCurrent < 0 ? 0 : effCurrent;
    Serial.print("Current: ");
    Serial.println(effCurrent);
    usage += ((230.0 * effCurrent) / 3600000.0);
    Serial.print("Usage: ");
    Serial.println(usage, 6);

    data = "";
    data += effCurrent;
    data += ";";
    data += usage;

    Serial3.println(data);

    if (Serial3.available())
    {
        String msg = "";
        while (Serial3.available())
        {
            msg += char(Serial3.read());
            delay(50);
        }
        Serial.println(msg);
    }
    //dispLED(String(effCurrent), String(usage));
    EEPROM_writeAnything(0, usage);
    delay(1000);
}
