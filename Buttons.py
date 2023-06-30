import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

modeButton = 23
setButton = 18
measureButton = 20

def setupButtons():
    GPIO.setup(modeButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(setButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(measureButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
