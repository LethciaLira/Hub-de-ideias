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
COLOR_ORANGE = (255, 190, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (0 , 0, 255)

# Tabela de aceleração por cor
speed_boost = {
    COLOR_YELLOW: 1.1,  
    COLOR_GREEN: 1.2,   
    COLOR_ORANGE: 1.3, 
    COLOR_RED: 1.4      



# Constants
SCREEN_WIDTH = 890
SCREEN_HEIGHT = 940
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 14
BALL_SIZE = 10
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 10

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BREAKOUT")

clock = pygame.time.Clock()

# Function for menu
def show_menu():
    waiting = True
    while waiting:
        screen.fill(COLOR_BLACK)
        title_text = menu_font.render("BREAKOUT", True, COLOR_WHITE)
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
def create_blocks(rows=8, cols=14, spacing=5, top_offset=200):
    blocks = []
    colors = [COLOR_RED, COLOR_ORANGE, COLOR_GREEN, COLOR_YELLOW]
    for row in range(rows):
        for col in range(cols):
            x = col * (BLOCK_WIDTH + spacing) 
            y = row * (BLOCK_HEIGHT + spacing) + top_offset
            rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            color = colors[(row // 2) % len(colors)]
            blocks.append({"rect": rect, "color": color, "visible": True})
           # blocks.append(blocks   
    return blocks

# Loop do jogo
def game_loop():
    paddle = pygame.Rect(SCREEN_WIDTH//2 - PADDLE_WIDTH//2,  # x: centro horizontal
    SCREEN_HEIGHT - 50,                 # y: próximo à parte inferior da tela
    PADDLE_WIDTH,
    PADDLE_HEIGHT)
    paddle_color = COLOR_BLUE
    ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4,4]
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
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += 7
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 7

        # Movimento da bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Colisão com topo/baixo
        if ball.top <= 0:
            ball_speed[1] *= -1
            if bounce_sound: bounce_sound.play()

        # Colisão com paddle
        if ball.colliderect(paddle):
            ball_speed[1] *= -1
            # Calcula onde a bola bateu na paddle
            hit_pos = (ball.centerx - paddle.left) / PADDLE_WIDTH  # valor entre 0 e 1
            # Ajusta a velocidade horizontal proporcionalmente
            ball_speed[0] = (hit_pos - 0.5) * 10
            if bounce_sound: bounce_sound.play()

        #Colisão com laterais
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed[0] *= -1
            if bounce_sound: bounce_sound.play()

        # Colisão com blocos
        for block in blocks:
            if block["visible"] and ball.colliderect(block["rect"]): 
                block["visible"] = False
                
                ball_speed[0] *= -1
                  # Descobre o lado da colisão
                if abs(ball.bottom - block["rect"].top) < 10 and ball_speed[1] > 0:
                    # bateu por cima
                    ball_speed[1] *= -1
                elif abs(ball.top - block["rect"].bottom) < 10 and ball_speed[1] < 0:
                    # bateu por baixo
                    ball_speed[1] *= -1
                elif abs(ball.right - block["rect"].left) < 10 and ball_speed[0] > 0:
                    # bateu pela esquerda
                    ball_speed[0] *= -1
                elif abs(ball.left - block["rect"].right) < 10 and ball_speed[0] < 0:
                    # bateu pela direita
                    ball_speed[0] *= -1
                
                if block["color"] in speed_boost:
                    ball_speed[0] *= speed_boost[block["color"]]
                    ball_speed[1] *= speed_boost[block["color"]]
                if block["color"] ==  COLOR_YELLOW:
                    score += 1
                elif block["color"] ==  COLOR_ORANGE:
                    score += 3
                elif block["color"] ==  COLOR_GREEN:
                    score += 5
                elif block["color"] ==  COLOR_RED:
                    score += 7
                    # Limite de velocidade para não ficar impossível
                   # Velocidade máxima por cor (não acumula)
                max_speed_by_color = {
                    COLOR_YELLOW: 5,
                    COLOR_GREEN: 6,
                    COLOR_ORANGE: 7,
                    COLOR_RED: 8
                }
                if block["color"] in max_speed_by_color:
                    ball_speed[0] = max_speed_by_color[block["color"]] * (1 if ball_speed[0] > 0 else -1)
                    ball_speed[1] = max_speed_by_color[block["color"]] * (1 if ball_speed[1] > 0 else -1)


                if score_sound: 
                    score_sound.play()
                break

        # Fim de jogo se a bola sair pela esquerda ou direita
        if ball.bottom >= SCREEN_HEIGHT:
            running = False

        # --- Desenho ---
        screen.fill(COLOR_BLACK)

        # Paddle
        pygame.draw.rect(screen, paddle_color, paddle)

        # Bola
        pygame.draw.ellipse(screen, COLOR_WHITE, ball)

        # Blocos
        for block in blocks:
            if block["visible"]:
                pygame.draw.rect(screen, block["color"], block["rect"])
        # Faz o score piscar
        time_now = pygame.time.get_ticks()
        if (time_now // 500) % 2 == 0:  
            score_color = COLOR_WHITE
        else:
            score_color = COLOR_BLACK        
        # Score
        score_text = score_font.render(f"1:", True, COLOR_WHITE)
        screen.blit(score_text, (50, 20))
        score_text = score_font.render(f" {score} ", True, score_color)
        screen.blit(score_text, (150, 20))
        score2_text = score_font.render("2: 000", True, COLOR_WHITE)
        screen.blit(score2_text, (500, 20))
       

        pygame.display.flip()

    return True

# Main loop
while True:
    show_menu()
    play_again = game_loop()
    if play_again is False:
        pygame.quit()
        sys.exit()

