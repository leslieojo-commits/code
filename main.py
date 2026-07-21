# import libraries
import pygame
import time
import random

#--- CONSTANTS ----

# screen size
SCREEN_X = 800
SCREEN_Y = 600

# defining colors
BLACK = pygame.Color(0, 0, 0)
UI_WHITE = pygame.Color(255, 255, 255)
BTN_RED = pygame.Color (173, 19, 28)
BKGD_RED = pygame.Color (255, 117, 111)
SNAKE_GREEN = pygame.Color (88, 122, 51)
TILE_WHITE = pygame.Color (232, 232, 232)

# intializing pygame
pygame.init()

# creating game window
pygame.display.set_caption("Not Snake game")
game_window = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE) # screen size

# sets frame rate
clock = pygame.time.Clock() 



quit_game = False

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.VIDEORESIZE: # allows game window to resize
            SCREEN_X, SCREEN_Y = event.w, event.h
            game_window = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)


        game_window.fill(BKGD_RED) # draws background colour in an hidden buffer
        pygame.display.flip() # updates draw in the foreground 
pygame.quit()
