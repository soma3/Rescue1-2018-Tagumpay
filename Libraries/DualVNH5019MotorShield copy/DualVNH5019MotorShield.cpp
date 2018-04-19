#include "DualVNH5019MotorShield.h"

// Constructors ////////////////////////////////////////////////////////////////

DualVNH5019MotorShield::DualVNH5019MotorShield()
{
  //Pin map
//   _INA1 = 4;
//   _INB1 = 9;
//   _PWM1 = 6;
//   _EN1DIAG1 = 14;
//   _CS1 = A1;
//   _INA2 = 7;
//   _INB2 = 8;
//   _PWM2 = 5;
//   _EN2DIAG2 = 15;
//   _CS2 = A2;
    
   //orignal pins
   _INA1 = 4;
   _INB1 = 2;
   _PWM1 = 9;
   _EN1DIAG1 = 6;
   _CS1 = A0;
   _INA2 = 7;
   _INB2 = 8;
   _PWM2 = 10;
   _EN2DIAG2 = 12;
   _CS2 = A1;
}

DualVNH5019MotorShield::DualVNH5019MotorShield(unsigned char INA1,
                                               unsigned char INB1,
                                               unsigned char PWM1,
                                               unsigned char EN1DIAG1,
                                               unsigned char CS1,
                                               unsigned char INA2,
                                               unsigned char INB2,
                                               unsigned char PWM2,
                                               unsigned char EN2DIAG2,
                                               unsigned char CS2)
{
  _INA1 = INA1;
  _INB1 = INB1;
  _PWM1 = PWM1;
  _EN1DIAG1 = EN1DIAG1;
  _CS1 = CS1;
  _INA2 = INA2;
  _INB2 = INB2;
  _PWM2 = PWM2;
  _EN2DIAG2 = EN2DIAG2;
  _CS2 = CS2;
}

// Public Methods //////////////////////////////////////////////////////////////
void DualVNH5019MotorShield::init()
{
// Define pinMode for the pins and set the frequency for timer1.

  pinMode(_INA1,OUTPUT);
  pinMode(_INB1,OUTPUT);
  pinMode(_PWM1,OUTPUT);
  pinMode(_EN1DIAG1,INPUT);
  pinMode(_CS1,INPUT);
  pinMode(_INA2,OUTPUT);
  pinMode(_INB2,OUTPUT);
  pinMode(_PWM2,OUTPUT);
  pinMode(_EN2DIAG2,INPUT);
  pinMode(_CS2,INPUT);

  #ifdef DUALVNH5019MOTORSHIELD_TIMER1_AVAILABLE
    if (_PWM1 == _PWM1_TIMER1_PIN && _PWM2 == _PWM2_TIMER1_PIN)
    {
      // Timer 1 configuration
      // prescaler: clockI/O / 1
      // outputs enabled
      // phase-correct PWM
      // top of 400
      //
      // PWM frequency calculation
      // 16MHz / 1 (prescaler) / 2 (phase-correct) / 400 (top) = 20kHz
      TCCR1A = 0b10100000;
      TCCR1B = 0b00010001;
      ICR1 = 400;
    }
  #endif
}
// Set speed for motor 1, speed is a number betwenn -400 and 400
void DualVNH5019MotorShield::setM1Speed(int speed)
{
  unsigned char reverse = 0;

  if (speed < 0)
  {
    speed = -speed;  // Make speed a positive quantity
    reverse = 1;  // Preserve the direction
  }
  if (speed > 255)  // Max PWM dutycycle
    speed = 255;

  #ifdef DUALVNH5019MOTORSHIELD_TIMER1_AVAILABLE
    if (_PWM1 == _PWM1_TIMER1_PIN && _PWM2 == _PWM2_TIMER1_PIN)
    {
      OCR1A = speed;
    }
    else
    {
      analogWrite(_PWM1,speed); // map 400 to 255 - not anymore
    }
  #else
    analogWrite(_PWM1,speed); // map 400 to 255 - not anymore
  #endif

  if (speed == 0)
  {
    digitalWrite(_INA1,LOW);   // Make the motor coast no
    digitalWrite(_INB1,LOW);   // matter which direction it is spinning.
  }
  else if (reverse)
  {
    digitalWrite(_INA1,LOW);
    digitalWrite(_INB1,HIGH);
  }
  else
  {
    digitalWrite(_INA1,HIGH);
    digitalWrite(_INB1,LOW);
  }
}

// Set speed for motor 2, speed is a number betwenn -255 and 255
void DualVNH5019MotorShield::setM2Speed(int speed)
{
  unsigned char reverse = 0;

  if (speed < 0)
  {
    speed = -speed;  // make speed a positive quantity
    reverse = 1;  // preserve the direction
  }
  if (speed > 255)  // Max
    speed = 255;

  #ifdef DUALVNH5019MOTORSHIELD_TIMER1_AVAILABLE
    if (_PWM1 == _PWM1_TIMER1_PIN && _PWM2 == _PWM2_TIMER1_PIN)
    {
      Serial.print("line 147");
      OCR1B = speed;
    }
    else
    {
      analogWrite(_PWM2,speed); // map 400 to 255 - not anymore
      Serial.print("line 153");
    }
  #else
    analogWrite(_PWM2,speed); // map 400 to 255 - not anymore
      Serial.print("line 157");
  #endif

  if (speed == 0)
  {
    digitalWrite(_INA2,LOW);   // Make the motor coast no
    digitalWrite(_INB2,LOW);   // matter which direction it is spinning.
  }
  else if (reverse)
  {
    digitalWrite(_INA2,LOW);
    digitalWrite(_INB2,HIGH);
  }
  else
  {
    digitalWrite(_INA2,HIGH);
    digitalWrite(_INB2,LOW);
  }
}

// Set speed for motor 1 and 2
void DualVNH5019MotorShield::setSpeeds(int m1Speed, int m2Speed)
{
  setM1Speed(m1Speed);
  setM2Speed(m2Speed);
}

// Brake motor 1, brake is a number between 0 and 255
void DualVNH5019MotorShield::setM1Brake(int brake)
{
  // normalize brake
  if (brake < 0)
  {
    brake = -brake;
  }
  if (brake > 255)  // Max brake
    brake = 255;
  digitalWrite(_INA1, LOW);
  digitalWrite(_INB1, LOW);

  #ifdef DUALVNH5019MOTORSHIELD_TIMER1_AVAILABLE
    if (_PWM1 == _PWM1_TIMER1_PIN && _PWM2 == _PWM2_TIMER1_PIN)
    {
      OCR1A = brake;
    }
    else
    {
      analogWrite(_PWM1,brake); // map 400 to 255 - not anymore
    }
  #else
    analogWrite(_PWM1,brake); // map 400 to 255 -  not anymore
  #endif
}

// Brake motor 2, brake is a number between 0 and 255
void DualVNH5019MotorShield::setM2Brake(int brake)
{
  // normalize brake
  if (brake < 0)
  {
    brake = -brake;
  }
  if (brake > 255)  // Max brake
    brake = 255;
  digitalWrite(_INA2, LOW);
  digitalWrite(_INB2, LOW);

  #ifdef DUALVNH5019MOTORSHIELD_TIMER1_AVAILABLE
    if (_PWM1 == _PWM1_TIMER1_PIN && _PWM2 == _PWM2_TIMER1_PIN)
    {
      OCR1B = brake;
    }
    else
    {
      analogWrite(_PWM2,brake); // map 400 to 255 - not anymore
    }
  #else
    analogWrite(_PWM2,brake); // map 400 to 255 - not anymore
  #endif
}

// Brake motor 1 and 2, brake is a number between 0 and 255
void DualVNH5019MotorShield::setBrakes(int m1Brake, int m2Brake)
{
  setM1Brake(m1Brake);
  setM2Brake(m2Brake);
}

// Return motor 1 current value in milliamps.
unsigned int DualVNH5019MotorShield::getM1CurrentMilliamps()
{
  // 5V / 1024 ADC counts / 144 mV per A = 34 mA per count
  return analogRead(_CS1) * 34;
}

// Return motor 2 current value in milliamps.
unsigned int DualVNH5019MotorShield::getM2CurrentMilliamps()
{
  // 5V / 1024 ADC counts / 144 mV per A = 34 mA per count
  return analogRead(_CS2) * 34;
}

// Return error status for motor 1
unsigned char DualVNH5019MotorShield::getM1Fault()
{
  return !digitalRead(_EN1DIAG1);
}

// Return error status for motor 2
unsigned char DualVNH5019MotorShield::getM2Fault()
{
  return !digitalRead(_EN2DIAG2);
}

int DualVNH5019MotorShield::speedcheck(int _speed){
    int sign = 0;
    if (_speed>0) sign = 1;
    if (_speed<0) sign = -1;
    if (abs(_speed)<min_speed) return sign*min_speed;
    if (abs(_speed)>max_speed) return sign*max_speed;
    else return _speed;
}

void DualVNH5019MotorShield::move(int speed)
{   speed = speedcheck(speed);
    //    right.drive(speedcheck(speed));
    //    left.drive(speedcheck(speed));
    setSpeeds(speed, speed);
}

void DualVNH5019MotorShield::move(int speed, int difference)
{   int temp = difference/2;
    //    right.drive(speedcheck(speed+temp));
    //    left.drive(speedcheck(speed-temp));
    setSpeeds(speedcheck(speed+temp), speedcheck(speed-temp));
    
}

void DualVNH5019MotorShield::turnright(int speed)
{
    //    left.drive(speedcheck(speed));
    //    right.drive(-speedcheck(speed));
    setSpeeds(speedcheck(-speed), speedcheck(speed));
}

void DualVNH5019MotorShield::turnleft(int speed)
{
    setSpeeds(speedcheck(speed), speedcheck(-speed));
}

void DualVNH5019MotorShield::turn(int speed){
    if (speed>0){
        turnright(speed);
    }
    if (speed<0){
        turnleft(-speed);
    }
}

void DualVNH5019MotorShield::brake()
{  setM1Brake(400);
   setM2Brake(400);
    
}

int DualVNH5019MotorShield::M1pwmdrive(int speed, int _counter){
    counter = _counter;
    if (counter>cycle) counter = 0;
    if (counter == 0){
        if (speed==0) setM1Brake(400);
        setM1Speed(speed);
    }
    else{
        if (speed==0) setM1Brake(400);
        int lowspeed = speed*scaling_constant;
        setM1Speed(lowspeed);
    }
    counter = counter + 1;
    return counter;
}

int DualVNH5019MotorShield::M2pwmdrive(int speed, int _counter){
    counter = _counter;
    if (counter>cycle) counter = 0;
    if (counter == 0){
        if (speed==0) setM2Brake(400);
        setM2Speed(speed);
    }
    else{
        if (speed==0) setM2Brake(400);
        int lowspeed = speed*scaling_constant;
        setM2Speed(lowspeed);
    }
    counter = counter + 1;
    return counter;
}

int DualVNH5019MotorShield::pwmove(int speed, int difference, int _counter){
    int temp = difference/2;
    M1pwmdrive(speed+temp,_counter);
    M2pwmdrive(speed-temp,_counter);
    return counter;
}

void DualVNH5019MotorShield::pivotLEFTturn(int speed){
	setSpeeds(speedcheck(speed), 0);
}

void DualVNH5019MotorShield::pivotRIGHTturn(int speed){
	setSpeeds(0, speedcheck(speed));
}

