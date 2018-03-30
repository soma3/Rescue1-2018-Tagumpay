#include <motor.h>

Motor left(5,6), right(9,10); 
void setup() {

}

void loop() {
  // put your main code here, to run repeatedly:
    move(right,left,200);
    delay(2000);
    brake(right,left);
    delay(2000);
    
}
    
