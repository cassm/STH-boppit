#include <easyMesh.h>

#define   LED             2       // GPIO number of connected LED

#define   MESH_PREFIX     "BopIt"
#define   MESH_PASSWORD   "upVsg49hh0CjNo80"
#define   MESH_PORT       5555

easyMesh  mesh;

uint32_t sendMessageTime = 0;
int ledState = 0;
String msg = "";
char msgChar = 'a';
long unsigned int lastDebounceTime = 0;
int minDebounceInterval = 20;

void buttonISR () {
  if (millis() < lastDebounceTime + minDebounceInterval) {
    return;
  }
  lastDebounceTime = millis();
  msg += msgChar++;
  if (msgChar == 'z') {
    msgChar = 'a';
  }
}
void setup() {
  Serial.begin(115200);
    
  pinMode( LED, OUTPUT );
  digitalWrite( LED, HIGH);

//mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | STARTUP );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.setReceiveCallback( &receivedCallback );
  mesh.setNewConnectionCallback( &newConnectionCallback );
  attachInterrupt(5, buttonISR, RISING);

  randomSeed( analogRead( A0 ) );
}


void loop() {
  mesh.update();

  // if the time is ripe, send everyone a message!
  if ( msg.length() != 0 ){
    Serial.println(msg);
    mesh.sendBroadcast( msg );
    msg = "";
  }
}

void receivedCallback( uint32_t from, String &msg ) {
  digitalWrite( LED, ledState++%2);
  Serial.print(msg);
}

void newConnectionCallback( bool adopt ) {
  Serial.printf("startHere: New Connection, adopt=%d\n", adopt);
  digitalWrite( LED, LOW);
}
