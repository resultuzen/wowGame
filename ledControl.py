import time
import board
import neopixel
import random

pixel_pin = board.D18
num_pixels = 542
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def smooth_transition(color1, color2, steps):
    transition = [(int(color1[i] + (color2[i] - color1[i]) / steps)) for i in range(3)]
    return transition

def dance_effect(duration, steps):
    for _ in range(int(duration / steps)):
        target_color = random_color()

        for _ in range(steps):
            pixels.fill(smooth_transition(pixels[0], target_color, steps))
            pixels.show()
            time.sleep(0.05)

dance_effect(60, 5)  # 60 saniye boyunca, her 5 adımda bir renk geçişi
