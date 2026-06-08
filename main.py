''' FIRST DRAFT VERSION OF MY SNAKE GAME '''


import pygame
import time
pygame.init

#screen name & size
pygame.display.set_caption("Not Snake game")
screen = pygame.display.set_mode((1000,720), pygame.RESIZABLE) # will need to fix the magic numbers in next version

'''-----CONSTANTS-----'''

#RGB Tuples
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#Snake Size 
snake_x = 490
snake_y = 250

#Snake size/movement coordinates
snake_x_change = 10
snake_y_change = 10

# Drawing snake rectangles
pygame.draw.rect(screen, RED, [snake_x, snake_y, 20, 20]) 

quit_game = False

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        elif event.type == pygame.K_LEFT:
            snake_x_change = -20
            snake_y_change = 0
        elif event.type == pygame.K_RIGHT:
            snake_x_change = 20
            snake_y_change = 0
        elif event.type == pygame.K_UP:
            snake_x_change = 0
            snake_y_change = -20
        elif event.type == pygame.K_DOWN:
            snake_x_change = 0
            snake_y_change = 20

    #increments
    snake_x += snake_x_change
    snake_y += snake_y_change

pygame.display.update()

# time-based snake movement
clock = pygame.time.Clock()

#Background
screen.fill (GREEN)

pygame.quit()
quit()