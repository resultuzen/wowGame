import RPi.GPIO as GPIO
import pygame
import sys
import time
import os
import random
import board
import neopixel
from encoder import Encoder

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Ekran Ayarları
pygame.init()
pygame.display.set_caption("Pong Game!")
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
width, height = screen.get_size()
bgcolor = pygame.Color('black')
gamecolor = pygame.Color('white')

# Sağ Oyuncu Ayarları
sagOyuncuHiz = 49
sagOyuncuSoftHiz = 7
sagOyuncuYukseklik = 90
sagOyuncuGenislik = 20

# Sol Oyuncu Ayarları
solOyuncuHiz = 49
solOyuncuSoftHiz = 7
solOyuncuYukseklik = 90
solOyuncuGenislik = 20

# Fotoğraf Ayarları
scoreBoardPhoto = pygame.image.load("photo/scoreBoard.png")
acilisEkraniPhoto = pygame.image.load("photo/acilisEkrani.png")

# Skor Tablosu Ayarları
oyunSuresi = 10  # sn
baslangicZamani = None
p1score = 0
p2score = 0

# Oyundaki Nesnelerin Konumları
ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
ballcolor = pygame.Color('white')
ballspeed = [7 * random.choice((1, -1)), 7 * random.choice((1, -1))]

sagOyuncu = pygame.Rect(width - 30, height // 2 - (sagOyuncuYukseklik // 2), sagOyuncuGenislik, sagOyuncuYukseklik)
solOyuncu = pygame.Rect(10, height // 2 - (solOyuncuYukseklik // 2), solOyuncuGenislik, solOyuncuYukseklik)

ledPin = board.D18
ledCount = 673

pixels = neopixel.NeoPixel(ledPin, ledCount, brightness=1, auto_write=False)
ORDER = neopixel.GRB

pixels.fill((0, 0, 0))
pixels.show()

group_positions = [
    (0, 174),  # Üst LED'ler
    (273, 447),  # Alt LED'ler
    (0, 174),  # Sol LED'ler
    (448, 672)  # Sağ LED'ler
]

solEnkoderDataPin = 19
solEnkoderClockPin = 13
sagEnkoderDataPin = 6
sagEnkoderClockPin = 5

# Kart Okuyucu Ayarları
kartKontrolPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(kartKontrolPin, GPIO.IN)  # PUD_UP

# Enkoder Ayarları
solEncoder = Encoder(solEnkoderDataPin, solEnkoderClockPin)
sagEncoder = Encoder(sagEnkoderDataPin, sagEnkoderClockPin)

solEnkoderDegeri = 0
sagEnkoderDegeri = 0

# Ses dosyaları
hit = pygame.mixer.Sound('music/hit.ogg')
bounce = pygame.mixer.Sound('music/bounce.ogg')
goal = pygame.mixer.Sound('music/goal.ogg')
start = pygame.mixer.Sound('music/start.ogg')

def ballAnimation():
    global ballspeed, p1score, p2score, hit, bounce
    ball.x += ballspeed[0]
    ball.y += ballspeed[1]

    if ball.top <= 0 or ball.bottom >= height:
        ballspeed[1] *= -1
        bounce.play()
        ledControl(ball, True) if ball.top <= 0 else ledControl(ball, False)

    if ball.centerx <= 15 or ball.centerx >= width - 15:
        if ball.centerx < width / 2:
            p1score += 1
            goalAnimation(1)
        else:
            p2score += 1
            goalAnimation(2)

        goal.play()
        ballRestart()
        pygame.time.delay(500)

    if ball.colliderect(sagOyuncu) or ball.colliderect(solOyuncu):
        ballspeed[0] *= -1
        hit.play()

def ballRestart():
    global ballspeed, start
    ball.center = (width // 2, height // 2)
    start.play()
    ballspeed = [7 * random.choice((1, -1)), 7 * random.choice((1, -1))]

def oyuncuAnimation(oyuncu, enkoder_value, oyuncu_hiz, oyuncu_soft_hiz):
    target_y = (height // 2) - (oyuncu.height // 2) + enkoder_value * oyuncu_hiz

    if target_y > oyuncu.y:
        oyuncu.y += oyuncu_soft_hiz
    elif target_y < oyuncu.y:
        oyuncu.y -= oyuncu_soft_hiz

def ledControl(ball, is_top):
    led_group = 0 if is_top else 1
    for i in range(group_positions[led_group][0], group_positions[led_group][1] + 1):
        pixels[i] = (255, 255, 255)
    pixels.show()
    time.sleep(0.1)
    for i in range(group_positions[led_group][0], group_positions[led_group][1] + 1):
        pixels[i] = (0, 0, 0)
    pixels.show()
    time.sleep(0.1)

def introLedAnimation():
    pixels.fill((random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255])))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

def goalAnimation(teamSelect):
    led_group = 2 if teamSelect == 1 else 3
    for _ in range(4):
        for i in range(group_positions[led_group][0], group_positions[led_group][1] + 1):
            pixels[i] = (255, 255, 255)
        pixels.show()
        time.sleep(0.1)
        for i in range(group_positions[led_group][0], group_positions[led_group][1] + 1):
            pixels[i] = (0, 0, 0)
        pixels.show()
        time.sleep(0.1)

ballRestart()
clock = pygame.time.Clock()

calismaDurumu = False
acilisEkrani = True
gecenSure = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pixels.fill((0, 0, 0))
            pixels.show()
            GPIO.cleanup()
            pygame.quit()
            sys.exit()

    if acilisEkrani:
        if GPIO.input(kartKontrolPin) == GPIO.HIGH:
            pixels.fill((0, 0, 0))
            pixels.show()
            ballRestart()
            calismaDurumu = True
            acilisEkrani = False
            baslangicZamani = pygame.time.get_ticks()

        screen.fill(bgcolor)
        screen.blit(acilisEkraniPhoto, (0, 0))
        pygame.display.flip()
        introLedAnimation()

    elif calismaDurumu:
        gecenSure = (pygame.time.get_ticks() - baslangicZamani) // 1000
        kalanSure = oyunSuresi - gecenSure

        if kalanSure <= 0:
            pixels.fill((0, 0, 0))
            pixels.show()
            calismaDurumu = False
            acilisEkrani = True
            p1score = 0
            p2score = 0

        sagEnkoderDegeri = sagEncoder.getValue()
        solEnkoderDegeri = solEncoder.getValue()

        ballAnimation()
        oyuncuAnimation(sagOyuncu, sagEnkoderDegeri, sagOyuncuHiz, sagOyuncuSoftHiz)
        oyuncuAnimation(solOyuncu, solEnkoderDegeri, solOyuncuHiz, solOyuncuSoftHiz)

        screen.fill(bgcolor)
        screen.blit(scoreBoardPhoto, (560, 0))

        scoreBoardFont = pygame.font.Font(None, 100)
        leftScoreText = scoreBoardFont.render("{}".format(p1score), True, (255, 255, 255))
        timeScoreText = scoreBoardFont.render("{}".format(kalanSure), True, (255, 255, 255))
        rightScoreText = scoreBoardFont.render("{}".format(p2score), True, (255, 255, 255))

        screen.blit(leftScoreText, (700, 44))
        screen.blit(timeScoreText, (935, 44))
        screen.blit(rightScoreText, (1225, 44))

        pygame.draw.rect(screen, gamecolor, sagOyuncu)
        pygame.draw.rect(screen, gamecolor, solOyuncu)
        pygame.draw.ellipse(screen, ballcolor, ball)

        pygame.display.flip()
        clock.tick(60)
