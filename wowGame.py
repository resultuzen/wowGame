from time import sleep
from encoder import Encoder
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

player1speed = 2
player2speed = 2

def ballAnimation():
    global ballspeedx, ballspeedy, player2speed, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy
    if ball.top <= 0 or ball.bottom >= height:
        ballspeedy *= -1
        bounce.play()
    if ball.centerx <= 15 or ball.centerx >= width - 15:
        if ball.centerx < width/2:
            p1score += 1
        else:
            p2score += 1
        goal.play()
        ballRestart()
        pygame.time.delay(1000)
    if ball.colliderect(player1):
        ballspeedx *= -1
        hit.play()
    if ball.colliderect(player2):
        ballspeedx *= -1
        hit.play()


def ballRestart():
    global ballspeedx, ballspeedy, start
    ball.center = (width/2, height/2)
    start.play()
    ballspeedx = 7 * random.choice((1, -1))
    ballspeedy = 7 * random.choice((1, -1))


def player1Animation(enkoder_value):
    player1.y += enkoder_value * player1speed
    if player1.top <= 0:
        player1.top = 0
    if player1.bottom >= height:
        player1.bottom = height


def player2Animation(enkoder_value):
    player2.y += enkoder_value * player2speed
    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= height:
        player2.bottom = height


def printScore(surface):
    global p1score, p2score
    font = pygame.font.Font(None, 72)
    text = font.render(str(p2score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2-30, 42)
    surface.blit(text, textRect)
    text = font.render(str(p1score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2+30, 42)
    surface.blit(text, textRect)

# GPIO pinlerini ayarla
ENKODER1_DT = 19
ENKODER1_CLK = 13
ENKODER2_DT = 6
ENKODER2_CLK = 5

GPIO.setmode(GPIO.BCM)

encoder1 = Encoder(ENKODER1_DT, ENKODER1_CLK)
encoder2 = Encoder(ENKODER2_DT, ENKODER2_CLK)

pygame.init()
clock = pygame.time.Clock()

# Ses dosyaları
hit = pygame.mixer.Sound('hit.ogg')
bounce = pygame.mixer.Sound('bounce.ogg')
goal = pygame.mixer.Sound('goal.ogg')
start = pygame.mixer.Sound('start.ogg')

# Ekranı ayarla
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

ball = pygame.Rect(width/2-15, height/2-15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

player1 = pygame.Rect(width - 30, height // 2 - 70, 20, 140)
player2 = pygame.Rect(10, height // 2 - 70, 20, 140)

p1score = 0
p2score = 0

# Enkoderlerin değerlerini tutmak için değişkenler
enkoder1_value = 0
enkoder2_value = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    enkoder1_value = encoder1.getValue()
    enkoder2_value = encoder2.getValue()

    # Oyun mantığını işle
    ballAnimation()
    player1Animation(enkoder1_value)
    player2Animation(enkoder2_value)

    # Ekranı temizle ve çizimleri yap
    screen.fill(bgcolor)
    printScore(screen)
    pygame.draw.aaline(screen, gamecolor, (width/2, 0), (width/2, height))
    pygame.draw.rect(screen, gamecolor, player1)
    pygame.draw.rect(screen, gamecolor, player2)
    pygame.draw.ellipse(screen, ballcolor, ball)

    pygame.display.flip()
    clock.tick(60)
