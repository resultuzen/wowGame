from time import sleep
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Player:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed


# Width - Height - Speed
Player1 = Player(20, 140, 20)
Player2 = Player(20, 140, 20)


def ballAnimation():
    global ballspeedx, ballspeedy, p1score, p2score, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballspeedy *= -1
        bounce.play()
    if ball.centerx <= 15 or ball.centerx >= screenWidth - 15:
        if ball.centerx < screenWidth / 2:
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
    ball.center = (screenWidth / 2, screenHeight / 2)
    start.play()
    ballspeedx = 7 * random.choice((1, -1))
    ballspeedy = 7 * random.choice((1, -1))


def player1Animation(encoder_value):
    player1.y = encoder_value * Player1.speed
    
    if player1.top <= 0: 
        player1.top = 0
        
    if player1.bottom >= player1: 
        player1.bottom = screenHeight


def player2Animation(encoder_value):
    player2.y = encoder_value * Player2.speed
    
    if player2.top <= 0: 
        player2.top = 0
        
    if player2.bottom >= player2: 
        player2.bottom = screenHeight


def printScore(surface):
    global p1score, p2score
    font = pygame.font.Font(None, 72)
    text = font.render(str(p2score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (screenWidth / 2 - 30, 42)
    surface.blit(text, textRect)
    text = font.render(str(p1score), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (screenWidth / 2 + 30, 42)
    surface.blit(text, textRect)


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
screenWidth, screenHeight = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

player1 = pygame.Rect(screenWidth - Player1.width / 2, screenHeight / 2, Player1.width, Player1.height)
player2 = pygame.Rect(Player2.width / 2, screenHeight / 2, Player2.width, Player2.height)

p1score = 0
p2score = 0

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

    # Oyun mantığını işle
    ballAnimation()
    player1Animation(enkoder1_value)
    player2Animation(enkoder2_value)

    # Ekranı temizle ve çizimleri yap
    screen.fill(bgcolor)
    printScore(screen)
    pygame.draw.aaline(screen, gamecolor, (screenWidth / 2,
                       0), (screenWidth / 2, screenHeight))
    pygame.draw.rect(screen, gamecolor, player1)
    pygame.draw.rect(screen, gamecolor, player2)
    pygame.draw.ellipse(screen, ballcolor, ball)

    pygame.display.flip()
    clock.tick(60)
