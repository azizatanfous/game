import pygame
import random
import sys
import numpy as np

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SIZE = 30
WIN_SCORE = 100
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 255)  # Light blue for sky
DARK_BLUE = (0, 0, 139)  # Darker blue for sky transition
GRASS_GREEN = (34, 139, 34)  # Dark green for grass

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Soccer Balls')

# Fonts and messages
font = pygame.font.Font(None, 36)
catch_messages = ["Look at you, finally making that button work!", "Awesome!", "You got it!", "Nice moves!", "Spot on!"]
miss_messages = ["Whoops!", "Missed!", "Are you playing or just sightseeing?", "Do you need glasses? Because that wasn’t even close!", "I’d call that a pass, but I don’t think the ball agrees."]

# Game variables
balls = []
catcher_x = SCREEN_WIDTH // 2
catcher_width = 100
player_speed = 20
score = 0
miss_count = 0
game_over = False
fall_speed = 5
message = ""
message_display_time = 0

# Clock for framerate control
clock = pygame.time.Clock()
FPS = 60

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_soccer_net(surface, x, y, width, height):
    """Draw a simple soccer net using lines."""
    pygame.draw.rect(surface, GREEN, (x, y, width, height), 2)
    for i in range(10):
        pygame.draw.line(surface, GREEN, (x + i * (width // 10), y), (x + i * (width // 10), y + height), 2)

def draw_gradient_background(surface, top_color, bottom_color):
    """Draw a vertical gradient from top_color to bottom_color."""
    for y in range(SCREEN_HEIGHT):
        color = tuple(map(lambda start, end: int(start + (end - start) * y / SCREEN_HEIGHT), top_color, bottom_color))
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

def draw_grass(surface, grass_color, height):
    """Draw a simple grass field at the bottom of the screen."""
    pygame.draw.rect(surface, grass_color, (0, SCREEN_HEIGHT - height, SCREEN_WIDTH, height))

def show_start_screen():
    """Show start screen until any key is pressed."""
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start_screen = False
        draw_gradient_background(screen, LIGHT_BLUE, DARK_BLUE)
        draw_grass(screen, GRASS_GREEN, 100)
        draw_text("Press any key to start.", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

show_start_screen()  # Display start screen at the beginning

# Main game loop
running = True
while running:
    draw_gradient_background(screen, LIGHT_BLUE, DARK_BLUE)
    draw_grass(screen, GRASS_GREEN, 100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:
                balls = []
                score = 0
                miss_count = 0
                game_over = False
                fall_speed = 5
                catcher_width = 100

    if not game_over:
        if random.randint(1, 100) < 3:
            balls.append([random.randint(0, SCREEN_WIDTH - BALL_SIZE), 0])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and catcher_x > 0:
            catcher_x -= player_speed
        if keys[pygame.K_RIGHT] and catcher_x < SCREEN_WIDTH - catcher_width:
            catcher_x += player_speed
        for ball in balls:
            ball[1] += fall_speed
            if ball[1] > SCREEN_HEIGHT - 50:
                if catcher_x < ball[0] + BALL_SIZE and catcher_x + catcher_width > ball[0]:
                    score += 10
                    message = random.choice(catch_messages)
                    message_display_time = 90
                else:
                    miss_count += 1
                    message = random.choice(miss_messages)
                    message_display_time = 90
                if miss_count >= 3:
                    game_over = True
                    message = "Game Over! Press Space to Restart"
                balls.remove(ball)

    if message_display_time > 0:
        draw_text(message, font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        message_display_time -= 1
    draw_soccer_net(screen, catcher_x, SCREEN_HEIGHT - 50, catcher_width, 50)
    for ball in balls:
        pygame.draw.circle(screen, BLACK, (ball[0] + BALL_SIZE // 2, ball[1] + BALL_SIZE // 2), BALL_SIZE // 2)
    draw_text(f'Score: {score}', font, WHITE, screen, SCREEN_WIDTH // 2, 20)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()





