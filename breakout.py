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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 120
BALL_SIZE = 10

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BREAKOUT")

clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH// 2 - PADDLE_HEIGHT // 2, SCREEN_HEIGHT - 40, PADDLE_HEIGHT, PADDLE_WIDTH)
        self.speed = 8

    def move (self, keys):
        if keys[pygame.K_LEFT] and self.rect.left >0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right<SCREEN_WIDTH:
            self.rect.x += self.speed
    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_WHITE, self.rect)        

#class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE , BALL_SIZE)
        self.speed_x = 4
        self.speed_y = -4
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0  or self.rect.right>= SCREEN_WIDTH:
            self.speed_x *= -1
            bounce_sound.play()
        
        if self.rect.top <=0 :
            self.speed_y *= -1
            bounce_sound.play()

        def check_collision(self, paddle):
            if self.rect.colliderect(paddle.rect):
                self.speed_y *= -1
                bounce_sound.play()
        
            def draw(self, surface):
                pygame.draw.rect(surface, COLOR_WHITE, self.rect)

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

while True:
    show_menu()
    play_again = game_loop()
    if play_again is False:
        pygame.quit()
        sys.exit()
