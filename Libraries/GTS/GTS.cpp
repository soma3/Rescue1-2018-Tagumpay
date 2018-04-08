#include "Arduino.h"
#include <GTS.h>

float _integral;
float _lasterror;
float _kp;
float _ki;
float _kd; 


void pid(float kp, float ki, float kd)
{
 float _kp = kp;
 float _ki = ki;
 float _kd = kd ;
}

void gyrosetup(MPU6050 gyro)
{
gyro.start(-52,93,-1,985);
}

void gyroturn(Motor right, Motor left, int nextpos,int speed, MPU6050 gyro) //added speed
{ 
  while (0==0){ 
    int _currentpos = ((int)gyro.getangle() + 7200)%360;
    int _nextpos = nextpos ;
    int _adjust = _nextpos - _currentpos;
      if (_adjust > 0){
        if (_adjust < 180){
          turnright(right,left,speed);
        }
        if (_adjust > 180){
          turnleft(right,left,speed);
        }
        else {
        }
      }
      if (_adjust < 0){
        if (_adjust > -180){
          turnleft(right,left,speed);
        }
        if (_adjust < -180){
          turnright(right,left,speed);
        }
        else {
        }
      }
      else {
      }
   }
}

void gyrostraight(Motor right, Motor left, float _origin, int _speed, MPU6050 gyro)//added speed
{

  float _cfac = gyro.getangle();
  float _setoff = _origin - _cfac;

  float _integral = _integral + _setoff;
  float _derivative = _setoff - _lasterror;
  float _correction = (_kp*_setoff + _ki*_integral + _kd*_derivative)*2;

  move(right, left, _speed, _correction);

  _lasterror = _setoff ; 
}



