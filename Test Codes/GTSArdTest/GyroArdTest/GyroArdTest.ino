#include <MPU6050_6Axis_MotionApps20.h>
#include <motor.h>
#include <Wire.h>
#include <GTS.h>


MPU6050 gyro; 
Motor left(5,6), right(10,9);

void setup() {
Serial.begin(9600);
gyrosetup(gyro);
pid(1.,1.,1.);
}

void loop() {
  // put your main code here, to run repeatedly:
//gyroturn(right, left, 50, 50, gyro);
gyrostraight(right,left,0,100,gyro);
}
