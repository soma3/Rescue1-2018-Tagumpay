#ifndef motor
#define motor

#include <Arduino.h> 

class Motor
{
    public:
    Motor(int In1pin, int In2pin);
    
    void drive(int speed);
    
    void brake();
    
    int counter=0;
    int low_speed=20;
    int cycle=10;

    private:
    
    int In1, In2;
    
    void fwd(int speed);
    void rev(int speed);
    
};

//int min_speed = 20, max_speed = 255;

//void minspeed(int _min_speed);
//void maxspeed(int _max_speed);
int speedcheck(int _speed);

void move(Motor right, Motor left, int speed);
void move(Motor right, Motor left, int speed, int difference);
void brake(Motor right, Motor left);

void turnleft(Motor right, Motor left, int speed);
void turnright(Motor right, Motor left, int speed);
void pwmove(Motor right, Motor left, int speed, int difference);
void pwmturn(Motor right, Motor left, int speed);

#endif
