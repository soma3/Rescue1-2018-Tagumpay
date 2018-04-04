#include <motor.h>

#include <Wire.h>

#include <VL53L0X.h>

#include <helper_3dmath.h>
#include <MPU6050_6Axis_MotionApps20.h>

#include <I2Cdev.h>

MPU6050 gyro;
Motor left(6,5), right(9,10);
float origin = 0;
float integral = 0;
float lasterror = 0;
float kp = 1;
float ki = 1;
float kd = 1;

int speed = 50;

void setup() {
      Wire.begin();
      gyro.start(-53,-1,96,988);
}
void loop() {
// accepts float origin                
      float angle = gyro.getangle();
      float cfac = angle;
      float setoff = origin - cfac;
    
      float integral = integral + setoff;        
      float derivative = setoff - lasterror;
      float correction = (kp*setoff + ki*integral + kd*derivative)*2;

      move(right, left, speed, correction);
         
      lasterror = setoff;
}

