import pygame
import sys

# Oyun ekranı boyutları
WIDTH, HEIGHT = 800, 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Oyuncu özellikleri
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 100
PLAYER_SPEED = 5

# Pygame'in başlatılması
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Oyuncuların konumları
player1_pos = [50, HEIGHT // 2 - PLAYER_HEIGHT // 2]
player2_pos = [WIDTH - 50 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2]

# Oyuncuların hareket yönleri
player1_move_up = False
player1_move_down = False
player2_move_up = False
player2_move_down = False

# Topun konumu ve hızı
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_dir = [5, 5]

# Kart okuma kontrolü
card_read = False

# Oyun süresi
game_duration = 30  # 30 saniye
start_time = None

# Ana oyun döngüsü
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                card_read = True
                print("Kart okundu! İyi oyunlar!")
                start_time = pygame.time.get_ticks() / 1000  # Başlangıç zamanını al

            elif event.key == pygame.K_w:
                player1_move_up = True
            elif event.key == pygame.K_s:
                player1_move_down = True
            elif event.key == pygame.K_UP:
                player2_move_up = True
            elif event.key == pygame.K_DOWN:
                player2_move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1_move_up = False
            elif event.key == pygame.K_s:
                player1_move_down = False
            elif event.key == pygame.K_UP:
                player2_move_up = False
            elif event.key == pygame.K_DOWN:
                player2_move_down = False

    if card_read:
        # Oyuncu hareketleri
        if player1_move_up:
            player1_pos[1] -= PLAYER_SPEED
        if player1_move_down:
            player1_pos[1] += PLAYER_SPEED
        if player2_move_up:
            player2_pos[1] -= PLAYER_SPEED
        if player2_move_down:
            player2_pos[1] += PLAYER_SPEED

        # Ekran sınırları
        player1_pos[1] = max(0, min(player1_pos[1], HEIGHT - PLAYER_HEIGHT))
        player2_pos[1] = max(0, min(player2_pos[1], HEIGHT - PLAYER_HEIGHT))

        # Topun hareketi
        ball_pos[0] += ball_dir[0]
        ball_pos[1] += ball_dir[1]

        # Topun çarpışmaları
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT:
            ball_dir[1] *= -1
        if ball_pos[0] <= player1_pos[0] + PLAYER_WIDTH and \
                player1_pos[1] <= ball_pos[1] <= player1_pos[1] + PLAYER_HEIGHT:
            ball_dir[0] *= -1
        if ball_pos[0] >= player2_pos[0] - PLAYER_WIDTH and \
                player2_pos[1] <= ball_pos[1] <= player2_pos[1] + PLAYER_HEIGHT:
            ball_dir[0] *= -1
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            ball_pos = [WIDTH // 2, HEIGHT // 2]

        # Ekran temizleme
        screen.fill(BLACK)

        # Oyuncuları çizme
        pygame.draw.rect(screen, WHITE, pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.rect(screen, WHITE, pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))

        # Topu çizme
        pygame.draw.circle(screen, WHITE, (ball_pos[0], ball_pos[1]), 10)

        # Süre kontrolü
        if start_time is not None:
            elapsed_time = (pygame.time.get_ticks() / 1000) - start_time
            remaining_time = max(0, game_duration - elapsed_time)
            if remaining_time <= 0:
                print("Süreniz bitti!")
                running = False
            else:
                print(f"Kalan süre: {remaining_time} saniye")

        # Ekranı güncelleme
        pygame.display.flip()
        clock.tick(60)

# Temizlik
pygame.quit()
sys.exit()
