#include <motor.h>
int counter = 0;
Motor left(7,6), right(4,5); 
void setup() {
    Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:  
//    Serial.println(counter); 
//    if (counter==0) {
//      move(right,left,140);
//      counter++;
//    }
//    else {
//      move(right, left, 20);
//      counter++;
//    }
//    if (counter > 10){
//    counter = 0;
//    }
      
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

counter = pwmove(right,left,255,0,counter);
 
}
    
