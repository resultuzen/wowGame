import os, sys, random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import RPi.GPIO as GPIO
from time import sleep

def ballAnimation():
    global ballspeedx, ballspeedy, opponentspeed, pscore, oscore, hit, bounce
    ball.x += ballspeedx
    ball.y += ballspeedy
    if ball.top <= 0 or ball.bottom >= height: 
        ballspeedy *= -1
        bounce.play()
    if ball.centerx <= 15 or ball.centerx >= width - 15: 
        if ball.centerx < width/2 :
            pscore += 1
        else:
            oscore += 1
        goal.play()
        ballRestart()
        pygame.time.delay(1000)
    if ball.colliderect(player): 
        ballspeedx *= -1
        hit.play()
    if ball.colliderect(opponent):
        ballspeedx *= -1
        opponentspeed = random.choice((3, 7))
        hit.play()

def ballRestart():
    global ballspeedx, ballspeedy, start
    ball.center = (width/2, height/2)
    start.play()
    ballspeedx = 7 * random.choice((1, -1))
    ballspeedy = 7 * random.choice((1, -1))

def playerAnimation(enkoder_value):
    player.y += enkoder_value * playerspeed
    if player.top <= 0: player.top = 0
    if player.bottom >= height: player.bottom = height

def opponentAI(enkoder_value):
    if opponent.bottom < ball.centery : opponent.centery += enkoder_value * opponentspeed
    if opponent.top > ball.centery : opponent.centery -= enkoder_value * opponentspeed
    if opponent.top <= 0 : opponent.top = 0
    if opponent.bottom >= height : opponent.bottom = height

def printScore(surface):
    global pscore, oscore
    font = pygame.font.Font(None, 72)
    text = font.render(str(oscore), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2-30, 42)
    surface.blit(text, textRect)
    text = font.render(str(pscore), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2+30, 42)
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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

width, height = screen.get_size()

pygame.display.set_caption("Test")

bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

ball = pygame.Rect(width/2-15, height/2-15, 30, 30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

player = pygame.Rect(width-30, height/2-70, 20, 140)
playerspeed = 0

opponent = pygame.Rect(10, height/2-70, 20, 140)
opponentspeed = 5

pscore = 0
oscore = 0

# Enkoderlerin değerlerini tutmak için değişkenler
enkoder1_value = 0
enkoder2_value = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Her iki enkoderin değerlerini oku
    enkoder1_clk = GPIO.input(ENKODER1_CLK)
    enkoder1_dt = GPIO.input(ENKODER1_DT)
    enkoder2_clk = GPIO.input(ENKODER2_CLK)
    enkoder2_dt = GPIO.input(ENKODER2_DT)

    # Her iki enkoder için dönüş değerlerini hesapla
    if enkoder1_clk != enkoder1_dt:
        if enkoder1_clk:
            enkoder1_value += 1
        else:
            enkoder1_value -= 1

    if enkoder2_clk != enkoder2_dt:
        if enkoder2_clk:
            enkoder2_value += 1
        else:
            enkoder2_value -= 1

    # Oyun mantığını işle
    ballAnimation()
    playerAnimation(enkoder1_value)
    opponentAI(enkoder2_value)

    # Ekranı temizle ve çizimleri yap
    screen.fill(bgcolor)
    printScore(screen)
    pygame.draw.aaline(screen, gamecolor, (width/2, 0), (width/2, height))
    pygame.draw.rect(screen, gamecolor, player)
    pygame.draw.rect(screen, gamecolor, opponent)
    pygame.draw.ellipse(screen, ballcolor, ball)

    pygame.display.flip()
    clock.tick(60)
