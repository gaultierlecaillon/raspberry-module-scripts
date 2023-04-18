#!/usr/bin/python3

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time


def main():
    # define GPIO pins
    direction = 22  # Direction (DIR) GPIO Pin
    step = 23  # Step GPIO Pin
    EN_pin = 24  # enable pin (LOW to enable)

    # Declare a instance of class pass GPIO pins numbers and the motor type
    mymotortest = RpiMotorLib.A4988Nema(direction, step, (21, 21, 21), "DRV8825")
    GPIO.setup(EN_pin, GPIO.OUT)  # set enable pin as output

    ###########################
    # Actual motor control
    ###########################
    while True:
        #step = int(input("Enter step:"))
        #direction = bool(step < 0)
        GPIO.output(EN_pin, GPIO.LOW)  # pull enable to low to enable motor
        mymotortest.motor_go(False,  # True=Clockwise, False=Counter-Clockwise
                             "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                             385,  # number of steps
                             .0007,  # step delay [sec]
                             True,  # True = print verbose output
                             .05)  # initial delay [sec]
        time.sleep(1)
        mymotortest.motor_go(True,  # True=Clockwise, False=Counter-Clockwise
                             "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                             385,  # number of steps
                             .0007,  # step delay [sec]
                             True,  # True = print verbose output
                             .5)  # initial delay [sec]
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # clear GPIO allocations after run
