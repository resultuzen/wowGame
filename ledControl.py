import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)

group1 = 172
group2 = 272
group3 = 372
group4 = 546

steps = group1

num_pixels = 546
ORDER = neopixel.GRB

while True:
    for _ in range(steps):
            pixels[0] = (255, 0, 0)
            pixels.fill((0, 255, 0))
            pixels.show()
            time.sleep(0.05)
