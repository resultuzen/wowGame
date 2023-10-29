from time import sleep
import RPi.GPIO as GPIO
import pygame
import os
import sys
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

player1speed = 2
player2speed = 2

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
width, height = screen.get_size()
bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

ball = pygame.Rect(width/2-15, height/2-15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

p1score = 0
p2score = 0

player1 = pygame.Rect(width - 30, height // 2 - 70, 20, 140)
player2 = pygame.Rect(10, height // 2 - 70, 20, 140)

# Enkoderlerin değerlerini tutmak için değişkenler
enkoder1_value = 0
enkoder2_value = 0

# Initialize last states for both encoders
enkoder1_clkLastState = GPIO.input(ENKODER1_CLK)
enkoder2_clkLastState = GPIO.input(ENKODER2_CLK)

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

player1_target = player1.y
player2_target = player2.y

def player1Animation(enkoder1_value):
    global player1_target
    player1_target += enkoder1_value
    if player1_target < 0:
        player1_target = 0
    if player1_target > height - player1.height:
        player1_target = height - player1.height

    if player1.y < player1_target:
        player1.y += player1speed
    elif player1.y > player1_target:
        player1.y -= player1speed

def player2Animation(enkoder2_value):
    global player2_target
    player2_target += enkoder2_value
    if player2_target < 0:
        player2_target = 0
    if player2_target > height - player2.height:
        player2_target = height - player2.height

    if player2.y < player2_target:
        player2.y += player2speed
    elif player2.y > player2_target:
        player2.y -= player2speed
        
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
        else:
            enkoder1_value -= 1
    enkoder1_clkLastState = enkoder1_clk

    if enkoder2_clk != enkoder2_clkLastState:
        if enkoder2_dt != enkoder2_clk:
            enkoder2_value += 1
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
    pygame.draw.aaline(screen, gamecolor, (width/2, 0), (width/2, height))
    pygame.draw.rect(screen, gamecolor, player1)
    pygame.draw.rect(screen, gamecolor, player2)
    pygame.draw.ellipse(screen, ballcolor, ball)

    pygame.display.flip()
    clock.tick(60)
