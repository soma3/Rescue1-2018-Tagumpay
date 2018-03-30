//motor speeds
int speed = 0;
int maxSpeed = 200; // max is 250
int speedRight = 0;
int speedLeft = 0;

//pins for Motors (dont actually know what pin is for what yet)
int pinIN1 = 2; //right forward
int pinIN2 = 3; //right
int pinIN3 = 4; //left forward
int pinIN4 = 5; //left


//for PID
float kp = 0.8; //need to tune
float ki = 0;
float kd = 0;
float baseSpeed = 100; // curently no idea what speed
int threshold = 0; //need to tune 
int midLine = 85;
int speedDiff = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);
  pinMode(pinIN3, OUTPUT);
  pinMode(pinIN4, OUTPUT);

}

void setSpeed(float _speed)
{
  speed = _speed;
}

//all the motor controls


  void driveRight(int speedRight) {
    if (speedRight >= 0)
    {
      analogWrite(pinIN1, speedRight);
      analogWrite(pinIN2, 0);
    }
    else
    {
      analogWrite(pinIN1, 0);
      analogWrite(pinIN2, speedRight);
    }
  }

  void driveLeft(int speedLeft) {
    if (speedLeft >= 0)
    {
      analogWrite(pinIN3, speedLeft);
      analogWrite(pinIN4, 0);
    }
    else
    {
      analogWrite(pinIN3, 0);
      analogWrite(pinIN4, speedLeft);
    }
  }

  void driveStraight(int speed)
  {
    driveLeft(speed);
    driveRight(speed);
  }

  void driveBackwards(int speed)
  {
    driveLeft(-speed);
    driveRight(-speed);
  }

  void turnRight(int speed)
  {
    driveLeft(speed);
    driveRight(-speed);
  }

  void turnLeft(int speed)
  {
    driveRight(speed);
    driveLeft(-speed);
  }


int getPosition() {
  if (Serial.available()) 
  {
    return Serial.read();
  }
}

//PID
void PID_linetrack()
{
  double now, backthen = 0;
  double error, previousError = 0;
  double proportional, integral = 0, derivative;
  double MAXintegral = 100000;//random value
  while (true)
  {
    //error = (kp/10 * proportional) + (ki/10 * integral) + (kd/10 * derivative);
    now = getPosition() - threshold;
    proportional = now;     
    //currently if the bot is too much to the right cx>120,
    //if too much to the left its cx <= 50 and if its just right cx<120 and cx>50
    derivative = now - backthen;
    integral += proportional;

    if (integral>MAXintegral) integral = MAXintegral;
    if (abs(now) <5) integral = 0;
    backthen = now;


    error = getPosition() - midLine;
    speedDiff = error*kp + derivative *kd + integral *ki;
    speedRight = baseSpeed + speedDiff;
    speedLeft = baseSpeed - speedDiff;


    if (speedRight > maxSpeed) speedRight = maxSpeed;
    if (speedLeft > maxSpeed) speedLeft = maxSpeed;
    if (speedRight <0) speedRight = 0;
    if (speedLeft <0) speedLeft = 0;

    driveRight(speedRight);
    driveLeft(speedLeft);
  }

}

void loop()
{
  /* add main program code here */
  Serial.print(getPosition());
  delay(500);
}



