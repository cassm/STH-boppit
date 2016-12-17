#include <QueueArray.h>
#include <ESP8266WiFi.h>
#include<Wire.h>

const char* ssid     = "BopIt";
const char* password = "upVsg49hh0CjNo80";

const char* host = "192.168.4.1";

// create a queue of characters.
volatile QueueArray <char> queue;

WiFiClient client;

void buttonISR () {
    //Serial.println("Button pushed");
    queue.push('X');
}

void setup() {
  digitalWrite(2,HIGH);
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  pinMode(5, INPUT);
  attachInterrupt(5, buttonISR, RISING);

  // set the printer of the queue.
  queue.setPrinter (Serial);
  delay(100);
  
  Serial.println("Serial begins");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("WIFI OK");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("Connected to Wifi");
  digitalWrite(2,LOW);
}

long cntAccel=0,cntSend=0;

void loop() {
  cntSend++;
  cntAccel++;
  if(!client.connected())
  {
    client.connect(host,80);
  }
  if(cntSend==800)
  {
      while (!queue.isEmpty()) {
          const char val = queue.pop();
          Serial.println(val);
          client.print(val);
          client.flush();
      }
      cntSend=0;
  }
}
