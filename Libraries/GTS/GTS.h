#ifndef GTS_h
#define GTS_h

#include "Arduino.h"
#include "motor.h"


class GTS
{
  public:
    void gyroturn(Motor right,Motor left,int nextpos, int speed);//added speed
    void gyrostraight(Motor right,Motor left,float _origin, int speed);//added speed
    void pid(float kp, float ki, float kd);
    void setup();
    float _integral;
    float _lasterror;
    float _cfac;
  private:
    int _currentpos;
    int _nextpos;
    int _adjust;
    float _origin;
    int _speed;
    float _setoff;
    float _derivative;
    float _correction;
    float _kp;
    float _ki;
    float _kd; 
};

#endif

