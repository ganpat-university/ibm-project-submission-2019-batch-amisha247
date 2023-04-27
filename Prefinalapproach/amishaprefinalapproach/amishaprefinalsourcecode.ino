// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
//#define buzz 13
#define echoPin 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 9 //attach pin D3 Arduino to pin Trig of HC-SR04
// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
void setup() {
Serial.begin(9600);
dht.begin();
pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
//pinMode(buzz,OUTPUT);
sensor_t sensor;
 // // Serial Communication is starting with 9600 of baudrate speed

Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
Serial.println("with Arduino UNO R3");
Serial.println(F("DHTxx Unified Sensor Example"));
 
}
void loop() {
  long per;
// Clears the trigPin condition
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin HIGH (ACTIVE) for 10 microseconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance = duration * 0.034 / 2;
per = map(distance, 10.5, 2, 0, 100);// Speed of sound wave divided by 2 (go and back)
// Displays the distance on the Serial Monitor
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  //dht.humidity().getEvent(&event);
   // Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.print(",");
    //Serial.println("C");
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
    //Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.print(",");
    //Serial.println("%");
    //delay(1000);
//Serial.print("Distance: ");
Serial.print(per);
Serial.print("\n");
//Serial.println(" cm");
//if (per >= 80 && per<=100)
//{
//Serial.print("Red Alert!  ");  
//}
//else if (per >= 55 && per<80)
//{
// Serial.print("Orange Alert!  ");  
//}
//else
//{
// Serial.print("Green Alert!  ");
//}

}

