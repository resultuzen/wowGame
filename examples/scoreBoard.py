import pygame
import sys

# Pygame'i başlat
pygame.init()

# Pencere boyutları
width, height = 800, 150 #800 x 150

# Pencere oluştur
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Skor Tablosu")

# Arkaplan resmi yükle
background = pygame.image.load("background.png")  # Arkaplan resminin adını uygun bir şekilde değiştirin

# Font tanımla
font = pygame.font.Font(None, 100)

# Başlangıç skoru
score = 0
hedefZaman = 3

clock = pygame.time.Clock() 

while True:

    calismaDurumu = True
    baslangicZamani = pygame.time.get_ticks()  # Oyunun başladığı zamanı kaydet

    while calismaDurumu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Skoru güncelle
        gecenSure = (pygame.time.get_ticks() - baslangicZamani) // 1000  # Oyunun başladığı zamandan geçen süre
        kalanSure = hedefZaman - gecenSure
        
        if gecenSure >= hedefZaman: #3 saniyeden fazla ise
            calismaDurumu = False

        score += 1

        # Arkaplanı ekrana çiz
        screen.blit(background, (0, 0))

        # Skoru metin olarak oluştur
        score_text = font.render("{}".format(score), True, (255, 255, 255))
        time_text = font.render("{}".format(kalanSure), True, (255, 255, 255))

        # Metni ekrana çiz
        screen.blit(score_text, (140, 44))
        screen.blit(time_text, (375, 44))
        screen.blit(score_text, (665, 44))

        # Ekranı güncelle
        pygame.display.flip()
        pygame.time.delay(1000)
        clock.tick(60)

    pygame.quit()
    sys.exit()