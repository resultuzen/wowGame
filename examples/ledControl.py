import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 672)
ORDER = neopixel.GRB

group1_start = 0
group1_end = 174
group2_start = 175
group2_end = 272
group3_start = 273
group3_end = 447
group4_start = 448
group4_end = 545

group5_start = 546
group5_end = 609

group6_start = 610
group6_end = 672

while True:
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 255, 255))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((255, 0, 255))
    pixels.show()
    time.sleep(0.1)

    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)
