//#include <MPU6050_6Axis_MotionApps20.h>
#include <motor.h>
#include <Wire.h>
#include <VL53L0X.h>
#include <I2Cdev.h>
#include <GTS.h>


//MPU6050 gyro; 
GTS gts;
Motor left(5,6), right(10,9);
//float _integral = 0;
//float _lasterror = 0;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
//Wire.begin();
gts.setup();
//gyro.start(-52,93,-1,985);
}

void loop() {
  // put your main code here, to run repeatedly:
gts.pid(1,1,1);
Serial.println(gts._cfac);
gts.gyrostraight(right,left,0,100);
}
