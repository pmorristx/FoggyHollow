import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)

while True:
    if(not (GPIO.input(17))):
        GPIO.output(25,True) ## Turn on GPIO pin #25        
        #print "Button Pressed"
        os.system("sudo shutdown -h now")
        break    
    time.sleep(1)



