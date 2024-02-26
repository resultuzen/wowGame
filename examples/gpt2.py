import RPi.GPIO as GPIO
import pygame
import sys
import time
import os
import random

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
scoreBoardPhoto = pygame.image.load("../photo/scoreBoard.png") 
acilisEkraniPhoto = pygame.image.load("../photo/acilisEkrani.png")

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

def ballAnimation():
    global ballspeedx, ballspeedy, solOyuncuspeed, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy

    if ball.top <= 0 or ball.bottom >= height:
        ballspeedy *= -1

    if ball.centerx <= 15 or ball.centerx >= width - 15:
        if ball.centerx < width / 2:
            p1score += 1

        else:
            p2score += 1

        ballRestart()
        pygame.time.delay(500)

    if ball.colliderect(sagOyuncu):
        ballspeedx *= -1

    if ball.colliderect(solOyuncu):
        ballspeedx *= -1

def ballRestart():
    global ballspeedx, ballspeedy, start
    ball.center = (width // 2, height // 2)
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

ballRestart()

clock = pygame.time.Clock()

calismaDurumu = False
acilisEkrani = True

gecenSure = 0

while True:

    if calismaDurumu == True and acilisEkrani == False:
        
        if GPIO.input(kartKontrolPin) == GPIO.HIGH:
            calismaDurumu = True
            acilisEkrani = False

        if calismaDurumu == True:
            gecenSure = (pygame.time.get_ticks() - baslangicZamani) // 1000  # Oyunun başladığı zamandan geçen süre
            kalanSure = oyunSuresi - gecenSure

            if kalanSure <= 0:
                calismaDurumu = False
                acilisEkrani = True

            # Oyun mantığını işle
            ballAnimation()
            sagOyuncuAnimation(0)
            solOyuncuAnimation(0)

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
                pygame.quit()
                sys.exit()

    if acilisEkrani == True:
        
        if GPIO.input(kartKontrolPin) == GPIO.HIGH:
            calismaDurumu = True
            acilisEkrani = False
            baslangicZamani = pygame.time.get_ticks() 

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        screen.fill(bgcolor)
        screen.blit(acilisEkraniPhoto, (0, 0))
        pygame.display.flip()
