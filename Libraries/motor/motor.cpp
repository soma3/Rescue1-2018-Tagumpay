
#include <Arduino.h>
#include <motor.h>

Motor::Motor(int digitalpin, int analogpin)
{
    _digitalpin = digitalpin;
    _analogpin = analogpin;
    
    pinMode(_digitalpin, OUTPUT);
    pinMode(_analogpin, OUTPUT);
}

//void minspeed(int _min_speed){
//    min_speed = _min_speed;
//}
//
//void maxspeed(int _max_speed){
//    max_speed = _max_speed;
//}

int Motor::speedcheck(int _speed){
    int sign = 0;
    if (_speed>0) sign = 1;
    if (_speed<0) sign = -1;
    if (abs(_speed)<min_speed) return sign*min_speed;
    if (abs(_speed)>max_speed) return sign*max_speed;
    else return _speed;
}

void Motor::fwd(int speed)
{
    digitalWrite(_digitalpin, LOW);
    analogWrite(_analogpin, speed);
}

void Motor::rev(int speed)
{
    digitalWrite(_digitalpin, HIGH);
    analogWrite(_analogpin, (255-speed));
}

void Motor::brake()
{
    digitalWrite(_digitalpin, LOW);
    analogWrite(_analogpin, 0);
}

void Motor::drive(int speed)
{
    if (speed==0) brake();
//    if (speed>0) fwd(speedcheck(speed));
//    if (speed<0) rev(-speedcheck(speed));
    if (speed>0) fwd(speed);
    if (speed<0) rev(-speed);
}

void move(Motor right, Motor left, int speed)
{
//    right.drive(speedcheck(speed));
//    left.drive(speedcheck(speed));
    right.drive(speed);
    left.drive(speed);
}

void move(Motor right, Motor left, int speed, int difference)
{   int temp = difference/2;
//    right.drive(speedcheck(speed+temp));
//    left.drive(speedcheck(speed-temp));
    right.drive(speed+temp);
    left.drive(speed-temp);

}

void turnright(Motor right, Motor left, int speed)
{
//    left.drive(speedcheck(speed));
//    right.drive(-speedcheck(speed));
    left.drive(speed);
    right.drive(-speed);
}

void turnleft(Motor right, Motor left, int speed)
{
//    left.drive(-speedcheck(speed));
//    right.drive(speedcheck(speed));
    left.drive(-speed);
    right.drive(speed);
}

void turn(Motor right, Motor left, int speed){
    if (speed>0){
        turnright(right,left,speed);
    }
    if (speed<0){
        turnleft(right,left,-speed);
    }
}

void brake(Motor right, Motor left)
{
    right.brake();
    left.brake();
}

//void pwmove(Motor right, Motor left, int speed, int difference, int counter){
//    if (right.counter>right.cycle) right.counter = 0;
//    if (right.counter==0){
//        move(right,left,speed,difference);
//    }
//    else{
//        move(right,left,right.low_speed);
//    }
//    right.counter++;
//}
//
//void pwmturn(Motor right, Motor left, int speed){
//    pwmove(right,left,0,2*speed);
//}


int Motor::pwmdrive(int speed, int _counter){
    counter = _counter;
    if (counter>cycle) counter = 0;
    if (counter == 0){
        if (speed==0) brake();
        if (speed>0) fwd(speed);
        if (speed<0) rev(-speed);//rev() takes in positive speed
    }
    else{
        if (speed==0) brake();
        if (speed>0) fwd((speed/scaling_constant)*low_speed);
        if (speed<0) rev((-speed/scaling_constant)*low_speed);//rev() is taking in positive speed
    }
    counter = counter + 1;
    return counter;
}

int pwmove(Motor right, Motor left, int speed, int difference, int _counter){
    int temp = difference/2;
    right.pwmdrive(speed+temp,_counter);
    left.pwmdrive(speed-temp,_counter);
    return right.counter;
}









