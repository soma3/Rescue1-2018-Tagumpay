#include <GTS.h>
#include <motor.h>
#include <Wire.h>
#include <VL53L0X.h>
#include <helper_3dmath.h>
#include <MPU6050_6Axis_MotionApps20.h>
#include <I2Cdev.h>

void GTS::gyroturn(int nextpos)
{
  void loop() {
    int _currentpos = ((int)mpu.getangle() + 7200)%360;
    int _nextpos = nextpos
    int _adjust = _nextpos - _currentpos;
      if (_adjust > 0){
        if (_adjust < 180){
          turnright(right,left,70);
        }
        if (_adjust > 180){
          turnleft(right,left,70);
        }
        else {
        }
      }
      if (_adjust < 0){
        if (_adjust > -180){
          turnleft(right,left,70);
        }
        if (_adjust < -180){
          turnright(right,left,70);
        }
        else {
        }
      }
      else {
      }
  }
}

void GTS::gyrostraight(float _origin)
{
 MPU6050 gyro;
 float _integral = 0;
 float _lasterror = 0;

 int _speed = 50;
 void setup() {
  move(right,left,255);
  delay(2000);
  Wire.begin();
  gyro.start(-52,93,-1,985);
 }
 void loop() {
  float _cfac = gyro.getangle();
  float _setoff = _origin - _cfac;

  float _integral = _integral + _setoff;
  float _derivative = _setoff - _lasterror;
  float _correction = (_kp*_setoff + _ki*_integral + _kd*_derivative)*2;

  move(right, left, _speed, correction);

  _lasterror = _setoff  
 }
}

GTS::pid(float kp, float ki, float kd)
{
 float _kp = kp
 float _ki = ki
 float _kd = kd 
}
