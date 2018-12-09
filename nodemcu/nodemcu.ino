#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <timer.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

bool lighting= true;
MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]={75,75,75,75}; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

signed long ir_ok = 0;

float beatsPerMinute;
int beatAvg;
auto timer = timer_create_default(); 
unsigned char mac[6];
String dev_id="";


void postData(float temperature,int heart){
  String url = "http://139.199.68.189:81/driverstate_nodemcu_api?driverId="+dev_id+"&temperature="+temperature+"&heart="+heart;
  HTTPClient http; 
  http.begin(url); 
  for(int i=0;i<3;i++){
    if(http.GET()==200)
      break;
  }
  http.end();
}

bool flash(void *) {
  static int i=0;
  i++;
  if(i%30==0){
    i=0;
    float temperature = particleSensor.readTemperature();
    if(ir_ok<0){//没有手
        beatAvg = -1;
        temperature = -1;
        ir_ok = 0;
    }
    Serial.print("beat:");
    Serial.print(beatAvg);
    Serial.print("  temp:");
    Serial.print(temperature,4);
    Serial.println();
    postData(temperature,beatAvg);
  }
  Serial.print("time:");
  Serial.println(i);
  return true;
}


void setup()
{
  Serial.begin(115200);
  Serial.println("Initializing...");
  WiFi.macAddress(mac);
  for (int i = 0; i < 6; i++)
      {
        dev_id+=String(mac[i],HEX);
        Serial.print(mac[i],HEX);
      }
  Serial.println("dev_id = "+dev_id);
  WiFi.mode(WIFI_STA);
  WiFi.begin("CMCC", "CMCCCMCC");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println(WiFi.localIP());
  
  timer.every(1000, flash);
  // Initialize sensor

  
  
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  Serial.println("Place your index finger on the sensor with steady pressure.");

  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
}


void loop()
{
  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true)
  {
    //We sensed a beat!
    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = (60 / (delta / 1000.0));

    if (beatsPerMinute < 255 && beatsPerMinute > 50)
    {
      rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
      rateSpot %= RATE_SIZE; //Wrap variable

      //Take average of readings
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++)
        beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }
  if (irValue < 50000) ir_ok--;
  else  ir_ok++;
  timer.tick();
}
