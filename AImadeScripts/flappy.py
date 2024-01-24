import pygame
import sys
import random

pygame.init()

# Game dimensions
WIDTH = 400
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird properties
bird_x = 50
bird_y = 300
bird_movement = 0
bird_speed = 4
bird_size = 20

# Pipe properties
pipe_width = 50
pipe_gap = 150
pipe_distance = 300
pipe_list = []

# Create a new pipe
def create_pipe():
    random_pipe_pos = random.randint(150, 450)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))  
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

# Move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Check for collisions
def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        return True
    return False

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load assets
bg_surface = pygame.image.load('background.png').convert()
bird_surface = pygame.image.load('bird.png').convert()
pipe_surface = pygame.image.load('pipe.png').convert()

# Game loop
clock = pygame.time.Clock()
score = 0
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and game_active == False:    
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 300)
                bird_movement = 0
                score = 0

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += 0.4
        bird_rect = bird_surface.get_rect(center=(bird_x, bird_y + bird_movement))
        bird_y += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = not check_collisions(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        if len(pipe_list) == 0 or pipe_list[-1].centerx == 200:
            pipe_list.extend(create_pipe())

        # Calculate score
        for pipe in pipe_list:
            if bird_x == pipe.centerx:
                score += 1

    else:
        score_surface = pygame.font.Font(None, 40).render(f'Score: {score}', True, RED)
        screen.blit(score_surface, (100, 200))

    pygame.display.update()
    clock.tick(60)