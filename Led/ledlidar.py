import time
import board
import neopixel

NUM_PIXEL = 15
pixels = neopixel.NeoPixel(board.D18, NUM_PIXEL)

while True:
    for x in range(0, NUM_PIXEL):
        x2 = (x+7) % NUM_PIXEL
        print("x:", x, ", x2:", x2 )
        pixels[x] = (255,165,0)
        #pixels[x2] = (255, 0, 255)
        time.sleep(0.1)