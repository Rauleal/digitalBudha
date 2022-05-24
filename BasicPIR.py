import RPi.GPIO as GPIO
import time
pin_pir =18 

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)         #Read output from PIR motion sensor

while True:
    i=GPIO.input(18)
    print(i)
    time.sleep(1)

