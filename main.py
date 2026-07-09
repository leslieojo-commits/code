# import libraries
import pygame
import time
import random

# ======================
# CONSTANTS
# ======================

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

# Button Angle
MENU_ANGLE = -5

# =======================
# CLASSES
# =======================

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
        self.rect = self.surface.get_rect(topleft = (self.x, self.y)) # creates the rectangle

    def button_draw (self, game_window, text):  # draws text unto button and rotates button
        self.surface.fill(self.color)
        button_text = self.font.render(text, True, UI_WHITE)
        button_text_rect = button_text.get_rect(center = (self.w // 2, self.h // 2))
        self.surface.blit(button_text, button_text_rect)

        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.rect.center))
        game_window.blit(rotated_surface, rotated_rect)

class Menu():   # Menu Class
    def __init__(self, screen_width, screen_height, font, color):
        self.screen_width = screen_width  # why do we need to pass this if we don't need to pass angle
        self.screen_height = screen_height
        self.font = font
        self.color = color
        self.buttons = []
        self.angle = MENU_ANGLE

    def create_buttons(self):  # Make the buttons
        play_button = Button(0, 0, 300, 100, self.color, self.font, self.angle)
        setting_button = Button(0, 0, 300, 100, self.color, self.font, self.angle)
        tutorial_button = Button(0, 0, 300, 100, self.color, self.font, self.angle)
        self.buttons.extend([play_button, setting_button, tutorial_button])

    def update_layout(self): 
        button_height = self.screen_height * 0.3
        button_width =  self.screen_width * 0.35

        total_button_height = 3 * button_height
        remaining_height = self.screen_height - total_button_height
        space = remaining_height / 2

        x = -50
        y = 0

        for button in self.buttons:
            button.w = button_width
            button.h = button_height

            button.x = x
            button.y = y

            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(center=(x + button.w / 2, y + button.h / 2))

            y += button_height + space
            

# ========================
# INITIALIZATION
# ========================

pygame.init()

pygame.display.set_caption("Not Snake game")
game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) # screen size

MAIN_FONT = pygame.Font(MAIN_FONT, MAIN_FONT_SIZE) 
clock = pygame.time.Clock() # sets frame rate

# Menu 
menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_FONT, BTN_RED)
menu.create_buttons()
menu.update_layout()

#buttons
#play_button = Button(-50, 50, 300, 100, BTN_RED, MAIN_FONT, angle= MENU_ANGLE)

# ========================
#  GAME LOOP 
# ========================

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.VIDEORESIZE: # allows game window to resize
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            menu.screen_height = SCREEN_HEIGHT
            menu.screen_width = SCREEN_WIDTH
            menu.update_layout()

        game_window.fill(BKGD_RED) # draws background colour in an hidden buffer
        menu.buttons[0].button_draw(game_window, "Play")
        menu.buttons[1].button_draw(game_window, "Setting")
        menu.buttons[2].button_draw(game_window, "Tutorial")
        #play_button.button_draw(game_window, "Play")
        pygame.display.flip() # updates draw in the foreground 
pygame.quit()
