import time
import board
import neopixel
import random

pixel_pin = board.D18
num_pixels = 542
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def dance_effect():
    for _ in range(10):  # 10 kere dans et
        for i in range(num_pixels):
            pixels[i] = random_color()
        pixels.show()
        time.sleep(0.5)  # 0.5 saniye bekle

dance_effect()
