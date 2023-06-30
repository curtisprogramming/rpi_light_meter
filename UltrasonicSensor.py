import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TrigPin = 24
EchoPin = 12

GPIO.setup(TrigPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)

GPIO.output(TrigPin, False)

def calcuateDistance():
    print("calculating")

    GPIO.output(TrigPin, True)
    sleep(0.00001)
    GPIO.output(TrigPin, False)

    while GPIO.input(EchoPin) == 0:
        pulse_start = time()

    while GPIO.input(EchoPin) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)
    print(distance)
    return distance