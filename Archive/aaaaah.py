import serial
import struct
from time import sleep

ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600)
while True:
    correction = 0 #change
    
    motorleft = 255      #change
    motorright = 54      #change
    
    if motorleft < 255:
        motorleft = motorleft/2
    if motorleft == 255:
        motorleft = 127
    if motorright < 255:
        motorright = motorright/2
    if motorright == 255:
        motorright = 127
    motorright = 127
    motorleft = -8
    
    ser.write(struct.pack('bb', motorleft, motorright))
    print ser.readline()
#je suis le dieu qui gagnera robocup
    #ser.write(8)
    #dtaa = int(ser.read()) + 1
'''    while ser.inWaiting():
        data = ser.read()
        print data
'''
	
'''#!/usr/bin/python3

import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

#read from Arduino
input = ser.read()
print("Read input" + input.decode("utf-8")+ "from Arduino")

#write something back
ser.write(b'A')

#read response back from Arduino
for i in range (0,3):
    input = ser.read()
    input_number = ord(input)
    print ("Read input back: " + str(input_number))
    '''