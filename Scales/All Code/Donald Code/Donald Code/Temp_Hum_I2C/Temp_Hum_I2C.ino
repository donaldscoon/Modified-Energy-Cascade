
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ---- Description ----
// This Sensor Array is collecting data 5 SHT31 Temp/Hum I2C Sensors connected to a multiplexer
// It is outputting this data to serial monitor for Python code to extract. 
// Extra values are being output as "NA" for MySQL database uniformity/functionality
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <Wire.h>
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SHT31.h>

Adafruit_SHT31 sht1; // I2C
Adafruit_SHT31 sht2; // I2C
Adafruit_SHT31 sht3; // I2C
Adafruit_SHT31 sht4; // I2C
Adafruit_SHT31 sht5; // I2C

// Select I2C BUS
void TCA9548A(uint8_t bus){
  Wire.beginTransmission(0x70);  // TCA9548A address
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}


////////////////////////////////////////////////////////////////////////////////////////////////



void setup() {
  Serial.begin(9600);
  
  // Start I2C communication with the Multiplexer
  Wire.begin();


  // Init sensor on bus number 2
  TCA9548A(1);
  if (!sht1.begin(0x44)) {
    Serial.print("NA");  Serial.print(",");
    Serial.print("NA");  Serial.print(",");  }

  
  // Init sensor on bus number 3
  TCA9548A(2);
  if (!sht2.begin(0x44)) {
    Serial.print("NA");  Serial.print(",");
    Serial.print("NA");  Serial.print(",");  }
  
  // Init sensor on bus number 4
  TCA9548A(3);
  if (!sht3.begin(0x44)) {
    Serial.print("NA");  Serial.print(",");
    Serial.print("NA");  Serial.print(",");  }
  
  // Init sensor on bus number 5
  TCA9548A(4);
  if (!sht4.begin(0x44)) {
    Serial.print("NA");  Serial.print(",");
    Serial.print("NA");  Serial.print(",");  }

  // Init sensor on bus number 5
  TCA9548A(5);
  if (!sht5.begin(0x44)) {
    Serial.print("NA");  Serial.print(",");
    Serial.print("NA");  Serial.print(",");  }

}


////////////////////////////////////////////////////////////////////////////////////////////////


void loop() { 
  //Print values for sensor 1
  printValues(sht1, 1);
  printValues(sht2, 2);
  printValues(sht3, 3);
  printValues(sht4, 4);
  printValues(sht5, 5);
  Serial.println();
  delay(9750);
}


////////////////////////////////////////////////////////////////////////////////////////////////



void printValues(Adafruit_SHT31 sht, int bus) {
  TCA9548A (bus);

  if(bus == 1) {
  //Serial.print("temp_sensor");  Serial.print(";");
  Serial.print(sht.readTemperature());  Serial.print(",");
  //Serial.print("hum_sensor");  Serial.print(";");
  Serial.print(sht.readHumidity());  Serial.print(",");   }

  if(bus == 2) {
  //Serial.print("temp_outside");  Serial.print(";");
  Serial.print(sht.readTemperature());  Serial.print(",");
  //Serial.print("hum_outside");  Serial.print(";");
  Serial.print(sht.readHumidity());  Serial.print(",");   }

  if(bus == 3) {
  //Serial.print("temp_upper");  Serial.print(";");
  Serial.print(sht.readTemperature());  Serial.print(",");
  //Serial.print("hum_upper");  Serial.print(";");
  Serial.print(sht.readHumidity());  Serial.print(",");   }

  if(bus == 4) {
  //Serial.print("temp_intake");  Serial.print(";");
  Serial.print(sht.readTemperature());  Serial.print(",");
  //Serial.print("hum_intake");  Serial.print(";");
  Serial.print(sht.readHumidity());  Serial.print(",");   }
  
  if(bus == 5) {
  //Serial.print("temp_outflow");  Serial.print(";");
  Serial.print(sht.readTemperature());  Serial.print(",");
  //Serial.print("hum_outflow");  Serial.print(";");
  Serial.print(sht.readHumidity());  Serial.print(",");   }

}
