#include <MPU6050_6Axis_MotionApps20.h>
#include <motor.h>
#include <I2Cdev.h>
#include <GTS.h>


MPU6050 gyro; 
Motor left(4,5), right(7,6);

void setup() {
Wire.begin();  
//gyrosetup(gyro);
gyro.start(-52,93,-1,985);
//pid(1.,1.,1.);
Serial.begin(9600);
delay(5000);
Serial.println(gyro.getangle());
Serial.println(gyro.ranger());
gyro.scamreset();
Serial.println(gyro.getangle());
Serial.println(gyro.ranger());
Serial.println("sjgdiagjasjdojoh");
delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:

//12.4.18
Serial.println("Start");
gyroturn(right, left, 50, gyro);
//Serial.println(gyro.ranger());
//Serial.println(_currentpos);
//Serial.println(_adjust);
//Serial.println("next");
//end


//
//Serial.println(gyro.getangle());
//gyrostraight(right,left,0,80,gyro);
//speedcheck() works :>
}
