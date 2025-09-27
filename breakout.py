import pygame
import sys
import os
import random

pygame.init()

# Paths
ASSETS_PATH = os.path.join(os.getcwd(), "assets")  # use os.getcwd() para evitar erro no VSCode

# Sounds
try:
    bounce_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "bounce.wav"))
except:
    bounce_sound = None

try:
    score_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "258020_kodack_arcade-bleep-sound.wav"))
except:
    score_sound = None

# Text
try:
    score_font = pygame.font.Font(os.path.join(ASSETS_PATH, "PressStart2P.ttf"), 44)
    menu_font = pygame.font.Font(os.path.join(ASSETS_PATH, "PressStart2P.ttf"), 60)
except:
    score_font = pygame.font.SysFont("Arial", 44)
    menu_font = pygame.font.SysFont("Arial", 60)

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 860
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 120
BALL_SIZE = 10
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MyPong")

clock = pygame.time.Clock()

# Function for menu
def show_menu():
    waiting = True
    while waiting:
        screen.fill(COLOR_BLACK)
        title_text = menu_font.render("MYPONG", True, COLOR_WHITE)
        start_text = score_font.render("Press SPACE to Play", True, COLOR_WHITE)

        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 200))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 400))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Criar blocos
def create_blocks(rows=5, cols=8, spacing=10, top_offset=50):
    blocks = []
    colors = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW]
    for row in range(rows):
        for col in range(cols):
            x = col * (BLOCK_WIDTH + spacing) + 50
            y = row * (BLOCK_HEIGHT + spacing) + top_offset
            rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            color = random.choice(colors)
            blocks.append({"rect": rect, "color": color, "visible": True})
    return blocks

# Loop do jogo
def game_loop():
    paddle = pygame.Rect(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_speed = [5, 5]
    score = 0

    blocks = create_blocks()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Movimento do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle.top > 0:
            paddle.y -= 7
        if keys[pygame.K_DOWN] and paddle.bottom < SCREEN_HEIGHT:
            paddle.y += 7

        # Movimento da bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Colisão com topo/baixo
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed[1] *= -1
            if bounce_sound: bounce_sound.play()

        # Colisão com paddle
        if ball.colliderect(paddle):
            ball_speed[0] *= -1
            if bounce_sound: bounce_sound.play()

        # Colisão com blocos
        for block in blocks:
            if block["visible"] and ball.colliderect(block["rect"]):
                ball_speed[0] *= -1
                block["visible"] = False
                score += 10
                if score_sound: score_sound.play()
                break

        # Fim de jogo se a bola sair pela esquerda ou direita
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            running = False

        # --- Desenho ---
        screen.fill(COLOR_BLACK)

        # Paddle
        pygame.draw.rect(screen, COLOR_WHITE, paddle)

        # Bola
        pygame.draw.ellipse(screen, COLOR_WHITE, ball)

        # Blocos
        for block in blocks:
            if block["visible"]:
                pygame.draw.rect(screen, block["color"], block["rect"])

        # Score
        score_text = score_font.render(f"Score: {score}", True, COLOR_WHITE)
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

    return True

# Main loop
while True:
    show_menu()
    play_again = game_loop()
    if play_again is False:
        pygame.quit()
        sys.exit()
