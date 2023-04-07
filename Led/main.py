#!/usr/bin/python3
import time
import board
import neopixel
from random import randint

NUM_PIXEL = 6 + 6 + 15 + 15 # rEyes lEyes strip


class Leds:
    pixels = neopixel.NeoPixel(board.D18, NUM_PIXEL)

    def __init__(self):
        print("Hello");

    def standBy(self):
        start = 0
        end = 200
        step = 4
        while True:
            for i in range(start, end, step):
                for x in range(0, NUM_PIXEL):
                    self.pixels[x] = (250, i, 250)

            for i in range(end, start, -step):
                for x in range(0, NUM_PIXEL):
                    self.pixels[x] = (250, i, 250)

            time.sleep(1)


Leds = Leds();
Leds.standBy();
