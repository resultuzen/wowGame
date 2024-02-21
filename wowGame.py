import time
from encoder import Encoder
import RPi.GPIO as GPIO
import pygame, sys
import os
import random
import board
import neopixel
import time
#from pyvidplayer import Video

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

ledPin = board.D18
ledCount = 672

pixels = neopixel.NeoPixel(ledPin, ledCount, brightness=1, auto_write=False)
ORDER = neopixel.GRB

pixels.fill((0, 0, 0))
pixels.show()

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

# Ekranı ayarla
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
width, height = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

sagOyuncuHiz = 49
sagOyuncuSoftHiz = 7
sagOyuncuYukseklik = 90
sagOyuncuGenislik = 20
sagHedefAraligi = (height // 2) - sagOyuncuYukseklik

solOyuncuHiz = 49
solOyuncuSoftHiz = 7
solOyuncuYukseklik = 90
solOyuncuGenislik = 20
solHedefAraligi = (height // 2) - solOyuncuYukseklik

ustLEDSayisi = 174 #Adet
ustLEDBaslangic = 0 #.indis

altLEDSayisi = 174 #Adet
altLEDBaslangic = 447 #.indis

#vid = Video("intro.mp4") #intro.mp4 diye bir video yok, bunu eklemek gerekiyor.
#vid.set_size((1280, 720)) #Video çözünürlüğü 1920 x 1080 olmalı veya farklı olacaksa buradaki değerler değiştirilmelidir.

def ballAnimation():
    global ballspeedx, ballspeedy, solOyuncuspeed, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy

    if ball.top <= 0 or ball.bottom >= height:
        ballspeedy *= -1
        bounce.play()

        if ball.top <= 0: #Üst LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / ustLEDSayisi))

            for i in range(5):
                pixels[ledNo + i] = (255, 255, 255)
                pixels[ledNo - i] = (255, 255, 255)
                pixels.show()

            time.sleep(0.025)

            for i in reversed(range(5)):
                pixels[ledNo + i] = (0, 0, 0)
                pixels[ledNo - i] = (0, 0, 0)
                pixels.show()

        if ball.bottom >= height: #Alt LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / altLEDSayisi))

            for i in range(5):
                pixels[altLEDBaslangic - ledNo + i] = (255, 255, 255)
                pixels[altLEDBaslangic - ledNo - i] = (255, 255, 255)
                pixels.show()

            time.sleep(0.025)

            for i in reversed(range(5)):
                pixels[altLEDBaslangic - ledNo + i] = (0, 0, 0)
                pixels[altLEDBaslangic - ledNo - i] = (0, 0, 0)
                pixels.show()

    if ball.centerx <= 15 or ball.centerx >= width - 15:
        if ball.centerx < width / 2:
            p1score += 1
            goalAnimation(1) #Eğer karşı bölgedeki LED'ler yanıyorsa buradaki rakam 2 olmalı.

        else:
            p2score += 1
            goalAnimation(2) #Eğer karşı bölgedeki LED'ler yanıyorsa buradaki rakam 1 olmalı.

        goal.play()
        ballRestart()
        pygame.time.delay(500)

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

def introLedAnimation():

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

def goalAnimation(teamSelect):

    if teamSelect == 1: #Sol Taraf

        for dongu in range (4):

            for i in range(group4_start, group4_end + 1):
                pixels[i] = (255, 255, 255)

            for i in range(group5_start, group5_end + 1):
                pixels[i] = (255, 255, 255)

            pixels.show()
            time.sleep(0.1)

            for i in range(group4_start, group4_end + 1):
                pixels[i] = (0, 0, 0)

            for i in range(group5_start, group5_end + 1):
                pixels[i] = (0, 0, 0)

            pixels.show()
            time.sleep(0.1)

    if teamSelect == 2: #Sağ Taraf

        for dongu in range (4):

            for i in range(group2_start, group2_end + 1):
                pixels[i] = (255, 255, 255)

            for i in range(group6_start, group6_end + 1):
                pixels[i] = (255, 255, 255)

            pixels.show()
            time.sleep(0.1)

            for i in range(group2_start, group2_end + 1):
                pixels[i] = (0, 0, 0)

            for i in range(group6_start, group6_end + 1):
                pixels[i] = (0, 0, 0)

            pixels.show()
            time.sleep(0.1)
        
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
         #vid.close()
        
    if calismaDurumu == False:
        #vid.draw(screen, (0, 0)) #Bunun yerine vid.restart() fonksiyonu da kullanılabilir.
        pygame.display.update()
        introLedAnimation()
        #clock.tick(60)
        
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
