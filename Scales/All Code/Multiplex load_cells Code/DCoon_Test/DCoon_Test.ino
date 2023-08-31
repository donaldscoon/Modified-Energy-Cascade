
#include <Arduino.h>
#include "HX711.h"
#include "TimeLib.h"

const int DOUT1 = 2;  
const int CLK1 = 3;   
const int DOUT2 = 4;   
const int CLK2 = 5;    
const int DOUT3 = 9;
const int CLK3 = 8;

int Runs=0;
 
HX711 scale1;
HX711 scale2;
HX711 scale3;

const int timeZoneOffset = 4; // Replace with your time zone offset

void setup() {
  Serial.begin(9600);
  
  scale1.begin(DOUT1, CLK1);
  scale2.begin(DOUT2, CLK2);
  scale3.begin(DOUT3, CLK3);
  
  scale1.set_scale(-468.16);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale2.set_scale(-498.9693);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale3.set_scale(-497.12);

  scale1.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
  scale2.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0
  scale3.tare();
  
  //setTime(hour, minute, second, day, month, year), Set time for when program starts and time is set to 24hr loop. There is also a 4 sec delay.
   setTime(20, 30, 4, 21, 6, 2023);
  
  Serial.println("Readings:In units of (g)");
  Serial.println("UTC Date: (day, month, year, hour, minute, second, Reading1, Reading2, Reading3, Reading4, Reading5, Runs)");
  delay(150);
}

void loop() {
  time_t localTime = now();  // Get the local time
  // Calculate the approximate UTC time
  time_t utcTime = localTime - timeZoneOffset;

  Runs=Runs+1;
  
  Serial.print(year(utcTime));
  Serial.print("-");
  Serial.print(month(utcTime));
  Serial.print("-");
  Serial.print(day(utcTime));
  Serial.print(" ");  

  Serial.print(hour(utcTime));
  Serial.print(":");
  Serial.print(minute(utcTime));
  Serial.print(";");
    
  //Serial.print("Reading 1: ");
  Serial.print(scale1.get_units(3), 1); //scale.get_units() returns a float
  //Serial.print(" g"); //You can change this to kg but you'll need to refactor the calibration_factor
  Serial.print(";");
  
  //Serial.print("Reading 2: ");
  Serial.print(scale2.get_units(3), 1); //scale.get_units() returns a float
  //Serial.println(" g"); //You can change this to kg but you'll need to refactor the calibration_factor
  Serial.print(";");
  
  //Serial.print("Reading 3: ");
  Serial.print(scale3.get_units(3), 1); //scale.get_units() returns a float
  //Serial.println(" g"); //You can change this to kg but you'll need to refactor the calibration_factor
  Serial.print(";");
  Serial.println(Runs);

  //String csvLine = String(SD1)+"g ;"+String(SD2)+"g ;"+String(SD3)+"g";
  delay(1500);
}
