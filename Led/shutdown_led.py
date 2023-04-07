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
        for x in range(0, NUM_PIXEL):
            self.pixels[x] = (0, 0, 0)


Leds = Leds();
Leds.standBy();
