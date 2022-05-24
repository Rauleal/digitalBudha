# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

widthR = 640
heightR = 480
maskOp = 0
imageOp = 1

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (widthR, heightR)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(widthR, heightR))
# allow the camera to warmup
time.sleep(0.1)

#mask
mask = np.zeros([heightR,widthR,3],dtype='uint8')
#print(mask.shape)
#define cricel
center_coordinates = (int(widthR/2),int(heightR/2))
radius = 100
color = (255, 255, 255)  
thickness = -1
mask = cv2.circle(mask, center_coordinates, radius, color, thickness)
inmask = cv2.bitwise_not(mask)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	# show the frame
	#cv2.imshow("Frame", image)
	final = cv2.addWeighted(image,imageOp,inmask,maskOp,0.0)
	cv2.imshow("Frame", final)
	
	imageOp -= 0.01
	maskOp +=0.06
	
	#clsing elments
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows()