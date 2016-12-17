#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <WiFiServer.h>

const char *ssid = "BopIt";
const char *password = "upVsg49hh0CjNo80";

WiFiServer server(80);

void setup() {
    Serial.begin(115200);
    pinMode(2, OUTPUT);
    digitalWrite(2,HIGH);
    WiFi.softAP(ssid, password);

    IPAddress myIP = WiFi.softAPIP();
    Serial.print("Server IP = ");
    Serial.println(myIP);
    server.begin();
}

void loop() {
    WiFiClient client = server.available();
  
    if (client) {
        digitalWrite(2,LOW);
        Serial.println("Client connected.");
    
        while (client.connected()) {
            while (client.available()) {
                char command = client.read();
                Serial.println(command);
            }
        }
        Serial.println("Client disconnected.");
        client.stop();
        digitalWrite(2,HIGH);
    }
}

     
        /*while(!client.available())
        {
            delay(1);
        }
        Serial.println("Client available");
        String s=client.read('X');
        if(s.length()!=0)
        {
            Serial.println("Nonzero length message");
            Serial.println(s);
        }
        else
        {
            Serial.println("Zero length message");
        }
        client.flush();
    }
}*/
