import os, sys, random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def ballAnimation():
    global ballspeedx,ballspeedy,opponentspeed,pscore,oscore,hit,bounce
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
        opponentspeed = random.choice((3,7))
        hit.play()

def ballRestart():
    global ballspeedx, ballspeedy,start
    ball.center = (width/2,height/2)
    start.play()
    ballspeedx = 7 * random.choice((1,-1))
    ballspeedy = 7 * random.choice((1,-1))

def playerAnimation():
    player.y += playerspeed
    if player.top <= 0 : player.top = 0
    if player.bottom >= height : player.bottom = height

def opponentAI():
    if opponent.bottom < ball.centery : opponent.centery += opponentspeed
    if opponent.top > ball.centery : opponent.centery -= opponentspeed
    if opponent.top <= 0 : opponent.top = 0
    if opponent.bottom >= height : opponent.bottom = height

def printScore(surface):
    global pscore,oscore
    font = pygame.font.Font(None, 72)
    text = font.render(str(oscore), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2-30,42)
    surface.blit(text,textRect)
    text = font.render(str(pscore), True, gamecolor)
    textRect = text.get_rect()
    textRect.center = (width/2+30,42)
    surface.blit(text,textRect)

pygame.init()

clock = pygame.time.Clock()

# sound files
hit = pygame.mixer.Sound('hit.ogg')
bounce = pygame.mixer.Sound('bounce.ogg')
goal = pygame.mixer.Sound('goal.ogg')
start = pygame.mixer.Sound('start.ogg')



# screen = pygame.display.set_mode((1248,832)) # %65
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

width,height = screen.get_size()

pygame.display.set_caption("Test")

bgcolor = pygame.Color('grey12')
gamecolor = pygame.Color('white')

ball = pygame.Rect(width/2-15,height/2-15,30,30)
ballcolor = pygame.Color('white')
ballspeedx = ballspeedy = 0
ballRestart()

player = pygame.Rect(width-30,height/2-70,20,140)
playerspeed = 0

opponent = pygame.Rect(10,height/2-70,20,140)
opponentspeed = 5

pscore = 0
oscore = 0




while True:
    #inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerspeed = 7
            if event.key == pygame.K_UP:
                playerspeed = -7
        if event.type == pygame.KEYUP:
            playerspeed = 0


    #logic
    ballAnimation()
    playerAnimation()
    opponentAI()

    #drawings
    screen.fill(bgcolor)
    printScore(screen)
    pygame.draw.aaline(screen,gamecolor,(width/2,0),(width/2,height))
    pygame.draw.rect(screen,gamecolor,player)
    pygame.draw.rect(screen,gamecolor,opponent)
    pygame.draw.ellipse(screen,ballcolor,ball)

    #loop
    pygame.display.flip()
    clock.tick(50)


