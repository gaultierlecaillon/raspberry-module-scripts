#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math


class Motion:

    cpr = 8192
    cpr_error_tolerance = 500

    def __init__(self):
        self.initOdrive()
        self.displayInfos()

    def initOdrive(self):
        # Find a connected ODrive (this will block until you connect one)
        print("finding an odrive...")
        self.odrv0 = odrive.find_any()

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

        time.sleep(1)

    def activeLoopControl(self):
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def setFilteredPositionControl(self):
        self.odrv0.axis0.trap_traj.config.accel_limit = 5
        self.odrv0.axis1.trap_traj.config.accel_limit = 5

        self.odrv0.axis0.trap_traj.config.decel_limit = 200
        self.odrv0.axis1.trap_traj.config.decel_limit = 200

        self.odrv0.axis0.trap_traj.config.vel_limit = 30
        self.odrv0.axis1.trap_traj.config.vel_limit = 30

        self.odrv0.axis0.controller.config.input_mode = InputMode.POS_FILTER
        self.odrv0.axis1.controller.config.input_mode = InputMode.POS_FILTER

    def setPIDGains(self):
        self.odrv0.axis0.controller.config.pos_gain = 20  # Position gain for axis0
        self.odrv0.axis1.controller.config.pos_gain = 20  # Position gain for axis1

        self.odrv0.axis0.controller.config.vel_gain = 0.1666666716337204  # Velocity gain for axis0
        self.odrv0.axis1.controller.config.vel_gain = 0.1666666716337204  # Velocity gain for axis1

        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.3333333432674408  # Velocity integrator gain for axis0
        self.odrv0.axis1.controller.config.vel_integrator_gain = 0.3333333432674408  # Velocity integrator gain for axis1


    def moveForward(self, forward, time):
        print("Encoder index befor moveForward to ", forward)
        print("Axis 0:", motors.getEncoderIndex(motors.odrv0.axis0))
        print("Axis 1:", motors.getEncoderIndex(motors.odrv0.axis1))

        self.odrv0.axis0.controller.config.input_filter_bandwidth = time
        self.odrv0.axis1.controller.config.input_filter_bandwidth = time

        self.odrv0.axis0.controller.input_pos = forward
        self.odrv0.axis1.controller.input_pos = forward



    def motionRotate(self, angle, time):
        forward = (33.5 * angle) / 360  # convert angle to x
        self.odrv0.axis0.controller.config.input_filter_bandwidth = time
        self.odrv0.axis1.controller.config.input_filter_bandwidth = time

        self.odrv0.axis0.controller.input_pos = forward
        self.odrv0.axis1.controller.input_pos = -forward

    def getEncoderIndex(self, axis):
        return axis.encoder.shadow_count

    def waitForMovementCompletion(self, index):
        start = time.time()
        delta1 = delta2 = index * self.cpr_error_tolerance

        while delta1 >= self.cpr_error_tolerance and delta2 >= self.cpr_error_tolerance:
            delta1 = abs(self.cpr * index - self.odrv0.axis0.encoder.shadow_count)
            delta2 = abs(self.cpr * index - self.odrv0.axis1.encoder.shadow_count)

            if time.time() - start > 10:
                print("waitForMovementCompletion Timeout")
                exit(1)
            time.sleep(0.01)

        print("Position reached in", round(time.time() - start,2), "s")


motors = Motion()
motors.calibrate()
motors.activeLoopControl()
motors.setPIDGains()
motors.setFilteredPositionControl()




###### STARTING HERE #####
motors.moveForward(10, 2)
motors.waitForMovementCompletion(10)


print("Encoder index after moveForward:")
print("Axis 0:", motors.getEncoderIndex(motors.odrv0.axis0))
print("Axis 1:", motors.getEncoderIndex(motors.odrv0.axis1))