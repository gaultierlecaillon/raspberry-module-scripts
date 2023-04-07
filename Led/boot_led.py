#!/usr/bin/python3
import time
import board
import neopixel
from random import randint

NUM_PIXEL = 6 + 6 + 15 + 15 # rEyes lEyes strip


class Leds:
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXEL)

    def __init__(self):
        print("Boot led");

    def standBy(self):
        # eyes
        for x in range(0, 12):
            self.pixels[x] = (250, 30, 250)

        # roof
        for x in range(12, 27):
            self.pixels[x] = (250, 50, 250)

        # lidar
        for x in range(27, 42):
            self.pixels[x] = (10, 3, 10)


Leds = Leds();
Leds.standBy();
