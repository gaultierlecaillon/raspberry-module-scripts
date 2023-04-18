#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math


class Motion:

    is_calibrated = False
    cpr = 8192
    cpr_error_tolerance = 100

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

        if not self.is_calibrated:
            # Calibrate motor and wait for it to finish
            print("Starting calibration...")

            self.odrv0.clear_errors()
            self.odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
            self.odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

            while self.odrv0.axis0.current_state != AXIS_STATE_IDLE and self.odrv0.axis1.current_state != AXIS_STATE_IDLE:
                time.sleep(0.1)

            time.sleep(0.1)
            self.activeLoopControl()
            self.is_calibrated = True
        else:
            print("Odrive already calibrated")

    def activeLoopControl(self):
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    def setPIDGains(self):
        self.odrv0.axis0.controller.config.pos_gain = 20  # Position gain for axis0
        self.odrv0.axis1.controller.config.pos_gain = 20  # Position gain for axis1

        self.odrv0.axis0.controller.config.vel_gain = 0.1666666716337204  # Velocity gain for axis0
        self.odrv0.axis1.controller.config.vel_gain = 0.1666666716337204  # Velocity gain for axis1

        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.3333333432674408  # Velocity integrator gain for axis0
        self.odrv0.axis1.controller.config.vel_integrator_gain = 0.3333333432674408  # Velocity integrator gain for axis1

    def setFilteredPositionControl(self):
        self.odrv0.axis0.trap_traj.config.accel_limit = 20
        self.odrv0.axis1.trap_traj.config.accel_limit = 20

        self.odrv0.axis0.trap_traj.config.decel_limit = 20
        self.odrv0.axis1.trap_traj.config.decel_limit = 20

        self.odrv0.axis0.trap_traj.config.vel_limit = 20
        self.odrv0.axis1.trap_traj.config.vel_limit = 20

        self.odrv0.axis0.controller.config.inertia = 0
        self.odrv0.axis1.controller.config.inertia = 0


        self.odrv0.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
        self.odrv0.axis1.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ

    def getEncoderIndex(self, axis):
        return axis.encoder.shadow_count

    def moveForward(self, forward_mm):
        forward_index = 50 / 1265 * forward_mm  # cause when I input 50 pos, robot move 1265mm
        self.odrv0.axis0.controller.input_pos = forward_index
        self.odrv0.axis1.controller.input_pos = forward_index

    def moveRotate(self, forward_mm):
        forward_index = 50/1265 * forward_mm # cause when I input 50 pos, robot move 1m 26cm and 5mm
        self.odrv0.axis0.controller.input_pos = forward_index
        self.odrv0.axis1.controller.input_pos = - forward_index

    def waitForMovementCompletion(self, forward_mm):
        time.sleep(0.1) # avoid false encoder value

        #After calibration, I know 1000mm=323800 index and 0mm=0index
        index_target = 323800/1000 * forward_mm
        start = time.time()
        delta1 = delta2 = forward_mm * self.cpr_error_tolerance

        while delta1 >= self.cpr_error_tolerance and delta2 >= self.cpr_error_tolerance:
            delta1 = abs(index_target - self.odrv0.axis0.encoder.shadow_count)
            delta2 = abs(index_target - self.odrv0.axis1.encoder.shadow_count)

            if time.time() - start > 10:
                print("waitForMovementCompletion Timeout")
                exit(1)
            time.sleep(0.01)

        print("Position reached in", round(time.time() - start,2), "s")


motors = Motion()
motors.calibrate()
motors.setPIDGains()
motors.setFilteredPositionControl()

while True:
    forward_mm = float(input("\nEnter any value in mm: "))

    print("Encoder 1 before", motors.getEncoderIndex(motors.odrv0.axis0))
    print("Encoder 2 before", motors.getEncoderIndex(motors.odrv0.axis1))

    motors.moveForward(forward_mm)
    #motors.moveRotate(forward_mm)
    motors.waitForMovementCompletion(forward_mm)

    print("Motion Done !")
    print("Encoder 1 after", motors.getEncoderIndex(motors.odrv0.axis0))
    print("Encoder 2 after", motors.getEncoderIndex(motors.odrv0.axis1))
