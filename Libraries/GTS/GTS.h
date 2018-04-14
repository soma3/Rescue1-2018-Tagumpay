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
 float _kp = 5;
 float _ki;
 float _kd;
 int GTScounter = 0;
 unsigned long timenow;
 unsigned long starttime;

void gyroturn(Motor right,Motor left,int nextpos, MPU6050 gyro){
    while (0==0){
        _currentpos = ((int)gyro.ranger());
        _nextpos = nextpos ;
        _adjust = _nextpos - _currentpos;
        Serial.println(_currentpos);
//        Serial.println(_adjust);
        if (_adjust > threshold){
            if (_adjust <= 180){
//                left.drive(80);
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
            if (_adjust <= -180){
                //brake(right,left);
                //turnright(right,left,90);
                turnright(right,left,right.speedcheck(360+_adjust));
            }
        }
        else {
            brake(right, left);
            Serial.println("breaekr");
            break;
        }
    }//added speed
}
void gyrostraight(Motor right,Motor left,float _origin, int _speed, MPU6050 gyro){
    float _cfac = gyro.ranger();
    if (_cfac>180){
        _cfac = _cfac-360;
    }
    float _setoff = _cfac - _origin;
//    if (_setoff<-180){
//        _setoff = -_setoff-360;
//    }
//    else if (_setoff>180){
//        _setoff = _setoff - 360;
//    }
    Serial.println(_setoff);
//    Serial.println(_kp);
    float _integral = _integral + _setoff;
    float _derivative = _setoff - _lasterror;
    float _correction = (_kp*_setoff + _ki*_integral + _kd*_derivative)*2;
    GTScounter = pwmove(right, left, _speed, _correction, GTScounter);
   //move(right, left, _speed, _correction);
    
    _lasterror = _setoff ;
}//added speed

void gyrostraight(Motor right,Motor left,float _origin, int _speed, MPU6050 gyro, int duration){
    starttime = millis();
    while (millis()-starttime<duration){
        gyrostraight(right,left,_origin,_speed,gyro);
    }
}//not tested!!!!

void pid(float kp, float ki, float kd){
    float _kp = kp;
    float _ki = ki;
    float _kd = kd;
}
    //void gyrosetup(MPU6050 gyro);


#endif

