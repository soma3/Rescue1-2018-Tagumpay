#ifndef GTS_h
#define GTS_h

#include "Arduino.h"

class GTS
{
  public:
    void gyroturn(int nextpos);
    void gyrostraight(float _origin);
    pid(float kp, float ki, float kd);
    float _integral
  private:
    int _currentpos;
    int _nextpos;
    int _adjust;
    float _origin;
    float _integral;
    float _lasterror;
    int _speed;
    float _cfac;
    float _setoff;
    float _derivative;
    float _correction;
    float _kp;
    float _ki;
    float _kd;
};

#endif
