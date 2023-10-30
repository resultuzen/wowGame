import time
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# GPIO pinlerini ayarla
ENKODER1_DT = 19
ENKODER1_CLK = 13
ENKODER2_DT = 6
ENKODER2_CLK = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENKODER1_CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENKODER1_DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENKODER2_CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENKODER2_DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Enkoderlerin değerlerini tutmak için değişkenler
enkoder1_value = 0
enkoder2_value = 0

# Initialize last states for both encoders
enkoder1_clkLastState = GPIO.input(ENKODER1_CLK)
enkoder2_clkLastState = GPIO.input(ENKODER2_CLK)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Read current states
    enkoder1_clk = GPIO.input(ENKODER1_CLK)
    enkoder1_dt = GPIO.input(ENKODER1_DT)
    enkoder2_clk = GPIO.input(ENKODER2_CLK)
    enkoder2_dt = GPIO.input(ENKODER2_DT)

    # Her iki enkoder için dönüş değerlerini hesapla
    if enkoder1_clk != enkoder1_clkLastState:
        if enkoder1_dt != enkoder1_clk:
            enkoder1_value += 1
            enkoder1_clkLastState = enkoder1_clk
        else:
            enkoder1_value -= 1
            enkoder1_clkLastState = enkoder1_clk

    if enkoder2_clk != enkoder2_clkLastState:
        if enkoder2_dt != enkoder2_clk:
            enkoder2_value += 1
            enkoder2_clkLastState = enkoder2_clk
        else:
            enkoder2_value -= 1
            enkoder2_clkLastState = enkoder2_clk
    
    print("Enkoder 1 Data:", enkoder1_dt)
    print("Enkoder 1 Clock:", enkoder1_clk)
    print("Enkoder 1 Clock Last State:", enkoder1_clkLastState)
    print("Enkoder 1:", enkoder1_value)

    time.sleep(2)

    print("Enkoder 2 Data:", enkoder2_dt)
    print("Enkoder 2 Clock:", enkoder2_clk)
    print("Enkoder 2 Clock Last State:", enkoder2_clkLastState)
    print("Enkoder 2:", enkoder2_value)

    time.sleep(2)

pygame.quit()
sys.exit()
