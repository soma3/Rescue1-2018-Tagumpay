
#include <Arduino.h>
#include <motor.h>

Motor::Motor(int In1pin, int In2pin)
{
    In1 = In1pin;
    In2 = In2pin;
    
    pinMode(In1, OUTPUT);
    pinMode(In2, OUTPUT);
}

void minspeed(int _min_speed){
    _min_speed = min_speed;
}

void maxspeed(int _max_speed){
    _max_speed = max_speed;
}

int speedcheck(int _speed){
    if (_speed<min_speed) return min_speed;
    if (_speed>max_speed) return max_speed;
}

void Motor::fwd(int speed)
{
    analogWrite(In1, speed);
    analogWrite(In2, 0);
}

void Motor::rev(int speed)
{
    analogWrite(In1, 0);
    analogWrite(In2, speed);
}

void Motor::brake()
{
    analogWrite(In1, 0);
    analogWrite(In2, 0);
}

void Motor::drive(int speed)
{
    if (speed==0) brake();
    if (speed>0) fwd(speedcheck(speed));
    if (speed<0) rev(-speedcheck(speed));
}

void move(Motor right, Motor left, int speed)
{
    right.drive(speedcheck(speed));
    left.drive(speedcheck(speed));
}

void move(Motor right, Motor left, int speed, int difference)
{   int temp = difference/2;
    right.drive(speedcheck(speed+temp));
    left.drive(speedcheck(speed-temp));
}

void turnright(Motor right, Motor left, int speed)
{
    left.drive(speedcheck(speed));
    right.drive(-speedcheck(speed));
}

void turnleft(Motor right, Motor left, int speed)
{
    left.drive(-speedcheck(speed));
    right.drive(speedcheck(speed));
}

void brake(Motor right, Motor left)
{
    right.brake();
    left.brake();
}










