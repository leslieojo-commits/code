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
BTN_HOVER_RED = pygame.Color (210, 60, 40)
BKGD_RED = pygame.Color (255, 117, 111)
SNAKE_GREEN = pygame.Color (88, 122, 51)
TILE_WHITE = pygame.Color (232, 232, 232)

# Fonts
FONT_FOLDER = "fonts"
MAIN_FONT = f"{FONT_FOLDER}\\Poppins-Medium.ttf"
MAIN_FONT_SIZE = 40

TITLE_FONT = f"{FONT_FOLDER}\\Poppins-Bold.ttf"
TITLE_FONT_SIZE = 70

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

    

    def __init__(self, text, x, y, w, h, normal_color, hover_color, font, angle=0):
        self.w = w
        self.h = h
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.font = font
        self.text = text
        self.angle = angle # rotation angle
        self.hovered = False

        self.surface = pygame.Surface((w, h), pygame.SRCALPHA) # creates the button surface
        self.rect = self.surface.get_rect(topleft = (x, y)) # creates the rectangle

    def button_draw (self, game_window):  # draws text unto button and rotates button
        self.surface.fill((0, 0, 0, 0))
        if self.hovered:
            button_color = self.hover_color

        else:
            button_color = self.normal_color

        pygame.draw.rect(self.surface, button_color, (0, 0, self.w, self.h), border_radius = 15)
        button_text = self.font.render(self.text, True, UI_WHITE)
        button_text_rect = button_text.get_rect(center = (self.w // 2, self.h // 2))
        self.surface.blit(button_text, button_text_rect)

        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.rect.center))
        game_window.blit(rotated_surface, rotated_rect)


            

    def update(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            self.hovered = True

        else:
            self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            
        return False

class Screen:
    def update(self):
        pass

    def draw(self, game_window):
        pass

    def handle_event(self, event):
        pass

    def update_layout(self):
        pass

class Menu(Screen):   # Menu Class
    def __init__(self, screen_width, screen_height, font, normal_color, hover_color):
        self.screen_width = screen_width  # why do we need to pass this if we don't need to pass angle
        self.screen_height = screen_height
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.buttons = []
        self.angle = MENU_ANGLE
        self.title = [
            Text("Not", BLACK, TITLE_FONT, 0, 0),
            Text("Snake", BLACK, TITLE_FONT, 0, 0)
        ]

    def create_buttons(self):  # Make the buttons
        play_button = Button("Play", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font, self.angle)
        setting_button = Button("Settings", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font, self.angle)
        quit_button = Button("Quit", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font,  self.angle)
        self.buttons.extend([play_button, setting_button, quit_button])

    def update_layout(self, width, height):

        self.screen_width = width
        self.screen_height = height

        button_height = self.screen_height * 0.3
        button_width =  self.screen_width * 0.45

        total_button_height = 3 * button_height
        remaining_height = self.screen_height - total_button_height
        space = remaining_height / 2

        x = -50
        y = 0

        for button in self.buttons:
            button.w = button_width
            button.h = button_height

            #button.x = x
            #button.y = y

            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(center=(x + button.w / 2, y + button.h / 2))

            y += button_height + space

        title_x = self.screen_width * 0.85
        title_y = self.screen_height * 0.80
        spacing = 45
        self.title[0].text_set_position(title_x, title_y)
        self.title[1].text_set_position(title_x - spacing, title_y + self.title[0].rect.height - spacing )

    def draw(self, game_window):
        for button in self.buttons:
            button.button_draw(game_window)
        
        for text in self.title:
            text.text_draw(game_window)

        pygame.draw.line(game_window, BLACK, (self.title[0].rect.left, self.title[0].rect.centery),
                         (self.title[0].rect.right, self.title[0].rect.centery), 5)
        
    def update(self):
        mouse_position = pygame.mouse.get_pos()

        for button in self.buttons:
            button.update(mouse_position)

    def handle_event(self, event):
        for button in self.buttons:
             if button.handle_event(event):
                 return button.text
             
        return None

class Text():
    def __init__(self, text, color, font, x, y):
        self.text = text
        self.color = color
        self.font = font
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center = (x, y))

    def text_set_position(self, x, y):
        self.rect.center = (x, y)
        
    def text_draw(self, game_window):
        game_window.blit(self.surface, self.rect)

class SnakeGame(Screen):

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.board = Board(screen_width, screen_height)

    def update(self):
        pass

    def draw(self, game_window):
        self.board.draw(game_window)

    def handle_event(self, event):
        pass

    def update_layout(self, width, height):
        
        self.board.screen_width = width
        self.board.screen_height = height

        self.board.update_layout()

class Board:

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.width = 400
        self.height = 400

        self.color = UI_WHITE

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.update_layout()

    def update_layout(self):

        board_size = min(self.screen_width, self.screen_height) * 0.9

        self.width = board_size
        self.height = board_size

        self.rect.width = self.width
        self.rect.height = self.height

        self.rect.center = (self.screen_width // 2, self.screen_height // 2)


    def draw (self, game_window):
        pygame.draw.rect(game_window, UI_WHITE, self.rect)
        

class Game:
    def __init__(self):
        self.running = True

        self.clock = pygame.time.Clock()

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.game_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        self.menu = Menu(self.width, self.height, MAIN_FONT, BTN_RED, BTN_HOVER_RED)

        self.menu.create_buttons()
        self.menu.update_layout(self.width, self.height)

        self.snake_game = SnakeGame(self.width, self.height)

        self.current_screen = self.menu

    def process_events(self):
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:

                self.width = event.w
                self.height = event.h 

                self.game_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

                self.current_screen.update_layout(self.width, self.height)

            action = self.current_screen.handle_event(event)

            if action == "Play":
                self.current_screen = self.snake_game

            elif action == "Settings":
                print ("Settings")

            elif action == "Quit":
                self.running = False

    def update (self):
        self.current_screen.update()

    def draw (self):
        self.game_window.fill(BKGD_RED)
        self.current_screen.draw(self.game_window)

    def render (self):
        pygame.display.flip()
        self.clock.tick(60)



# ========================
# INITIALIZATION
# ========================

pygame.init()

pygame.display.set_caption("Not Snake game")

MAIN_FONT = pygame.font.Font(MAIN_FONT, MAIN_FONT_SIZE) 
TITLE_FONT = pygame.font.Font(TITLE_FONT, TITLE_FONT_SIZE)


#buttons
#play_button = Button(-50, 50, 300, 100, BTN_RED, MAIN_FONT, angle= MENU_ANGLE)

# ========================
#  GAME LOOP 
# ========================

game = Game()

while game.running:

    game.process_events()

    game.update()

    game.draw()

    game.render()

pygame.quit()
