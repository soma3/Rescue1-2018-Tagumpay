#include <motor.h>
 
Motor left(6,5), right(9,10); 
int incoming[2];
int diff;
int avg;
int motorleft, motorright;
int counter = 0

void setup() {
Serial.begin(9600);
move(right,left,150,0);
delay(10000);
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
  avg = 37;
  diff = 0;
  counter = pwmove(right,left,avg,diff,counter);
    }
}
    

