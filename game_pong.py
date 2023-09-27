import os, sys, random, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Board(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.width = 10
        self.image = pygame.Surface([self.width,self.game.height])
        self.image.fill(self.game.boardcolor)
        self.rect = self.image.get_rect()
        self.rect.center = [self.game.width * 0.5,self.game.height * 0.5]

class Ball(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.size = 40
        self.x = self.game.width * 0.5
        self.y = self.game.height * 0.5
        self.speedx = 0
        self.speedy = 0
        self.ball = pygame.image.load('ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.ball, (self.size,self.size)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]
    def update(self):
        if self.rect.left < 0:
            self.game.p2Score += 1
            self.game.reset()
        if self.rect.right > self.game.width:
            self.game.p1Score += 1
            self.game.reset()
        if (self.rect.top < 0) or (self.rect.bottom > self.game.height):
            self.speedy *= -1    
        self.x += self.speedx * self.game.gamespeed
        self.y += self.speedy * self.game.gamespeed
        self.rect.center = [self.x,self.y]

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x):
        super().__init__()
        self.game = game
        self.width = 30
        self.height = 150
        self.x = x
        self.y = self.game.height * 0.5
        self.speed = 0
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.game.forecolor)
        self.rect = self.image.get_rect()
        self.rect.center = [self.x,self.y]
    def update(self):
        self.y += self.speed
        self.rect.center = [self.x,self.y]
        if self.rect.bottom > self.game.height : 
            self.speed = 0
            self.rect.bottom = self.game.height
        if self.rect.top < 0 : 
            self.speed = 0
            self.rect.top = 0
        if pygame.sprite.spritecollide(self,self.game.objects,False):
            self.game.ball.speedx *= -1

class Game():
    def __init__(self,screen):
        self.screen = screen
        self.width = screen.get_size()[0]
        self.height = screen.get_size()[1]
        self.bgcolor = (20,20,20)
        self.boardcolor = (80,80,80)
        self.forecolor = (255,255,255)
        self.playerspeed = 2
        self.gameOver = True
        self.SPEED_UP = pygame.USEREVENT + 1
        self.RESETSCREEN = pygame.USEREVENT + 2
        self.p1Score = 0
        self.p2Score = 0
        self.scorelimit = 5
        self.activeScreen = 0

        # game objects
        self.objects = pygame.sprite.Group()
        self.board = Board(self)
        self.objects.add(self.board)
        self.ball = Ball(self)
        self.objects.add(self.ball)
        self.players = pygame.sprite.Group()
        self.player1 = Player(self,40)
        self.player2 = Player(self,self.width - 40)
        self.players.add(self.player1)
        self.players.add(self.player2)

    def homeScreen(self):
        self.player1.y = self.height * 0.5
        self.player2.y = self.height * 0.5
        self.p1Score = 0
        self.p2Score = 0
        self.ball.x = self.width * 0.5
        self.ball.y = self.height * 0.5
        self.gameOver = True


    def newGame(self):
        self.p1Score = 0
        self.p2Score = 0
        self.reset()
        self.start()

    def endGame(self):
        self.gameOver = True
        pygame.time.set_timer(self.RESETSCREEN, 5000,True)
        
    def reset(self):
        if (self.p1Score >= self.scorelimit) or (self.p2Score >= self.scorelimit) : self.endGame()
        self.gamespeed = 1
        self.ball.x = self.width * 0.5
        self.ball.y = self.height * 0.5
        self.ball.speedx = (random.randint(0,1)*2-1) * 5
        self.ball.speedy = (random.randint(0,1)*2-1) * random.randint(3,6)
    
    def start(self):
        pygame.time.set_timer(self.SPEED_UP, 10000)
        time.sleep(0.5)
        self.gameOver = False

    def printScore(self):
        font = pygame.font.Font(None, 144)
        text = font.render(str(self.p1Score), True, self.forecolor)
        textRect = text.get_rect()
        textRect.center = (self.width/2-60,50)
        self.screen.blit(text,textRect)
        text = font.render(str(self.p2Score), True, self.forecolor)
        textRect = text.get_rect()
        textRect.center = (self.width/2+60,50)
        self.screen.blit(text,textRect)

    def update(self):

        if not(self.gameOver):
            self.players.update()
            self.objects.update()
    
    def draw(self):
        self.screen.fill(game.bgcolor)
        self.printScore()
        self.players.draw(self.screen)
        self.objects.draw(self.screen)
            
#game setup
pygame.init()
clock = pygame.time.Clock()
#screen = pygame.display.set_mode((960,640)) # %65
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("WOWLAND")
pygame.mouse.set_visible(False)

# game objects
game = Game(screen)
game.homeScreen()

while True:
    for event in pygame.event.get():
        # exit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key events
        if event.type == pygame.KEYDOWN:
            if (game.gameOver == True) and (event.key == pygame.K_RETURN):
                game.newGame()
            if not(game.gameOver):    
                if event.key == pygame.K_DOWN:
                    game.player2.speed = game.playerspeed
                if event.key == pygame.K_UP:
                    game.player2.speed = -game.playerspeed
                if event.key == pygame.K_j:
                    game.player1.speed = game.playerspeed
                if event.key == pygame.K_u:
                    game.player1.speed = -game.playerspeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                game.player2.speed = 0
            if event.key == pygame.K_u or event.key == pygame.K_j:
                game.player1.speed = 0
        # game events
        if event.type == game.SPEED_UP:
            game.gamespeed += 0.05
        if event.type == game.RESETSCREEN:
            game.p1Score = 0
            game.p2Score = 0
            game.player1.y = game.height * 0.5
            game.player2.y = game.height * 0.5
            game.players.update()
    #update logic
    game.update()

    #draw screen
    game.draw()

    pygame.display.update()
    clock.tick(120)