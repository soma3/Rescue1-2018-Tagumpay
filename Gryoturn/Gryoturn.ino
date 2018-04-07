#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "motor.h"
#include "math.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include "Wire.h"
#endif
MPU6050 mpu;
#define OUTPUT_READABLE_EULER
#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;/////./≥≥≥≥≥/≥≥≥……………………≥;
//test test test
// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

Motor left(5,6), right(10,9); 
// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

float hyaabs(float aaa){
  if(aaa < 0) {
    return -1*aaa;
  }
  else{
    return aaa;
  }
}

// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    delay(10000);
//    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
//        Wire.begin();
//        TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz)
//    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
//        Fastwire::setup(400, true);
//    #endif
//
//    // initialize serial communication
//    // (115200 chosen because it is required for Teapot Demo output, but it's
//    // really up to you depending on your project)
//    Serial.begin(115200);
//    while (!Serial); // wait for Leonardo enumeration, others continue immediately
//
//   mpu.initialize();
//
//    
//   devStatus = mpu.dmpInitialize();
//
//    // supply your own gyro offsets here, scaled for min sensitivity
//    mpu.setXGyroOffset(-52);
//    mpu.setYGyroOffset(93);
//    mpu.setZGyroOffset(-1);
//    mpu.setZAccelOffset(985); // 1688 factory default for my test chip
//
//    // make sure it worked (returns 0 if so)
//    if (devStatus == 0) {
//
//        mpu.setDMPEnabled(true);
//
//        
//        attachInterrupt(0, dmpDataReady, RISING);
//        mpuIntStatus = mpu.getIntStatus();
//
//        // set our DMP Ready flag so the main loop() function knows it's okay to use it
//        Serial.println(F("DMP ready! Waiting for first interrupt..."));
//        dmpReady = true;
//
//        // get expected DMP packet size for later comparison
//        packetSize = mpu.dmpGetFIFOPacketSize();
//    } else {
//        // ERROR!
//        // 1 = initial memory load failed
//        // 2 = DMP configuration updates failed
//        // (if it's going to break, usually the code will be 1)
//        Serial.print(F("DMP Initialization failed (code "));
//        Serial.print(devStatus);
//        Serial.println(F(")"));
//    }
Wire.begin();
    TWBR = 24;
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);

  mpu.start(-52,93,-1,985);
    // configure LED for output
    pinMode(LED_PIN, OUTPUT);
}

// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {
//  move(right,left,100);
//  delay(2000);
//  turnright(right,left,200);
//  delay(2000);
//  turnleft(right,left,200);
//  delay(2000);
//needs variable to define next position(nextpos)
int angle = ((int)mpu.getangle() + 7200)%360;
int currentpos = angle;
int nextpos = 180;
int adjust = nextpos - currentpos;
  if (adjust > 0){
    if (adjust < 180){
      turnright(right,left,70);
    }
    if (adjust > 180){
      turnleft(right,left,70);
    }
    else {
    }
  }
  if (adjust < 0){
    if (adjust > -180){
      turnleft(right,left,70);
    }
    if (adjust < -180){
      turnright(right,left,70);
    }
    else {
    }
  }
  else {
  }
  
Serial.println(angle);
Serial.print("; ");
Serial.println(adjust);
//  if (currentpos >= 0){
//    if (nextpos >= 0){
//      if (adjust > 0){
//        turnright(right,left,70); 
//      }
//      if (adjust == 0){
//      }
//      else {
//        turnleft(right,left,70);
//        
//      }
//    }
//    else {
//      if (hyaabs(adjust) > 180 ){
//        turnright(right,left,70);
//      }
//      if (hyaabs(adjust) == 0){  
//      }
//      else {
//        turnleft(right,left,70);
//         
//      }
//    }
//  }  
//  else {
//    if (nextpos >= 0){
//      if (hyaabs(adjust) > 180){
//        turnleft(right,left,70);
//      }
//      if (hyaabs(adjust) == 0){
//      }
//      else {
//        turnright(right,left,70);
//      }}
//    else {
//      if (adjust > 0){
//        turnright(right,left,70);
//      }
//      if (adjust == 0){
//      }
//      else {
//        turnleft(right,left,70);
//      }
//    }
//  }
//gyrocentre



 //gyroturn
}
