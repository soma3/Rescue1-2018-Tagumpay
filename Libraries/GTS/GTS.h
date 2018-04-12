#ifndef GTS_h
#define GTS_h

#include "Arduino.h"
#include <motor.h>
#include <MPU6050_6Axis_MotionApps20.h>

// MPU6050 gyro;

 float _integral ;
 float _lasterror ;
 float _cfac;
//float _cfac = 0;
 int _currentpos;
 int _nextpos;
 int _adjust;
 int threshold = 2;
 float _setoff;
 float _derivative;
 float _correction;
 float _kp;
 float _ki;
 float _kd;

void gyroturn(Motor right,Motor left,int nextpos, MPU6050 gyro){
    while (0==0){
        int _currentpos = ((int)gyro.ranger());
        int _nextpos = nextpos ;
        int _adjust = _nextpos - _currentpos;
        Serial.println(_currentpos);
        Serial.println(_adjust);
        if (_adjust > threshold){
            if (_adjust < 180){
                left.drive(80);
                //turnright(right,left,90);
                turnright(right,left,right.speedcheck(_adjust));
            }
            if (_adjust > 180){
                //right.drive(80);
                //brake(right,left);
                //turnleft(right,left,90);
                turnleft(right,left,left.speedcheck(360-_adjust));
            }
        }
        else if (_adjust < -threshold){
            if (_adjust > -180){
                //brake(right,left);
                //turnleft(right,left,90);
                turnleft(right,left,left.speedcheck(-_adjust));
            }
            if (_adjust < -180){
                //brake(right,left);
                //turnright(right,left,90);
                turnright(right,left,right.speedcheck(360+_adjust));
            }
        }
        else {
            brake(right, left);
            Serial.println("breaekr");
            //break;
        }
    }//added speed
}
void gyrostraight(Motor right,Motor left,float _origin, int _speed, MPU6050 gyro){
    float _cfac = gyro.getangle();
    float _setoff = _origin - _cfac;
    Serial.println(_cfac);
    float _integral = _integral + _setoff;
    float _derivative = _setoff - _lasterror;
    float _correction = (_kp*_setoff + _ki*_integral + _kd*_derivative)*2;
    
    move(right, left, _speed, _correction);
    
    _lasterror = _setoff ;
}//added speed
void pid(float kp, float ki, float kd){
    float _kp = kp;
    float _ki = ki;
    float _kd = kd ;
}
    //void gyrosetup(MPU6050 gyro);


#endif

