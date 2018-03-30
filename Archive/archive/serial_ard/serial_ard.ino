int incoming[2];
int in1 = 2;
int motorleft, motorright;
void setup() {

Serial.begin(9600);              //Starting serial communication
Serial.println('READY');
}

void loop() {
  if (Serial.available()) {
    for (int i = 0; i < 1; i++) {
      incoming[i] = Serial.read();
    }
    int correction = incoming[0];
    motorleft = motorleft + correction;
    motorright = motorright - correction;
   }
  } 

//void loop() {
//  while(!Serial.available()){}
//  while (Serial.available()) {
//  char data = Serial.read();
//  char victor[3];
//  if (data = '#') {
//    for (byte x = 0; x <= 2; x++){
//      victor[x] = data;
//    }
//  }
//  else {Serial.read();}    
//  
//  Serial.println(victor);
//  }}
