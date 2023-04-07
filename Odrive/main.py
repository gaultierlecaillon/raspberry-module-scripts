#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

class Motors:

    def __init__(self):
        self.initOdrive()
        self.displayInfos()

    def initOdrive(self):
        # Find a connected ODrive (this will block until you connect one)
        print("finding an odrive...")
        self.odrv0 = odrive.find_any()
        time.sleep(1)

    def displayInfos(self):
        print("\n======================\nOdrive Infos:")
        print("VBus Voltage: " + str(self.odrv0.vbus_voltage))
        print("\n")

    def calibrate(self):
        # Calibrate motor and wait for it to finish
        print("Starting calibration...")
        self.odrv0.clear_errors()
        self.odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        self.odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

        while self.odrv0.axis0.current_state != AXIS_STATE_IDLE and self.odrv0.axis1.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

    def activeLoopControl(self):
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def startFilteredPositionControl(self):
        self.odrv0.axis0.trap_traj.config.accel_limit = 5
        self.odrv0.axis1.trap_traj.config.accel_limit = 5

        self.odrv0.axis0.trap_traj.config.decel_limit = 15
        self.odrv0.axis1.trap_traj.config.decel_limit = 15

        self.odrv0.axis0.trap_traj.config.vel_limit = 15
        self.odrv0.axis1.trap_traj.config.vel_limit = 15

        self.odrv0.axis0.controller.config.input_mode = InputMode.POS_FILTER
        self.odrv0.axis1.controller.config.input_mode = InputMode.POS_FILTER

    def moveForward(self, forward, time):
        self.odrv0.axis0.controller.config.input_filter_bandwidth = time
        self.odrv0.axis1.controller.config.input_filter_bandwidth = time

        self.odrv0.axis0.controller.input_pos = forward
        self.odrv0.axis1.controller.input_pos = forward

    def motionRotate(self, angle, time):
        forward = (33.5 * angle) / 360 # convert angle to x
        self.odrv0.axis0.controller.config.input_filter_bandwidth = time
        self.odrv0.axis1.controller.config.input_filter_bandwidth = time

        self.odrv0.axis0.controller.input_pos = forward
        self.odrv0.axis1.controller.input_pos = -forward


motors = Motors()
motors.calibrate()
motors.activeLoopControl()
motors.startFilteredPositionControl()

while True:
    '''
    angle = float(input("angle: "))
    time = int(input("time: "))
    motors.motionRotate(angle, time)
    '''


    motors.moveForward(-40, 1.5)
    time.sleep(3)
    motors.moveForward(0, 1.5)
    time.sleep(3)
    motors.motionRotate(180, 1.5)
    time.sleep(3)
    motors.motionRotate(0, 1.5)
    time.sleep(3)




