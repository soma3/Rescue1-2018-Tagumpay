#include <motor.h>

Motor left(5,6), right(10,9); 
void setup() {
    Serial.begin(9600);
}

int counter = 0;

void loop() {
  // put your main code here, to run repeatedly:  
   counter = pwmove(right,left, 140, 0,counter);
   Serial.println(counter);

}
    
