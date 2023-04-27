#include <dht11.h>
#define DHT11PIN 4

dht11 DHT11;

const int trigPin = 9;
const int echoPin = 10;

long duration;
int distance;
void setup()
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT11.read(DHT11PIN);
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print((float)DHT11.humidity, 2);
  Serial.print('-');
  Serial.print((float)DHT11.temperature, 2);
  Serial.print('-');
  Serial.println(distance);

  delay(2000);
}
