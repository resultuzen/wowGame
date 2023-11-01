from json import encoder
from time import sleep
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
import gaugette.gpio
import gaugette.rotary_encoder
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Player:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.encoderLastValue = 0

    def updatePositon(self, encoder):
        # Adim degisikligi limiti
        if abs(encoder - self.encoderLastValue) > 2:
            self.encoderLastValue = encoder
            return encoder * self.speed

        return self.encoderLastValue * self.speed


# Width - Height - Speed
Player1 = Player(20, 140, 10)
Player2 = Player(20, 140, 10)


def ballAnimation():
    global ballspeedx, ballspeedy, p1score, p2score, hit, bounce
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


def player1Animation(encoder_value):
    newPos = encoder_value * Player1.speed
    player1.y = encoder_value * Player1.speed

    if (newPos > height - (Player1.height / 2)):
        player1.y = height - (Player1.height / 2)
    if (newPos < height - (Player1.height / 2)):
        player1.y = (Player1.height / 2)


def player2Animation(encoder_value):
    newPos = encoder_value * Player2.speed
    player2.y = encoder_value * Player2.speed

    if (newPos > height - (Player2.height / 2)):
        player2.y = height - (Player2.height / 2)
    if (newPos < height - (Player2.height / 2)):
        player2.y = (Player2.height / 2)


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

encoder1_GPIO = gaugette.gpio.GPIO()
encoder2_GPIO = gaugette.gpio.GPIO()

encoder1 = gaugette.rotary_encoder.RotaryEncoder(encoder1_GPIO, ENKODER1_CLK, ENKODER1_DT)
encoder2 = gaugette.rotary_encoder.RotaryEncoder(encoder2_GPIO, ENKODER2_CLK, ENKODER2_DT)

encoder1.start()
encoder2.start()

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

player1 = pygame.Rect(width - Player1.width / 2, height /
                      2, Player1.width, Player1.height)
player2 = pygame.Rect(Player2.width / 2, height / 2,
                      Player2.width, Player2.height)

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

    # Read current states
    enkoder1_value = encoder1.get_cycles()
    enkoder2_value = encoder2.get_cycles()
    
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

pygame.quit()
sys.exit()
