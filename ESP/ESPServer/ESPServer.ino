#include <easyMesh.h>

#define   LED             2       // GPIO number of connected LED

#define   MESH_PREFIX     "BopIt"
#define   MESH_PASSWORD   "upVsg49hh0CjNo80"
#define   MESH_PORT       5555

easyMesh  mesh;
int ledState = 0;

void setup() {
  Serial.begin(115200);
    
  pinMode( LED, OUTPUT );
  digitalWrite( LED, HIGH);

//mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | STARTUP );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.setReceiveCallback( &receivedCallback );
  mesh.setNewConnectionCallback( &newConnectionCallback );

  randomSeed( analogRead( A0 ) );
}


void loop() {
  mesh.update();
}

void receivedCallback( uint32_t from, String &msg ) {
  Serial.print(msg);
  
  digitalWrite( LED, ledState++%2);
}

void newConnectionCallback( bool adopt ) {
  Serial.printf("startHere: New Connection, adopt=%d\n", adopt);
  digitalWrite( LED, LOW);
}
