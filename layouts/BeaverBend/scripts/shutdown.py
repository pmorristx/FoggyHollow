import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27,True) ## Turn on GPIO pin #27
while True:
    if(GPIO.input(17)):
        #GPIO.output(27,False) ## Turn off GPIO pin #27
        os.system("sudo shutdown -h now")
        break
    time.sleep(1)

