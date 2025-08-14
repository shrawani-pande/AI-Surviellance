#include <ESPAsyncWebServer.h>
#include "WiFi.h"

const char* ssid = "Realme";
const char* pass = "12345678";

#define BUZZER_PIN 25

// Setup server at port 8080
AsyncWebServer server (8080);

void InitLockdown(AsyncWebServerRequest *request){
  
  Serial.println("Alarm ON");
  digitalWrite(BUZZER_PIN, HIGH); 
  
  request->send_P(200, "text/plain", "Lockdown Started Successfully");
}

void StopLockdown(AsyncWebServerRequest *request){
  
  Serial.println("Alarm OFF");
  digitalWrite(BUZZER_PIN, LOW); 
  
  request->send_P(200, "text/plain", "Lockdown Stopped Successfully");
}


void setup() {
  
  pinMode(BUZZER_PIN, OUTPUT); 

  Serial.begin(115200);
  
  delay(1000);
  Serial.println("Connecting to WiFi....");

  WiFi.begin(ssid, pass);
  
  while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  
  Serial.print("Hostname: ");
  Serial.println(ssid);
  Serial.print("Password: ");
  Serial.println(pass);
  Serial.print("URL: ");
  Serial.print(WiFi.localIP());
  Serial.println(":8080/");

  Serial.println();

  // Mapping the temp route
  server.on("/InitLockdown", HTTP_GET, InitLockdown);
  
  server.on("/StopLockdown", HTTP_GET, StopLockdown);
  
  
  // Just for test purpose
  server.on("/test", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", "Hello From, Nile !!");
  });

  server.begin();
}

void loop(){

}