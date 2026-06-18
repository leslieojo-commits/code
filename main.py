''' FIRST DRAFT VERSION OF MY SNAKE GAME '''
# test update from personal machine

import pygame
import time
import random
pygame.init()

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
WHITE = (255,255, 255)

# Snake Size 
snake_x = 490
snake_y = 250

#Food Size
food_x = 490
food_y = 250

# time-based snake movement
clock = pygame.time.Clock()

#Snake size/movement coordinates
snake_x_change = 0
snake_y_change = 0

# Game Over MSG
font = pygame.font.Font("freesansbold.ttf", 50)

# Food randomizer
food_x = round(random.randrange(20,1000-20)/20)*20

#Function for displaying Game Over message
def message (msg, txt_colour):
    txt = font.render(msg, True, txt_colour)
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)

quit_game = False

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -20
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = 20
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_x_change = 0
                snake_y_change = -20
            elif event.key == pygame.K_DOWN:
                snake_x_change = 0
                snake_y_change = 20

    #increments
    snake_x += snake_x_change
    snake_y += snake_y_change

            # Code to quit fame, once bounds is reached
    if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
        quit_game = True


    # Drawing Background
    screen.fill (GREEN)
    pygame.draw.circle  (screen, RED, (snake_x, snake_y), 10)               #Temporarily making this more circular, because it looks sort of nicer
    #pygame.draw.rect(screen, RED, [snake_x, snake_y, 20, 20]) 

    # Drawing food
    pygame.draw.circle  (screen, BLACK, (food_x, food_y), 10)

    # Drawing snake rectangles
    pygame.display.update()

    clock.tick (10)

message ("Game over!", BLACK)
pygame.display.update()
time.sleep(1)

pygame.quit()
