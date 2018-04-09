#include <motor.h>
 
Motor left(6,5), right(9,10); 
int incoming[2];
int diff;
int avg;
int motorleft, motorright;

void setup() {
Serial.begin(9600);
}

void loop() {
  while (Serial.available()){
    for(int i=0;i<2;i++){
      int miao = Serial.read();
      if (miao > 127){
        miao = miao - 256;
      }
      incoming[i] = 2*miao;
  }
  diff = incoming[1]-incoming[0];
  avg = (incoming[1]+incoming[0])/2;
  move(right,left,avg,diff);
    }
}

//GERALD CHOO HAS ISSUES 
    

