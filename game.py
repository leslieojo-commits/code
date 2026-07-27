# ========================
# IMPORT LIBRARIES
# ========================

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
TILE_RED = pygame.Color (173, 19, 28)

# Fonts
FONT_FOLDER = "fonts"
MAIN_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Medium.ttf"
MAIN_FONT_SIZE = 40

TITLE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Bold.ttf"
TITLE_FONT_SIZE = 70

# Button Angle
MENU_ANGLE = -5

pygame.init()

MAIN_FONT = pygame.font.Font(MAIN_FONT_PATH, MAIN_FONT_SIZE) 
TITLE_FONT = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)


# =======================
# CLASSES
# =======================

class Button ():

    """ Controls the button drawing, hovering states and mouse detection """

    #NORMAL_ANGLE = 0
    #MAIN_MENU_ANGLE = 15 

    #BUTTON_FONT_FOLDER = "fonts"
    #BUTTON_FONT = f"{BUTTON_FONT_FOLDER}\\Poppins-Medium.ttf"
    #FONT_SIZE = 20

    

    def __init__(self, text, x, y, w, h, normal_color, hover_color, font, angle=0): 

        """ Initializes a button with with a given text, color, font, and default angle initially set to zero. """

        self.w = w
        self.h = h
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.font = font
        self.text = text
        self.angle = angle  # rotation angle
        
        self.hovered = False

        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)  
        self.rect = self.surface.get_rect(topleft = (x, y))  # creates the rectangle

    def button_draw (self, game_window):  

        """ Draws a rotated button that detects when it is hovered or not. """

        self.surface.fill((0, 0, 0, 0))  # Clears surface before drawing, for future purposes like adding animation etc.

        if self.hovered:  # Hover State
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

        """ Detects whether button is hovered over or not. """

        if self.rect.collidepoint(mouse_position):
            self.hovered = True

        else:
            self.hovered = False

    def handle_event(self, event): 

        """ Detects when button is clicked """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            
        return False

class Screen: 

    """ Allows Children classes inherit the current methods or override them. """

    def update(self):
        pass

    def draw(self, game_window): # Drawing game screen
        pass

    def handle_event(self, event): # Handling click, detection and logic
        pass

    def update_layout(self, width, height): # Layout Arrangement 
        pass

class Menu(Screen):  

    """ Controls button behaviour in the Menu.
     
    Attributes:
    screen_width (float): The current screen width at the moment (depends on resizing).
    scree_height (float): The current screen height.
    font: The font in use.
    normal_color: The current color when button is not hovered.
    hover_color: The display colour when button is hovered.
    angle: The angle the button will be rotated by.
    title: The menu title (text) that will be displayed on the screen.

    """

    def __init__(self, screen_width, screen_height, font, normal_color, hover_color):

        """ Initializes the Menu with the necessary attributes required. """

        self.screen_width = screen_width  
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

    def create_buttons(self): 

        """ Creates the Menu Buttons. """

        play_button = Button("Play", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font, self.angle)
        setting_button = Button("Settings", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font, self.angle)
        quit_button = Button("Quit", 0, 0, 300, 100, self.normal_color, self.hover_color, self.font,  self.angle)
        self.buttons.extend([play_button, setting_button, quit_button])

    def update_layout(self, width, height):

        """ Creates the layout arrangement for Menu Buttons. """

        self.screen_width = width
        self.screen_height = height

        button_height = self.screen_height * 0.3
        button_width =  self.screen_width * 0.45

        total_button_height = 3 * button_height
        remaining_height = self.screen_height - total_button_height
        space = remaining_height / 2

        x = -50
        y = 0

        for button in self.buttons:  # Loop to iterate and arange all the buttons in the list
            button.w = button_width
            button.h = button_height

            #button.x = x
            #button.y = y

            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(center=(x + button.w / 2, y + button.h / 2))

            y += button_height + space

        title_x = self.screen_width * 0.85  # Logic for creating Menu Title
        title_y = self.screen_height * 0.80

        spacing = 45

        self.title[0].text_set_position(title_x, title_y)  # Draws Title at given x position
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
        self.snake = Snake()

    def update(self):
        pass

    def draw(self, game_window):
        self.board.draw(game_window)
        self.snake.draw(game_window, self.board)

    def handle_event(self, event):
        pass

    def update_layout(self, width, height):
        
        self.screen_width = width
        self.screen_height = height

        self.board.update_layout(width, height)

class Board:

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.columns = 30
        self.rows = 18

        # self.color = None

        #self.color = UI_WHITE  -- Color doesn't come from the board it comes from the conditional logic

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.update_layout(screen_width, screen_height)

    def update_layout(self, width, height):

        self.screen_width = width
        self.screen_height = height

        available_width = width * 0.90
        available_height = height * 0.82

        cell_width = available_width // self.columns
        cell_height = available_height // self.rows

        self.cell_size = min(cell_width, cell_height)

        board_width = self.columns * self.cell_size
        board_height = self.rows * self.cell_size

        self.rect.width = board_width
        self.rect.height = board_height

        self.rect.centerx = width // 2

        margin = 20

        top_bar = height * 0.12

        self.rect.top = top_bar + margin

    

    def draw (self, game_window): # nested loop to draw the board tiles
        for row in range(self.rows):

            for column in range(self.columns):

                x = self.rect.left + column * self.cell_size

                y = self.rect.top + row * self.cell_size

                tile  = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if (row + column) % 2 == 0:
                    color = TILE_WHITE
                else:
                    color = TILE_RED

                pygame.draw.rect(game_window, color, tile)

    def get_tile_rect (self, column, row): # Return (columns, rows) into coordinates when called

        x = self.rect.left + column * self.cell_size
        y = self.rect.top + row * self.cell_size

        return pygame.Rect(x, y, self.cell_size, self.cell_size)
        


class Snake:
    def __init__(self):
        self.body = [ (5,7), (4,7), (3,7) ]
        self.direction =  (1,0) 
        self.color = SNAKE_GREEN

    def draw(self, game_window, board):
        for column, row in self.body:

            tile = board.get_tile_rect(column, row)
            pygame.draw.rect(game_window, self.color, tile)

    ''' def handle_keys(self):
        keys = pygame.key.get_just_released

        if keys[pygame.K_LEFT] & self.direction != (1,0):
            self.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] & self.direction != (-1,0):
            self.direction = (1,0)
        elif keys[pygame.K_UP] & self.direction != (1,0):
            self.direction = (0,1)
        elif keys[pygame.K_DOWN] & self.direction != (0,1):
            self.direction = (0,-1) '''

    def move(self):
        head_column, head_row = self.body[0]
        direction_column, direction_row = self.direction

        new_head = (head_column + direction_column, head_row + direction_row)
        self.body.insert(0, new_head)
        self.body.pop()


        
        

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

                self.menu.update_layout(self.width, self.height)
                self.snake_game.update_layout(self.width, self.height)

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
