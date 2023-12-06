import time
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
import board
import neopixel
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Ekranı ayarla
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

kartKontrolPin = 21

GPIO.setmode(GPIO.BCM)

pygame.init()
clock = pygame.time.Clock()

GPIO.setup(kartKontrolPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

calismaDurumu = False


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

def cardReading(surface):
    font = pygame.font.Font(None, 72)

    text = font.render("Kartı okutun ve bi' oyun görün!", True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    surface.blit(text, textRect)

while True:
    kartKontrolDurumu = GPIO.input(kartKontrolPin)

    if kartKontrolDurumu == GPIO.LOW:
        calismaDurumu = True
        
    if calismaDurumu == False:
        screen.fill(bgcolor)
        cardReading(screen)
        pygame.display.flip()
        clock.tick(60)        
        
    while calismaDurumu == True:
        dance_effect(60, 5)  # 60 saniye boyunca, her 5 adımda bir renk geçişi
