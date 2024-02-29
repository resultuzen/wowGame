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

#Sağ Oyuncu Ayarları
sagOyuncuHiz = 49
sagOyuncuSoftHiz = 7
sagOyuncuYukseklik = 90
sagOyuncuGenislik = 20
sagHedefAraligi = (height // 2) - sagOyuncuYukseklik

#Sol Oyuncu Ayarları
solOyuncuHiz = 49
solOyuncuSoftHiz = 7
solOyuncuYukseklik = 90
solOyuncuGenislik = 20
solHedefAraligi = (height // 2) - solOyuncuYukseklik

#Fotoğraf Ayarları
scoreBoardPhoto = pygame.image.load("photo/scoreBoard.png") 
acilisEkraniPhoto = pygame.image.load("photo/acilisEkrani.png")

#Skor Tablosu Ayarları
oyunSuresi = 10 #sn
baslangicZamani = None
p1score = 0
p2score = 0

#Oyundaki Nesnelerin Konumları
ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0

sagOyuncu = pygame.Rect(width - 30, height // 2 - (sagOyuncuYukseklik // 2), sagOyuncuGenislik, sagOyuncuYukseklik)
solOyuncu = pygame.Rect(10, height // 2 - (solOyuncuYukseklik // 2), solOyuncuGenislik, solOyuncuYukseklik)

kartKontrolPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(kartKontrolPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ledPin = board.D18
ledCount = 673

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

ustLEDSayisi = 174
ustLEDBaslangic = 0 

altLEDSayisi = 174 
altLEDBaslangic = 447 

solEnkoderDataPin = 19
solEnkoderClockPin = 13
sagEnkoderDataPin = 6
sagEnkoderClockPin = 5

#Kart Okuyucu Ayarları
kartKontrolPin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(kartKontrolPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

kartOkuma = False

#Enkoder Ayarları
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
    global ballspeedx, ballspeedy, solOyuncuspeed, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy

    if ball.top <= 0 or ball.bottom >= height:
        ballspeedy *= -1
        bounce.play()

        if ball.top <= 0:  # Üst LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / ustLEDSayisi))

            for i in range(5):
                pixels[ledNo + i] = (255, 255, 255)
                pixels[ledNo - i] = (255, 255, 255)

            pixels.show()

            for i in reversed(range(5)):
                pixels[ledNo + i] = (0, 0, 0)
                pixels[ledNo - i] = (0, 0, 0)

            pixels.show()

        if ball.bottom >= height:  # Alt LED'lerin Kontrolleri
            ledNo = round(ball.centerx / (width / altLEDSayisi))

            for i in range(5):
                pixels[altLEDBaslangic - ledNo + i] = (255, 255, 255)
                pixels[altLEDBaslangic - ledNo - i] = (255, 255, 255)

            pixels.show()

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

def introLedAnimation():
    
    pixels.fill((random.choice([0, 255]), random.choice([0, 255]), random.choice([0, 255])))
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

            for y in range(group5_start, group5_end + 1):
                pixels[y] = (255, 255, 255)

            pixels.show()
            time.sleep(0.1)

            for i in range(group4_start, group4_end + 1):
                pixels[i] = (0, 0, 0)

            for y in range(group5_start, group5_end + 1):
                pixels[y] = (0, 0, 0)

            pixels.show()
            time.sleep(0.1)

    if teamSelect == 2: #Sağ Taraf

        for dongu in range (4):

            for i in range(group2_start, group2_end + 1):
                pixels[i] = (255, 255, 255)

            for y in range(group6_start, group6_end + 1):
                pixels[y] = (255, 255, 255)

            pixels.show()
            time.sleep(0.1)

            for i in range(group2_start, group2_end + 1):
                pixels[i] = (0, 0, 0)

            for y in range(group6_start, group6_end + 1):
                pixels[y] = (0, 0, 0)

            pixels.show()
            time.sleep(0.1)

ballRestart()

clock = pygame.time.Clock()

calismaDurumu = False
acilisEkrani = True

gecenSure = 0

while True:

    if calismaDurumu == True and acilisEkrani == False:

        if calismaDurumu == True:
            gecenSure = (pygame.time.get_ticks() - baslangicZamani) // 1000  # Oyunun başladığı zamandan geçen süre
            kalanSure = oyunSuresi - gecenSure

            if kalanSure <= 0:
                pixels.fill((0, 0, 0))
                pixels.show()
                calismaDurumu = False
                acilisEkrani = True
                p1score = 0
                p2score = 0

            # Oyun mantığını işle
            sagEnkoderDegeri = sagEncoder.getValue()
            solEnkoderDegeri = solEncoder.getValue()

            ballAnimation()
            sagOyuncuAnimation(sagEnkoderDegeri)
            solOyuncuAnimation(solEnkoderDegeri)

            # Ekranı temizle ve çizimleri yap
            screen.fill(bgcolor)
            screen.blit(scoreBoardPhoto,(560, 0))
            
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pixels.fill((0, 0, 0))
                pixels.show()
                GPIO.cleanup()
                pygame.quit()
                sys.exit()

    if acilisEkrani == True:
        
        if GPIO.input(kartKontrolPin) == GPIO.HIGH:
            pixels.fill((0, 0, 0))
            pixels.show()
            ballRestart()
            calismaDurumu = True
            acilisEkrani = False
            baslangicZamani = pygame.time.get_ticks() 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pixels.fill((0, 0, 0))
                pixels.show()
                GPIO.cleanup()
                pygame.quit()
                sys.exit()
                
        screen.fill(bgcolor)
        screen.blit(acilisEkraniPhoto, (0, 0))
        pygame.display.flip()
        introLedAnimation()
