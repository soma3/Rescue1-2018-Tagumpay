#ifndef RescueZone_h
#define RescueZone_h

#include "Arduino.h"
// #include <motor.h>
#include "DualVNH5019MotorShield.h"
#include <GTS.h>
#include <MPU6050_6Axis_MotionApps20.h>
#include <Servo.h>

//MPU6050 gyro;

/*
functions to add in other libraries:
DualVNH5019MotorShield pivotLEFTturn, pivotRIGHTturn
GTS gyropivotLEFTturn, gyropivotRIGHTturn
*/

int EvacZone = 0; //1 if detected
int EvacZonePos = 0;
int DetectionThreshold = 16;//80%
//wall angles?
int 
//servo angles
int Ground = 0;//?
int Standby = 120;//?
int Release = 180;//?

int DetectEvacZone(){
	Serial.write(1);//ask raspi to start detecting
	while(!Serial.available());
	int bleb = (int)Serial.read();
	EvacZone = bleb;
	return EvacZone;
} 

void FaceTheWall(int wall, DualVNH5019MotorShield motors, MPU6050 gyro){
	switch(wall){
		case 1:
			gyroturn(motors,90,gyro);
			break;
		case 2:
			gyroturn(motors,0,gyro);
			break;
		case 3:
			gyroturn(motors,270,gyro);
			break;
		case 4:
			gyroturn(motors,180,gyro);
			break;
	}
}//might need some pivot turns before using this

void ClearView(Servo servo){
	servo.write(Ground);
	delay(1000);
	servo.write(Standby);
	delay(1000);
}//and hopefully captures balls

void Initialise(DualVNH5019MotorShield motors, MPU6050 gyro, Servo servo){
	gyro.scamreset();//might need to align with something before that
	ClearView(servo);
	int counter = 0;
	int frequency = 0;
	while (counter<20){
		if (DetectEvacZone() == 1) frequency ++; //increments when rectangle is detected
		if (frequency>DetectionThreshold){
			EvacZonePos = 2; //evaczone is in corner 2
			break;
		}
		counter++;
	}//facing corner 2
	gyropivotLEFTturn(motors,90,gyro);
	FaceTheWall(3, motors, gyro);//if gyro screws up too much might consider just pivot right turn to 270
	ClearView(servo);
	if (EvacZonePos == 0){
		counter = 0;
		frequency = 0;
		while (counter<20){
			if (DetectEvacZone() == 1) frequency ++; //increments when rectangle is detected
			if (frequency>DetectionThreshold){
				EvacZonePos = 4; //evaczone is in corner 4
				break;
			}
		counter++;
		}//facing corner 4
	}
	if (EvacZonePos == 0){//if evaczone not detected after checking corners 2,4 it in corner 3
		EvacZonePos = 3;
	}
	motors.move(-20);//go against wall 1 backwards
	delay(2000);//arbitrary delay time
	gyro.start();//DEFINITELY WRONG VALUES
	delay(5000);//for the values to stabilise
	gyro.scamresetto(270);//wall 3 is now 270
}

void TheSweep(DualVNH5019MotorShield motors, MPU6050 gyro, Servo servo){
// 		auahshaagshjakakaksjdhjskajshshd;
}
/* logics?
	start with 2 directions, 0 or 270.
	since robot faces wall 3 at the end of initialisation, go against wall 3 if no evaczone at corner 4.
	??? or can just trace the wall, motors on one side moves slightly faster than the other; at evac zone it should just align
	
*/

#endif

/*
layout of rescue zone?
			_________________________________
			|#3		    <-wall 2->		  #2|			
			|								|
			|				0				|
  <-wall 3->|		    270 + 90			|<-wall 1->		
			|			   180				|
			|								|
			|#4         <-wall 4->          |
			|-----------------------<-door->|
	
/*		