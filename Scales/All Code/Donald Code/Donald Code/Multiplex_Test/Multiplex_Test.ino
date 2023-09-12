#include <Wire.h>
#include <Arduino.h>
#include "HX711.h"
#include "TimeLib.h"

int Runs=0;


HX711 scale1;
HX711 scale2;
HX711 scale3;

const int timeZoneOffset = 4; // Replace with your time zone offset

// Select I2C BUS
void TCA9548A(uint8_t bus){
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
  // Serial.print(bus);
}

void setup() {
  Serial.begin(9600);
  
  // Start I2C communication with the Multiplexer
  Wire.begin();

  //setTime(hour, minute, second, day, month, year), Set time for when program starts and time is set to 24hr loop. There is also a 4 sec delay.
  setTime(18, 18, 0, 11, 9, 2023);

  Serial.println("Readings:In units of (g)");
  Serial.println("UTC Date: (day, month, year, hour, minute, second, Reading1, Reading2, Reading3, Reading4, Reading5, Runs)");
  delay(150);

  // Init sensor on bus number 0
  TCA9548A(0);
  scale1.begin(2,3); //HOW DO I WORK WITH THIS!!!
  scale1.set_scale(-498.9693);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale1.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

  // Init sensor on bus number 1
  TCA9548A(0);
  scale2.begin(2,3); //HOW DO I WORK WITH THIS!!!
  scale2.set_scale(-468.16);//This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale2.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

  
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

  printValues(scale1, 0);
  // Once I figure out how to get a reading from the first one I can do the rest.
  printValues(scale2, 1);
  // printValues(scale3, 2);
  Serial.println(Runs);
  delay(1000);
  Runs=Runs+1;
  }

void printValues(HX711 scale, int bus) {
  TCA9548A (bus);
  if(bus == 0) {
  Serial.print(scale1.get_units(3), 1); //scale.get_units() returns a float
  Serial.print(";");  }

// Once I figure out how to get a reading from the first one I can do the rest.
   if(bus == 1) {
  Serial.print(scale2.get_units(3), 1); //scale.get_units() returns a float
  Serial.print(";");  }

  // if(bus == 0) {
  // Serial.print(scale3.get_units(3), 1); //scale.get_units() returns a float
  // Serial.print(";");  }
}

// so right now the SDA and SCL are connected to the PWM 2/3 instead of A4/A5
// IDK why that gives an output but it does