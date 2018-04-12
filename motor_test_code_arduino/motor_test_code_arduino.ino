#include <motor.h>

Motor left(4,5), right(7,6); 
void setup() {
    Serial.begin(9600);

}

int counter = 0;

void loop() {
  // put your main code here, to run repeatedly:  
    Serial.println(counter); 
    if (counter==0) {
      move(right,left,140);
      counter++;
    }
    else {
      move(right, left, 20);
      counter++;
    }
    if (counter > 10){
    counter = 0;
    }
      
//    brake(right,left);
//    delay(2000);
//    move(right,left,-80,50);
//    delay(2000);
//    brake(right,left);
//    delay(2000);
//    move(right,left,80,-50);
//    delay(2000);
//    brake(right,left);
//    delay(2000);
//    turnleft(right,left,200);
//    delay(2000);
//    brake(right,left);
//    delay(2000);
//    turnright(right,left,200);
//    delay(2000);
//    brake(right,left);
//    delay(2000);

}
    
