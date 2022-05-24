#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <string.h>
#include <string>
#include <sstream>
#include <iostream>
#include "SparkFunLSM6DSO.h"
#include "Wire.h"
#include <ArduinoJson.h>
//#include "SPI.h"

HTTPClient http;
LSM6DSO myIMU; //Default constructor is I2C, addr 0x6B

// char ssid[] = "iPhone";    // your network SSID (name) 
// char pass[] = "iloveturtles"; // your network password (use for WPA, or use as key for WEP)
char ssid[] = "McDonald's Irvine";
char pass[] = "iloveturtles";

// Name of the server we want to connect to
const char kHostname[] = "http://54.176.61.234:5000/";
// const int kPort = 5000;
// Path to download (this is the bit after the hostname in the URL
// that you want to download
char kPath[] = "";

// Number of milliseconds to wait without receiving any data before we give up
const int kNetworkTimeout = 30*1000;
// Number of milliseconds to wait if no data is available before trying again
const int kNetworkDelay = 1000;

bool curl = false;
int counter = 0;

void setup() {

  Serial.begin(9600);
  delay(500); 
  
  Wire.begin();
  delay(10);
  if( myIMU.begin() )
    Serial.println("Ready.");
  else { 
    Serial.println("Could not connect to IMU.");
    Serial.println("Freezing");
  }

  if( myIMU.initialize(BASIC_SETTINGS) )
    Serial.println("Loaded Settings.");

  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("MAC address: ");
  Serial.println(WiFi.macAddress());

}

void loop()
{
  HTTPClient http;
  float angle = myIMU.readFloatAccelZ();

  if (angle <= 0.2 and curl == false)
  {
    curl = true;
    counter++;

    Serial.println(counter);
  }
  if (angle >= 1)
  {
    curl = false;
  }

  WiFiClient c;
  http.begin(c, kHostname);

  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  double rep_times[] = {2.0, 1.5, 3.0, 4.0, 2.8, 2.5};
  int i;
  for (i = 0; i < sizeof(rep_times) / sizeof(double); i++) {
    doc["rep_times"][i] = rep_times[i];
  }

  String requestBody;
  serializeJson(doc, requestBody);

  // http.addHeader("Content-Type", "text/plain");
  // String s = "WASSUP";
  int httpResponseCode = http.POST(requestBody);

  if(httpResponseCode>0){
       
      String response = http.getString();                       
       
      Serial.println(httpResponseCode);   
      Serial.println(response);
     
    }
    else {
     
      Serial.printf("Error occurred while sending HTTP POST: %d\n", httpResponseCode);
       
    }
    
  http.end();
  
  delay(10000);
}