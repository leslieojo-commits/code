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
SNAKE_GREEN = pygame.Color (44, 80, 5)
TILE_WHITE = pygame.Color (232, 232, 232)
TILE_RED = pygame.Color (255, 218, 220)
FOOD_COLOUR = pygame.Color (255, 223, 0)


#TILE_RED = pygame.Color (173, 19, 28)

# Fonts (Menu)
FONT_FOLDER = "fonts"
MAIN_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Medium.ttf"
MAIN_FONT_SIZE = 40

# Menu Title Font
TITLE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Bold.ttf"
TITLE_FONT_SIZE = 70

# Score font
SCORE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Bold.ttf"
SCORE_FONT_SIZE = 20

# Button Angle
MENU_BTN_ANGLE = -5

# ========================
# INITIALIZATION
# ========================

pygame.init()

MAIN_FONT = pygame.font.Font(MAIN_FONT_PATH, MAIN_FONT_SIZE) 
TITLE_FONT = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)
SCORE_FONT = pygame.font.Font(SCORE_FONT_PATH, SCORE_FONT_SIZE)


# =======================
# CLASSES
# =======================

class Button ():
    """ Controls the button drawing, hovering states and mouse detection. """

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

    def draw (self, game_window):  
        """ Draws a rotated button that detects when it is hovered over or not. """

        #  Clears surface before drawing to prevent visual smearing
        self.surface.fill((0, 0, 0, 0))  

        #  Hover State Logic to control button color
        if self.hovered:  
            button_color = self.hover_color

        else:
            button_color = self.normal_color

        pygame.draw.rect(self.surface, button_color, (0, 0, self.w, self.h), border_radius = 15)

        #  Rendering button text and Retrieving Rectangle for button rotation design
        button_text = self.font.render(self.text, True, UI_WHITE)
        button_text_rect = button_text.get_rect(center = (self.w // 2, self.h // 2))
        self.surface.blit(button_text, button_text_rect)

        #  Rendering and Retrieving button surface and rectangle to prevent jumping 
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.rect.center)) 
        game_window.blit(rotated_surface, rotated_rect)   

    def update(self, mouse_position):  
        """ Detects whether button is hovered over or not. """

        #  Checks if mouse position is inside the button rect. and executes hovering
        if self.rect.collidepoint(mouse_position):
            self.hovered = True

        else:
            self.hovered = False

    def handle_event(self, event): 
        """ Handles event decision upon mouse click detection.  """

        # Returns positon of the mouse at the instant if it's clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            
        return False

class Screen: 
    """ Allows Children classes inherit the current methods or override them. """

    # Allows Child classes to inherit update method for processing events
    def update(self):
        pass

    #  Allows Child classes to inherit draw method to draw itself unto game_window
    def draw(self, game_window): 
        pass

    #  Allows Child classes to inherit method to decide response to events 
    def handle_event(self, event): 
        pass

    #  Allows Child classes to inherit method to update it own layout 
    #  as game_window changes size or properties
    def update_layout(self, width, height): 
        pass

class Menu(Screen):  
    """ Controls behaiviour of elements contained in the Menu (Button, Text etc.) """

    def __init__(self, screen_width, screen_height, font, normal_color, hover_color):
        """ Initializes the Menu with the necessary attributes required. """

        self.screen_width = screen_width  
        self.screen_height = screen_height
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.buttons = []
        self.angle = MENU_BTN_ANGLE
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

        #  Receives current screen width & height from the Game Class
        self.screen_width = width
        self.screen_height = height

        #  Calculates Button height & width using percentages 
        button_height = self.screen_height * 0.3
        button_width =  self.screen_width * 0.45

        #  Calculates total button height
        total_button_height = 3 * button_height

        #  Calculates spacing between each button 
        remaining_height = self.screen_height - total_button_height
        space = remaining_height / 2

        # Initial coordinates of button in Menu Screen
        x = -50
        y = 0

        # Loop to iterate and arrange all the buttons in the list
        for button in self.buttons: 
            button.w = button_width
            button.h = button_height

            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(center=(x + button.w / 2, y + button.h / 2))

            #  Updates button y position and creates the space between buttons
            y += button_height + space

        #  Calculates Title Height & Title Width
        title_x = self.screen_width * 0.85  
        title_y = self.screen_height * 0.80

        # Constant for a visual effect in the title appeareance
        spacing = 45

        #  Defines Title Text position on the Menu screen
        self.title[0].text_set_position(title_x, title_y)  
        self.title[1].text_set_position(title_x - spacing, title_y + self.title[0].rect.height - spacing )  

    def draw(self, game_window):
        """ Loops through defined list and executes their draw function. """

        for button in self.buttons:
            button.draw(game_window)
        
        for text in self.title:
            text.draw(game_window)

        #  Draws a Strikethrough line on the first text in the title list
        pygame.draw.line(game_window, BLACK, (self.title[0].rect.left, self.title[0].rect.centery),
                         (self.title[0].rect.right, self.title[0].rect.centery), 5)
        
    def update(self):
        """ Stores mouse coordinates in a variable and passes it to button. """

        mouse_position = pygame.mouse.get_pos()

        for button in self.buttons:
            button.update(mouse_position)

    def handle_event(self, event):
        """ Handles the response the button passes when it is clicked. """

        for button in self.buttons:
             if button.handle_event(event):
                 return button.text
             
        return None

class Text():
    """ Controls the attributes of the Menu Text. """

    def __init__(self, text, color, font, x, y):
        """ Initializes the Menu text with the required parameters. """

        self.text = text
        self.color = color
        self.font = font
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center = (x, y))

    def text_set_position(self, x, y):
        """ Sets Menu text position using rect. """

        self.rect.center = (x, y)
        
    def draw(self, game_window):
        """ Draws the Menu Text. """

        game_window.blit(self.surface, self.rect)

class SnakeGame(Screen):
    """ Controls Snake Screen Properties  """

    def __init__(self, screen_width, screen_height):
        """ Initializes screen width & height and initializes game board and snake. """
        self._paused = False # Set Pause to False

        self.board = None # board not created yet - workaround for update_layout

        # set initial window parameters
        self.update_layout(screen_width, screen_height)

        # Set up the Snake Game & Board
        self.board = Board(self._margin, self._margin + self._hs_bar_height, screen_width - self._margin * 2, screen_height - self._margin * 2)
        self.reset_game ()

    def reset_game(self):
        """ Responsible for Snake Game & Board set up when called. """
        self.snake = Snake()
        self.food  = Food(self.board, self.snake.body)
        self._score = 0

    def update(self):
        """ Calls a method that updates entities on the Screen. """
        if not self._paused:  # Only perform updates while the game is not paused
            # move the snake
            moved = self.snake.move(self.board)

            if not moved:
                return
            
            if self.snake.position == self.food.position:
                self.snake.growing = True
                self._score += 1
                self.food.respawn(self.board, self.snake.body)

            if self.snake.dying:
                print ("TODO exit the snake game - BORK BORK BORK!!!")


        
        
            #check_wall_collision()


            #check_self_collision


    def draw(self, game_window):
        """ draw all entities in the game. """

        self.board.draw(game_window)
        self.snake.draw(game_window, self.board)
        self.food.draw(game_window, self.board)
        self.draw_hud(game_window)

    def draw_hud(self,game_window):
        """ Draws elements of the game display no top of the board """
        score_surface = SCORE_FONT.render(f"Score: {self._score}", False, UI_WHITE)
        score_surface_rect = score_surface.get_rect()
        score_surface_rect.topleft = (self._margin, self._margin)
        pygame.draw.rect(game_window, BTN_RED, pygame.Rect(0, 0, self._screen_width, self._hs_bar_height) )
        game_window.blit(score_surface, score_surface_rect)

        # if the snake is dying, pause the game
        if self.snake.dying:
            pause_message = "GAME OVER"
            self._paused = True
        else:
            pause_message = "Paused: press any key"

        # Draw the pause if we're paused
        if self._paused:
            pause_surface = SCORE_FONT.render(pause_message, True, UI_WHITE, BTN_RED )
            pause_surface_rect = pause_surface.get_rect()
            pause_surface_rect.center = (self._screen_width // 2, self._screen_height // 2)
            game_window.blit(pause_surface, pause_surface_rect)

        
        

    def handle_event(self, event):
        """ Responsible for responding to events being triggerd. """

        #  Determines the exact moment a key transitions from pressed to released
        keys = pygame.key.get_just_released()

        if keys[pygame.K_LEFT] :
            self.snake.direction = Snake.MOVE_LEFT
        elif keys[pygame.K_RIGHT]:
           self.snake.direction = Snake.MOVE_RIGHT
        elif keys[pygame.K_UP]:
            self.snake.direction = Snake.MOVE_UP
        elif keys[pygame.K_DOWN]:
            self.snake.direction = Snake.MOVE_DOWN

        #  Handles event for pausing
        if event.type == pygame.KEYDOWN:
            if self._paused:
                self._paused = False
            elif event.key == pygame.K_PAUSE:
                self._paused = True

        #  Handles event for restart
        if event.type == pygame.KEYDOWN:
            # TODO need to ask user for restart
            if event.key == pygame.K_ESCAPE:
                # Restart the game
                self.reset_game()
        

    def update_layout(self, width, height):
        """ Receives current layout properties from Game Class and updates its entities. """

        #  Receives Screen Width & Height Properties
        self._screen_width = width
        self._screen_height = height

        #  Defines spacing for high score 
        self._margin = 20
        self._hs_bar_height = int(height * 0.12)

        #  Passes Current Screen Width & Height to the Board
        if not self.board == None:
            self.board.update_layout(self._margin, self._margin + self._hs_bar_height, width - (self._margin * 2), height - self._hs_bar_height - (self._margin * 2))

class Board:
    """ Creates the Game Board """
    def __init__(self, x, y, screen_width, screen_height):

        #  Initializes screen width & screen height 
        self.screen_width = screen_width
        self.screen_height = screen_height

        #  Defines Number of board rows and columns
        self.columns = 30
        self.rows = 18

        self.rect = pygame.Rect(0, 0, 0, 0)

        #  Calls update_layout method to process screen width and height
        self.update_layout(x, y, screen_width, screen_height)

    def update_layout(self, x, y, width, height):
        """ Responsible for handling board layout and receiving updated screen sizes. """


        # Calculation for individual cell width & height
        cell_width = width // self.columns
        cell_height = height // self.rows

        #  Ensures cell is always a square 
        self.cell_size = min(cell_width, cell_height)

        #  Defines board width & height
        board_width = self.columns * self.cell_size
        board_height = self.rows * self.cell_size

        #  Defines rectangle for board width & height
        self.rect.width = board_width
        self.rect.height = board_height

        # set position
        self.rect.x = x + ((width - board_width) // 2)
        self.rect.y = y



    def draw (self, game_window): 
        """ Draws the board tiles (cells). """

        # Nested loop to draw the board tiles
        for row in range(self.rows):

            for column in range(self.columns):

                # Defines x-coordinates of each tile
                x = self.rect.left + column * self.cell_size

                # Defines y-coordinate of each tile
                y = self.rect.top + row * self.cell_size

                tile  = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Conditional logic for grid color
                if (row + column) % 2 == 0:
                    color = TILE_WHITE
                else:
                    color = TILE_RED

                pygame.draw.rect(game_window, color, tile)

    def get_tile_rect (self, column, row): 
        """ Returns coordinate and cell size when called. """
        x = self.rect.left + column * self.cell_size
        y = self.rect.top + row * self.cell_size

        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def valid_tile(self, tile_pos):
        column, row = tile_pos
        """ Returns if the tile is inside the board. (used for snake death) """
        if column < 0 or column >= self.columns or row < 0 or row >= self.rows:
            return False
        return True


        


class Snake:
    # directional constants - rotational so we can check opposites easily
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_VECTORS = [ (0,-1), (1,0), (0,1), (-1,0)]
    SEG_HEAD = 0
    def __init__(self):
        self.body = [ (5,7), (4,7), (3,7) ]
        self._direction = self.MOVE_RIGHT
        self._direction_vector = self.MOVE_VECTORS[self._direction]
        self._color = SNAKE_GREEN
        self._growing = False
        self._dying = False
        self._move_delay = 0.5 # snake defaults to 1 second - fix this to be defined by the GAME
        self._next_move = time.time() + self._move_delay


    def draw(self, game_window, board):
        for column, row in self.body:

            # Get the correct rectangle for this position in the board
            tile = board.get_tile_rect(column, row)
            pygame.draw.rect(game_window, self._color, tile)

    def move(self, board):
        if time.time() > self._next_move:
            head_column, head_row = self.body[0]
            direction_column, direction_row = self._direction_vector

            new_head = (head_column + direction_column, head_row + direction_row)
            self.body.insert(0, new_head)
            if self._growing:
                # keep the tail for this movement, then stop growing 
                self._growing = False
            else:
                self.body.pop()

            # set next move time
            self._next_move = time.time() + self._move_delay
            if not board.valid_tile(self.body[0]):
                self.dying = True
                
            return True
        
        return False
        
    def get_direction(self):
        """ return the current direction """
        return self._direction
    def set_direction(self, dir):
        """ set the current direction"""
        # is it a valid direction
        if dir in [0,1,2,3]:
            # check if reversing with a mod operation
            if not dir + 2 % 4 == self._direction: # Thsi is a correct solution but i can use it for now to do invalid code and stuff if not (dir + 2) % 4 != self._direction
            #if not (dir+ 2) % 4 != self._direction:   
                # set the direction and the vector
                self._direction = dir
                self._direction_vector = self.MOVE_VECTORS[self._direction]
    # property declaration for convenience
    direction = property(get_direction, set_direction)

    # property functions for internal "_growing" status
    def get_growing(self):
        return self._growing
    def set_growing(self, grow):
        # check for boolean type  
        if type(grow).__name__ == "bool":
            self._growing = grow
    growing = property( get_growing, set_growing )

    # Property Function to return snake positon
    def get_position(self):
        return self.body[self.SEG_HEAD]
    position = property(get_position)

    # Property Functions to get and set snake dying 
    def get_dying(self):
        return self._dying 
    def set_dying(self, die):
    # check for boolean type  
        if type(die).__name__ == "bool":
            self._dying = die
    dying = property( get_dying , set_dying )


class Food:
    """ Responsible for Food attributes. """

    def __init__(self, board, snake_body):
        """ Initializes the food parameters. """
        #self.position = (column, row)
        self.color = FOOD_COLOUR
        self.respawn (board, snake_body)

    def draw(self, game_window, board):
        """ Draws Food. """
        column, row = self.position
        tile = board.get_tile_rect(column, row)
        pygame.draw.rect (game_window, self.color, tile)
        pygame.draw.rect (game_window, BLACK, tile, width = 1)

    def respawn(self, board, snake_body):
        """ Spawns food at random unnoccupied positions. """
        column = random.randint(0, board.columns - 1)
        row = random.randint(0, board.rows -1)
        position = (column, row)

        while position in snake_body:
            column = random.randint(0, board.columns -1)
            row = random.randint(0, board.rows - 1)
            position = (column, row)

        self.position = position
    
           
        

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
        """ main event processing loop"""

        # procdess event list
        for event in pygame.event.get():
            # quitting?
            if event.type == pygame.QUIT:
                self.running = False
            # window resize
            elif event.type == pygame.VIDEORESIZE:

                self.width = event.w
                self.height = event.h 

                self.game_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

                self.menu.update_layout(self.width, self.height)
                self.snake_game.update_layout(self.width, self.height)

            # handle the current screen's events
            action = self.current_screen.handle_event(event)
            # button click
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
