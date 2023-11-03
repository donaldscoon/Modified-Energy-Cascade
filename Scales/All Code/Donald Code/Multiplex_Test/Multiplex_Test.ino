#include <Wire.h>
#include <Arduino.h>
#include "HX711.h"
#include "TimeLib.h"

int Runs=0;

const int CLK = 4;   
const int DOUT = 2;  

HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;

// HX711 scales[4];  // Array of HX711 objects
//////////////////////////////////////////////////////////////////////////////////////////
int timer = 1000;                   // 1000 milliseconds
int scale_pins[] = {7, 8, 9, 10};   // an array of pin numbers to which scales are attached

//////////////////////////////////////////////////////////////////////////////////////////

const int timeZoneOffset = 4; // Replace with your time zone offset

void turnon(int sensorpin) {
  digitalWrite(sensorpin, LOW);
  delay(1000);
}
void turnoff(int sensorpin) {
  digitalWrite(sensorpin, HIGH);
}

void turnoffall() {
  for (int i = 0; i < sizeof(scale_pins) / sizeof(scale_pins[0]); i++) {
    turnoff(scale_pins[i]);
  }
}

float read(HX711 scale, int sensorpin) {
  turnon(sensorpin);
  float weight = scale.get_units(3);
  turnoffall();
  return weight;
}
void setup() {
  Serial.begin(9600);
  
  Serial.print("\nSetup");

//////////////////////////////////////////////////////////////////////////////////////////
  // for (int i = 0; i < 4; i++) {
  //   scales[i].begin(DOUT, CLK);

  //   scales[i].set_scale(getScaleFactor(i));

  //   scales[i].tare(); 
  // }
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  turnoffall();

  // scale1.begin(DOUT, CLK);
  // scale2.begin(DOUT, CLK);
  
  turnoffall(); turnon(7); 
  scale3.begin(DOUT, CLK); delay(1000);
  scale3.set_scale(466.98718);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale3.tare();
  
  turnoffall(); turnon(8);
  scale4.begin(DOUT, CLK);
  scale4.set_scale(498.09172);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale4.tare();

  // scale1.set_scale(-470.98784);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  // scale2.set_scale(-493.1443);//This value is obtained by using the SparkFun_HX711_Calibration sketch

  // scale1.tare();
  // scale2.tare();


  //setTime(hour, minute, second, day, month, year), Set time for when program starts and time is set to 24hr loop. There is also a 4 sec delay.
  // setTime(18, 18, 0, 11, 9, 2023);

  // Serial.println("Readings:In units of (g)");
  // Serial.println("UTC Date: (day, month, year, hour, minute, second, Reading1, Reading2, Reading3, Reading4, Reading5, Runs)");
  // delay(150);
  Serial.println(" -> Done");
  turnoffall();
  }

void loop() { 
  // //Print values for sensor 1
  // time_t localTime = now();  // Get the local time
  // // Calculate the approximate UTC time
  // time_t utcTime = localTime - timeZoneOffset;
  
  // Serial.print(year(utcTime)); Serial.print("-");
  // Serial.print(month(utcTime)); Serial.print("-");
  // Serial.print(day(utcTime)); Serial.print(" ");  
  // Serial.print(hour(utcTime)); Serial.print(":");
  // Serial.print(minute(utcTime)); Serial.print(":");
  // Serial.print(second(utcTime)); Serial.print(";");

//////////////////////////////////////////////////////////////////////////////////////////
  // // loop from the lowest pin to the highest:
  // int i = 0;
  // // this loop iterates throught the list of pins used to control the mosfets
  // // It selects a pin, turn it on (LOW POWER), waits a second, takes a reading, 
  // // shuts down, and waits a second before moving to the next pin/scale.
  // while (i < sizeof(scale_pins) / sizeof(scale_pins[0])) { 
  //   // Pin Identification Debugger
  //   Serial.print("Pin: ");
  //   Serial.print(scale_pins[i]);
  //   Serial.print(";");
    
  //   // Scale Identification Debugger
  //   Serial.print("Scale: ");
  //   Serial.print(i);
  //   Serial.print(";");

  // //   // Serial.print("Turning on pin ");
  // //   // Serial.print(scale_pins[i]);
  // //   // Serial.print(";");

  //   // open mosfet switch, turning scale on
  //   digitalWrite(scale_pins[i], LOW);
  //   delay(timer);
    

  //   Serial.print(scales[i].get_units(3), 1); //scale.get_units() returns a float
  //   Serial.print(";");

  //   // // close mosfet switch, turning scale off.
  //   // Serial.print("Turning off pin ");
  //   // Serial.print(scale_pins[i]);

  //   digitalWrite(scale_pins[i], HIGH);
  //   delay(timer);
  //   i++;
  //   Serial.print(i);
  // }
//////////////////////////////////////////////////////////////////////////////////////////
  // Turn on pin 7, opening mosfet, collect data, turn off pin, close mosfet
  Serial.println("Scale 3: " + String(read(scale3, 7)));
  
  // Turn on pin 8, opening mosfet, collect data, turn off pin, close mosfet
  Serial.println("Scale 4: " + String(read(scale4, 8)));

  Serial.println(Runs);

  delay(1000);
  Runs=Runs+1;
  }

  // Helper function to get the scale factor for each scale based on its index
float getScaleFactor(int index) {
  switch (index) {
    case 0:
      return -470.98784;
    case 1:
      return -493.1443;
    case 2:
      return 466.98718;
    case 3:
      return 498.09172;
    default:
      return 1.0;  // Default scale factor if index is out of range
  }
}