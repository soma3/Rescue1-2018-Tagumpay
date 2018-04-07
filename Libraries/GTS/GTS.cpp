#include <GTS.h>
#include <motor.h>
#include <Wire.h>
#include <VL53L0X.h>
// #include <helper_3dmath.h>
#include <MPU6050_6Axis_MotionApps20.h>
#include <I2Cdev.h>
MPU6050 gyro;


// void GTS::gyroturn(Motor right, Motor left, int nextpos,int speed)//added speed
// { 
//   while (0==0){ 
//     int _currentpos = ((int)gyro.getangle() + 7200)%360;
//     int _nextpos = nextpos ;
//     int _adjust = _nextpos - _currentpos;
//       if (_adjust > 0){
//         if (_adjust < 180){
//           turnright(right,left,speed);
//         }
//         if (_adjust > 180){
//           turnleft(right,left,speed);
//         }
//         else {
//         }
//       }
//       if (_adjust < 0){
//         if (_adjust > -180){
//           turnleft(right,left,speed);
//         }
//         if (_adjust < -180){
//           turnright(right,left,speed);
//         }
//         else {
//         }
//       }
//       else {
//       }
//    }
// }

void GTS::gyrostraight(Motor right,Motor left,float _origin, int speed)//added speed
{
 float _integral = 0;
float _lasterror = 0;

  int _speed = speed;
  float _cfac = gyro.getangle();
  float _setoff = _origin - _cfac;

  _integral = _integral + _setoff;
  float _derivative = _setoff - _lasterror;
  float _correction = (_kp*_setoff + _ki*_integral + _kd*_derivative)*2;

  move(right, left, _speed, _correction);

  _lasterror = _setoff ; 
}

void GTS::pid(float kp, float ki, float kd)
{
 float _kp = kp;
 float _ki = ki;
 float _kd = kd ;
}

void GTS::setup()
{
Wire.begin();
gyro.start(-52,93,-1,985);
}


