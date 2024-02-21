import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 546)
pixels2 = neopixel2.NeoPixel(board.D23, 124)
ORDER = neopixel2.GRB

group1_start = 0
group1_end = 174
group2_start = 175
group2_end = 272
group3_start = 273
group3_end = 447
group4_start = 448
group4_end = 545

group5_start = 0
group5_end = 125

while True:
    pixels2.fill((255, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 255, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 255))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((255, 255, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 255, 255))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((255, 0, 255))
    pixels2.show()
    time.sleep(0.1)

    pixels2.fill((0, 0, 0))
    pixels2.show()
    time.sleep(0.1)
