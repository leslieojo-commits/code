# import libraries
import pygame
import time
import random

# ==============
# CONSTANTS
# ==============

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = pygame.Color(0, 0, 0)
UI_WHITE = pygame.Color(255, 255, 255)
BTN_RED = pygame.Color (173, 19, 28)
BKGD_RED = pygame.Color (255, 117, 111)
SNAKE_GREEN = pygame.Color (88, 122, 51)
TILE_WHITE = pygame.Color (232, 232, 232)

# Fonts
FONT_FOLDER = "fonts"
MAIN_FONT = f"{FONT_FOLDER}\\Poppins-Medium.ttf"
MAIN_FONT_SIZE = 30


# ==============
# CLASSES
# ==============

class Button ():    # Button Class
    #NORMAL_ANGLE = 0
    #MAIN_MENU_ANGLE = 15 

    #BUTTON_FONT_FOLDER = "fonts"
    #BUTTON_FONT = f"{BUTTON_FONT_FOLDER}\\Poppins-Medium.ttf"
    #FONT_SIZE = 20

    def __init__(self, x, y, w, h, color, font, angle=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.font = font
        self.angle = angle # rotatation angle

        self.surface = pygame.Surface((w, h), pygame.SRCALPHA) # creates the button surface
        self.rect = self.surface.get_rect(topleft = (-5, 0)) # creates the rectangle

    def button_draw (self, game_window, text):  # draws text unto button and rotates button
        self.surface.fill(self.color)
        button_text = self.font.render(text, True, UI_WHITE)
        button_text_rect = button_text.get_rect(center = (self.w // 2, self.h // 2))
        self.surface.blit(button_text, button_text_rect)

        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.rect.center))
        game_window.blit(rotated_surface, rotated_rect)



# ==============
# INITIALIZATION
# ==============

pygame.init()
pygame.display.set_caption("Not Snake game")
game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) # screen size

MAIN_FONT = pygame.Font(MAIN_FONT, MAIN_FONT_SIZE) 
clock = pygame.time.Clock() #Sets frame rate

#buttons
play_button = Button( 100, 100, 300, 100, BTN_RED, MAIN_FONT, angle= -5)

# --- Game Loop ---

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.VIDEORESIZE: # allows game window to resize
            SCREEN_X, SCREEN_Y = event.w, event.h
            game_window = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)
        #blah_blah = main_font.render("Blah Blah", SNAKE_GREEN, UI_WHITE)
        #blah_blah_rect = blah_blah.get_rect()
        #blah_blah_rect.center = ( SCREEN_X // 2, SCREEN_Y //2 )

        game_window.fill(BKGD_RED) # draws background colour in an hidden buffer
        play_button.button_draw(game_window, "Play")
        #game_window.blit(blah_blah, blah_blah_rect)
        pygame.display.flip() # updates draw in the foreground 
pygame.quit()
