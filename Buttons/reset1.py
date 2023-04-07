import RPi.GPIO as GPIO
import time
import board

# plug on GND and GPIO4 (7)
tiretteGPIO = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(tiretteGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def isTirette():
    return GPIO.input(tiretteGPIO)  # Returns 0 if OFF or 1 if ON


while True:
    print(isTirette())
    time.sleep(0.1)
