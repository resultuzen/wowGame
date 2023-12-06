import time
import RPi.GPIO as GPIO
import os
import sys
import random
import board
import neopixel

GPIO.setmode(GPIO.BCM)

pixel_pin = board.D18

group1 = 172
group2 = 272
group3 = 372
group4 = 546

steps = group1

num_pixels = 546
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

while True:
    for _ in range(steps):
            pixels.fill(pixels[0], (0, 0 , 255), steps)
            pixels.show()
            time.sleep(0.05)
