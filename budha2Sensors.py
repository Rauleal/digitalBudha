from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import serial
import RPi.GPIO as GPIO
import numpy as np

#define variables
i = 0
samples = 10
reset = samples * 0.01
widthR = 640
heightR = 480
circRadius = 300
maskOp = 0
imageOp = 1
maskRate = 0.03
imageRate = 0.01
read_ser = 0
sensorSample = np.zeros(samples, dtype=int)
motionAverage = 0

#functions

def updateMotionArray(value,index):     
    
    sensorSample[index] = value
        
    if(index < samples-1):
        index += 1
    else:
        index = 0
        
    return index

    
#intialize sensors
##serial

#ser1=serial.Serial("/dev/ttyUSB0",9600)  #change port,, UNO comes as USBx number as found from ls /dev/tty/ACM*
#.ser1.baudrate=9600

ser=serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

##GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN) 

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (widthR, heightR)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(widthR, heightR))
# allow the camera to warmup
time.sleep(0.1)

# define mask
mask = np.zeros([heightR,widthR,3],dtype='uint8')
#print(mask.shape)
#define cricle
center_coordinates = (int(widthR/2),int(heightR/2))
color = (255, 255, 255)  
thickness = -1
mask = cv2.circle(mask, center_coordinates, circRadius, color, thickness)
inmask = cv2.bitwise_not(mask)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    #cv2.imshow("Frame", image)
    final = cv2.addWeighted(image,imageOp,inmask,maskOp,0.0)
    cv2.imshow("Frame", final)
    
    read_serial=ser.readline().decode('utf-8')
    i = updateMotionArray(read_serial,i)
    
    read_pin = GPIO.input(18)
    i = updateMotionArray(read_pin,i)
    
    motionAverage = np.average(sensorSample)
    #if(i < samples-1):
    #    i += 1
    #else:
    #    i = 0
    print(sensorSample)
    #print(motionAverage)
    if(motionAverage > reset):
        maskOp = 0
        imageOp = 1
    else:
        imageOp -= imageRate
        maskOp += maskRate
    
    #clsing elments
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
GPIO.cleanup()
ser.close()


