import pygame
import sys
import os


pygame.init()

# Paths
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# Sounds
bounce_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "bounce.wav"))
score_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "258020__kodack__arcade-bleep-sound.wav"))

# Text
score_font = pygame.font.Font(os.path.join(ASSETS_PATH, "PressStart2P.ttf"), 44)
menu_font = pygame.font.Font(os.path.join(ASSETS_PATH, "PressStart2P.ttf"), 60)

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 860
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 120
BALL_SIZE = 10

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

while True:
    show_menu()
    play_again = game_loop()
    if play_again is False:
        pygame.quit()
        sys.exit()
