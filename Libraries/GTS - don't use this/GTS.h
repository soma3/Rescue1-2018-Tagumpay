#ifndef GTS_h
#define GTS_h

#include "Arduino.h"
#include <motor.h>
#include <MPU6050_6Axis_MotionApps20.h>
//MPU6050 gyro;


extern float _integral ;
extern float _lasterror ;
extern float _cfac;
extern int _currentpos;
extern int _nextpos;
extern int _adjust;
extern float _setoff;
extern float _derivative;
extern float _correction;
extern float _kp;
extern float _ki;
extern float _kd; 

	void gyroturn(Motor right,Motor left,int nextpos, int speed, MPU6050 gyro);//added speed
    void gyrostraight(Motor right,Motor left,float _origin, int _speed, MPU6050 gyro);//added speed
    void pid(float kp, float ki, float kd);
    void gyrosetup(MPU6050 gyro);


#endif

