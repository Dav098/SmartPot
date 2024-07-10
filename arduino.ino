//    PHOTORESISTOR
#define PHOTORESISTOR A1

//    DHT11
#include "DHT.h"        
#define DHTPIN 2          
#define DHTTYPE DHT11     
DHT dht(DHTPIN, DHTTYPE);

//    LED_STRIP
#define redPin 11
#define greenPin 10
#define bluePin 9

//    SOIL HUMIDITY SENSOR (SHS)
#define sensor_A0 A0       
#define sensor_D0 4 
int value_A0;
int value_D0;

//------------------------SETUP-----------------------------------------------------

void setup_dht11()
  {
    dht.begin();            // sensor initialization
  }

void setup_led(){
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void setup_SHS() {
  pinMode(4, INPUT);    // setting pin 4 as input
 
}
    

//-------------------------FUNCTIONS--------------------------------------------------- 
float t;
float h;
void dht11()
{
  t = dht.readTemperature();  // air temperature reading
  h = dht.readHumidity();     // air humidity reading
  // Have the values ​​been read?
  if (isnan(t) || isnan(h))
  {
    Serial.println("Error reading data from the sensor!");
  }
  else
  {
    //sending the results via the serial port
    Serial.print('t');
    Serial.print(t); //air temperature in *C
    delay(200);
    Serial.print('h');
    Serial.print(h); //air humidity in %
    delay(200);
  }
     
}



void TurnOn_Led()
{
  analogWrite(redPin, 255);
  analogWrite(greenPin, 255);
  analogWrite(bluePin, 255);
  Serial.print("LLed On");
  delay(200);
}
void TurnOff_Led()
{
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
  Serial.print("LLed Off");
  delay(200);
}



void SHS()
{
 value_A0 = analogRead(sensor_A0);     
 value_D0 = digitalRead(sensor_D0);     

 Serial.print('d');
 Serial.print(value_D0);    
 delay(200);
 Serial.print('a');
 Serial.print(value_A0);    
 delay(200);                              // delay between subsequent readings
 } 
 
//////////////////////////////////////////////////////////////////////////////////////////
void setup()
  {
    Serial.begin(9600);   // starting the serial monitor
    setup_dht11();
    setup_led();
    setup_SHS();
  }
  
void loop()
{
  dht11();
  SHS();
  if(analogRead(PHOTORESISTOR) <= 200)   //if the light value is less than ... then do...
  { 
    TurnOn_Led();
  }
  else{
    //if it's clear then...
    TurnOff_Led();
  }
  
  delay(30000);
  
}
  