#ifndef motor
#define motor

#include <Arduino.h> 

class Motor
{
    public:
    Motor(int digitalpin, int analogpin);
    
    void drive(int speed);
    int pwmdrive(int speed, int _counter);
    
    void brake();
    int speedcheck(int _speed);
    
    int counter=0;
    int low_speed=30;
    int cycle=20;
    int scaling_constant=100;
    int min_speed = 40, max_speed = 255;

    private:
    
    int _digitalpin, _analogpin;
    
    void fwd(int speed);
    void rev(int speed);
    
};

//void minspeed(int _min_speed);
//void maxspeed(int _max_speed);

void move(Motor right, Motor left, int speed);
void move(Motor right, Motor left, int speed, int difference);
void brake(Motor right, Motor left);

void turnleft(Motor right, Motor left, int speed);
void turnright(Motor right, Motor left, int speed);
void turn(Motor right, Motor left, int speed);
//void pwmove(Motor right, Motor left, int speed, int difference);
int pwmove(Motor right, Motor left, int speed, int difference, int _counter);
void pwmturn(Motor right, Motor left, int speed);

#endif
