#include <Wire.h>
#include <Arduino.h>
#include "HX711.h"
#include "TimeLib.h"

int Runs=0;

const int CLK = 3;   
const int DOUT = 2;  

HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;

//////////////////////////////////////////////////////////////////////////////////////////
int timer = 1000;           // The higher the number, the slower the timing.
int scale_pins[] = {7, 8};       // an array of pin numbers to which LEDs are attached
int pinCount = 2;           // the number of pins (i.e. the length of the array)
//////////////////////////////////////////////////////////////////////////////////////////

const int timeZoneOffset = 4; // Replace with your time zone offset

void setup() {
  Serial.begin(9600);

// // These turn on the pins, need to be automated
//   pinMode(7, OUTPUT);     
//   digitalWrite(7, HIGH);

//   pinMode(8, OUTPUT);     
//   digitalWrite(8, HIGH);
//////////////////////////////////////////////////////////////////////////////////////////
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {

    pinMode(scale_pins[thisPin], OUTPUT);

  }
//////////////////////////////////////////////////////////////////////////////////////////

  scale1.begin(DOUT, CLK);
  scale2.begin(DOUT, CLK);

  scale1.set_scale(-498.9693);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale2.set_scale(-468.1573);//This value is obtained by using the SparkFun_HX711_Calibration sketch

  scale1.tare();
  scale2.tare();

  //setTime(hour, minute, second, day, month, year), Set time for when program starts and time is set to 24hr loop. There is also a 4 sec delay.
  setTime(18, 18, 0, 11, 9, 2023);

  Serial.println("Readings:In units of (g)");
  Serial.println("UTC Date: (day, month, year, hour, minute, second, Reading1, Reading2, Reading3, Reading4, Reading5, Runs)");
  delay(150);

  }

void loop() { 
  //Print values for sensor 1
  time_t localTime = now();  // Get the local time
  // Calculate the approximate UTC time
  time_t utcTime = localTime - timeZoneOffset;
  
  Serial.print(year(utcTime)); Serial.print("-");
  Serial.print(month(utcTime)); Serial.print("-");
  Serial.print(day(utcTime)); Serial.print(" ");  
  Serial.print(hour(utcTime)); Serial.print(":");
  Serial.print(minute(utcTime)); Serial.print(":");
  Serial.print(second(utcTime)); Serial.print(";");

//////////////////////////////////////////////////////////////////////////////////////////
  // loop from the lowest pin to the highest:

  for (int thisPin = 0; thisPin < pinCount; thisPin++) {

    // open mosfet switch, turning scale on
    digitalWrite(scale_pins[thisPin], LOW);

    Serial.print(scale1.get_units(3), 1); //scale.get_units() returns a float
    Serial.print(";");

    // close mosfet switch, turning scale off.
    digitalWrite(scale_pins[thisPin], HIGH);
    delay(timer);

  }
//////////////////////////////////////////////////////////////////////////////////////////

  // Serial.print(scale1.get_units(3), 1); //scale.get_units() returns a float
  // Serial.print(";");

  // Serial.print(scale2.get_units(3), 1); //scale.get_units() returns a float
  // Serial.print(";");

  Serial.println(Runs);

  delay(1000);
  Runs=Runs+1;
  }