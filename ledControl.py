import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 546)
ORDER = neopixel.GRB

group1_start = 0
group1_end = 174
group2_start = 175
group2_end = 272
group3_start = 273
group3_end = 371
group4_start = 372
group4_end = 545

while True:
    # Group 1: 0-171
    for i in range(group1_start, group1_end + 1):
        pixels[i] = (255, 0, 0)
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Group 2: 172-271
    for i in range(group2_start, group2_end + 1):
        pixels[i] = (0, 255, 0)
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Group 3: 272-371
    for i in range(group3_start, group3_end + 1):
        pixels[i] = (0, 0, 255)
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Group 4: 372-545
    for i in range(group4_start, group4_end + 1):
        pixels[i] = (255, 255, 0)
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(1)
