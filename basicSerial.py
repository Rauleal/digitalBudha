import serial
import RPi.GPIO as GPIO
import time
import numpy as np

samples = 10
i = 0

#ser1=serial.Serial("/dev/ttyUSB0",9600)  #change port,, UNO comes as USBx number as found from ls /dev/tty/ACM*
#.ser1.baudrate=9600

ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

sensorSample = np.zeros(samples, dtype=int)

#def blink(pin):


#GPIO.output(pin,GPIO.HIGH)  
#time.sleep(1)  
#GPIO.output(pin,GPIO.LOW)  
#time.sleep(1)  
#return

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.OUT)
while True:
    #read_ser1=ser1.readline()
    #print("sensor1")
    #print(read_ser1)
    read_ser=ser.readline().decode('utf-8')
    #print("sensor2")
    #print(read_ser2)
    #print(sensorSample)
    
    sensorSample[i] = read_ser
    if(i < samples-1):
        i += 1
    else:
        i = 0
    
    average = np.average(sensorSample)
    
    print(average)
#if(read_ser=="Hello From Arduino!"):
#blink(11)