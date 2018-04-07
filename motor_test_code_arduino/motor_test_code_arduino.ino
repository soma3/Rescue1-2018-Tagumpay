#include <motor.h>

Motor left(5,6), right(10,9); 
void setup() {
    Serial.begin(9600);
}

int counter = 0;

void loop() {
  //right.fwd(80);
  //left.fwd(50);
  // put your main code here, to run repeatedly:  
   //counter = pwmove(right,left, 180, 0,counter);
   Serial.println(counter);

}
    
