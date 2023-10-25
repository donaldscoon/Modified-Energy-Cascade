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
int timer = 1000;                   // 1000 milliseconds
int scale_pins[] = {7, 8, 9, 10};   // an array of pin numbers to which scales are attached
// int scale_num[] = {1,2,3,4};
const char* scale_num[] = {"scale1", "scale2", "scale3", "scale4"};

//////////////////////////////////////////////////////////////////////////////////////////

const int timeZoneOffset = 4; // Replace with your time zone offset

void setup() {
  Serial.begin(9600);

//////////////////////////////////////////////////////////////////////////////////////////

  scale1.begin(DOUT, CLK);
  scale2.begin(DOUT, CLK);
  scale3.begin(DOUT, CLK);
  scale4.begin(DOUT, CLK);

  scale1.set_scale(-470.98784);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale2.set_scale(-493.1443);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale3.set_scale(466.98718);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale4.set_scale(498.09172);//This value is obtained by using the SparkFun_HX711_Calibration sketch

  // int i = 0;
  // // this loop iterates throught the list of pins used to control the mosfets
  // // It selects a pin, turn it on (LOW POWER), waits a second, tares the scale, 
  // // shuts down, and waits a second before moving to the next pin/scale.
  // while (i < sizeof(scale_pins) / sizeof(scale_pins[0])) { 

  //   pinMode(scale_pins[i], OUTPUT);
  //   digitalWrite(scale_pins[i], LOW);

  //   // Need to fix this!
  //   i++;
  scale1.tare();
  scale2.tare();
  scale3.tare();
  scale4.tare();

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
  int i = 0;
  // this loop iterates throught the list of pins used to control the mosfets
  // It selects a pin, turn it on (LOW POWER), waits a second, takes a reading, 
  // shuts down, and waits a second before moving to the next pin/scale.
  while (i < sizeof(scale_pins) / sizeof(scale_pins[0])) { 
    // Pin Identification Debugger
    Serial.print("The Pin is ");
    Serial.print(scale_pins[i]);
    Serial.print(";");
    
    // Scale Identification Debugger
    Serial.print("The Scale is ");
    Serial.print(scale_num[i]);
    Serial.print(";");

    // Serial.print("Turning on pin ");
    // Serial.print(scale_pins[i]);
    // Serial.print(";");

    // // open mosfet switch, turning scale on
    // digitalWrite(scale_pins[i], LOW);
    // delay(timer);
    

    // Serial.print(scale3.get_units(3), 1); //scale.get_units() returns a float
    // Serial.print(";");

    // // close mosfet switch, turning scale off.
    // Serial.print("Turning off pin ");
    // Serial.print(scale_pins[i]);

    // digitalWrite(scale_pins[i], HIGH);
    // delay(timer);
    i++;

  }
//////////////////////////////////////////////////////////////////////////////////////////
  // pinMode(7, OUTPUT);     
  // digitalWrite(7, LOW);

  // Serial.print(scale3.get_units(3), 1); //scale.get_units() returns a float
  // Serial.print(";");

  // Serial.print(scale2.get_units(3), 1);
  // Serial.print(";");

  Serial.println(Runs);

  delay(1000);
  Runs=Runs+1;
  }