import time
from encoder import Encoder
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
import board
import neopixel
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

ledPin = board.D18
ledCount = 447
pixels = neopixel.NeoPixel(ledPin, ledCount, brightness=1, auto_write=False)
ORDER = neopixel.GRB

pixels.fill((0, 0, 0))
pixels.show()

# Ekranı ayarla
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

sagOyuncuHiz = 10
sagOyuncuSoftHiz = 2
sagOyuncuYukseklik = 140
sagOyuncuGenislik = 20
sagHedefAraligi = (height // 2) - sagOyuncuYukseklik

solOyuncuHiz = 10
solOyuncuSoftHiz = 2
solOyuncuYukseklik = 140
solOyuncuGenislik = 20
solHedefAraligi = (height // 2) - solOyuncuYukseklik

ustLEDSayisi = 174 #Adet
ustLEDBaslangic = 0 #.indis

altLEDSayisi = 174 #Adet
altLEDBaslangic = 273 #.indis

def ballAnimation():
    global ballspeedx, ballspeedy, solOyuncuspeed, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy

    if ball.top <= 0 or ball.bottom >= height:
        ballspeedy *= -1
        time.sleep(1)
        bounce.play()

        if ball.bottom >= height: #Üst LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / ustLEDSayisi))

            pixels[ledNo] = (0, 255, 0)
            pixels.show()

            time.sleep(0.1)

            pixels[ledNo] = (0, 0, 0)
            pixels.show()

        if ball.top <= 0: #Alt LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / altLEDSayisi))

            pixels[447 - (ledNo + altLEDBaslangic)] = (0, 255, 0)
            pixels.show()

            time.sleep(0.1)

            pixels[447 - (ledNo + altLEDBaslangic)] = (0, 0, 0)
            pixels.show()

    if ball.centerx <= 15 or ball.centerx >= width - 15:
        if ball.centerx < width/2:
            p1score += 1

        else:
            p2score += 1

        goal.play()
        ballRestart()
        pygame.time.delay(1000)

    if ball.colliderect(sagOyuncu):
        ballspeedx *= -1
        hit.play()

    if ball.colliderect(solOyuncu):
        ballspeedx *= -1
        hit.play()


def ballRestart():
    global ballspeedx, ballspeedy, start
    ball.center = (width // 2, height // 2)
    start.play()
    ballspeedx = 7 * random.choice((1, -1))
    ballspeedy = 7 * random.choice((1, -1))


def sagOyuncuAnimation(enkoder_value):

    target_y = (height // 2) - (sagOyuncuYukseklik // 2) + enkoder_value * sagOyuncuHiz

    if target_y > sagOyuncu.y:
        sagOyuncu.y += sagOyuncuSoftHiz 

    elif target_y < sagOyuncu.y:
        sagOyuncu.y -= sagOyuncuSoftHiz
    
def solOyuncuAnimation(enkoder_value):
            
    target_y = (height // 2) - (solOyuncuYukseklik // 2) + enkoder_value * solOyuncuHiz

    if target_y > solOyuncu.y:
        solOyuncu.y += solOyuncuSoftHiz

    elif target_y < solOyuncu.y:
        solOyuncu.y -= solOyuncuSoftHiz        

def printScore(surface):
    global p1score, p2score
    font = pygame.font.Font(None, 72)
    text = font.render(str(p2score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width // 2-30, 42)
    surface.blit(text, textRect)
    text = font.render(str(p1score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width // 2+30, 42)
    surface.blit(text, textRect)

def cardReading(surface):
    font = pygame.font.Font(None, 72)

    text = font.render("Kartı okutun ve bi' oyun görün!", True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    surface.blit(text, textRect)

# GPIO pinlerini ayarla
solEnkoderDataPin = 19
solEnkoderClockPin = 13
sagEnkoderDataPin = 6
sagEnkoderClockPin = 5

kartKontrolPin = 21

GPIO.setmode(GPIO.BCM)

solEncoder = Encoder(solEnkoderDataPin, solEnkoderClockPin)
sagEncoder = Encoder(sagEnkoderDataPin, sagEnkoderClockPin)

pygame.init()
clock = pygame.time.Clock()

# Ses dosyaları
hit = pygame.mixer.Sound('hit.ogg')
bounce = pygame.mixer.Sound('bounce.ogg')
goal = pygame.mixer.Sound('goal.ogg')
start = pygame.mixer.Sound('start.ogg')

ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

sagOyuncu = pygame.Rect(width - 30, height // 2 - (sagOyuncuYukseklik // 2), sagOyuncuGenislik, sagOyuncuYukseklik)
solOyuncu = pygame.Rect(10, height // 2 - (solOyuncuYukseklik // 2), solOyuncuGenislik, solOyuncuYukseklik)

p1score = 0
p2score = 0

# Enkoderlerin değerlerini tutmak için değişkenler
solEnkoderDegeri = 0
sagEnkoderDegeri = 0

GPIO.setup(kartKontrolPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

calismaDurumu = False

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        sagEnkoderDegeri = sagEncoder.getValue()
        solEnkoderDegeri = solEncoder.getValue()
    
        # Oyun mantığını işle
        ballAnimation()
        sagOyuncuAnimation(sagEnkoderDegeri)
        solOyuncuAnimation(solEnkoderDegeri)
    
        # Ekranı temizle ve çizimleri yap
        screen.fill(bgcolor)
        printScore(screen)
        pygame.draw.aaline(screen, gamecolor, (width // 2, 0), (width // 2, height))
        pygame.draw.rect(screen, gamecolor, sagOyuncu)
        pygame.draw.rect(screen, gamecolor, solOyuncu)
        pygame.draw.ellipse(screen, ballcolor, ball)
    
        pygame.display.flip()
        clock.tick(60)
        
    time.sleep(0.1)
