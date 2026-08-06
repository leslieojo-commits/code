"""
Snake Game Module

This module contains the core classes and functionality 
of the Snake game.

Components include:
- Game: Controls the main game loop and screen switching logic
- Screen: Serves as parent class for each screen
- Menu: Handles the main menu interface.
- Settings: Controls the game settings such as speed.
- SnakeGame: Handles and controls snake game screen.
- Board: Creates and manges the game grid.
- Snake: Handles snake movement and drawing. 
- Button: Provides reusable UI button functionality.
- Text: Handles main menu title text.
- Food: Handles and manages food spawning and generation.
"""

# ========================
# IMPORT LIBRARIES
# ========================
import pygame
import time
import random
import json

# ========================
# JSON - File Persistence
# ========================
def load_high_score():
    """Load and returns saved high score."""
    try:
        with open ("stored_data.json", "r") as file:
            data = json.load(file) # returns the JSON file as a python dictionary 
            return data ["high_score"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0 # returns 0 if supplier function fails

def save_high_score(score):
    """Update and saves new highscore."""
    data = {
            "high_score": score
        }
    with open ("stored_data.json", "w") as file:
        # writes python dict. into Json with good spacing and alphabetical order
        json.dump (data, file, indent=4, sort_keys=True) 


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
TILE_WHITE = pygame.Color(248, 244, 244)
TILE_RED = pygame.Color (255, 218, 220)
FOOD_COLOUR = pygame.Color (255, 223, 0)

# Fonts (Menu)
FONT_FOLDER = "fonts"
MAIN_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Medium.ttf"
MAIN_FONT_SIZE = 40

# Menu Title Font
TITLE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-Bold.ttf"
TITLE_FONT_SIZE = 70

# Score font
SCORE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-SemiBold.ttf"
SCORE_FONT_SIZE = 20

# Pause font
PAUSE_FONT_PATH = f"{FONT_FOLDER}\\Poppins-SemiBold.ttf"
PAUSE_FONT_SIZE = 15

# Button Angle
MENU_BTN_ANGLE = -5

# ========================
# INITIALIZATION
# ========================
pygame.init()

# Setting Font Object
MAIN_FONT = pygame.font.Font(MAIN_FONT_PATH, MAIN_FONT_SIZE) 
TITLE_FONT = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)
SCORE_FONT = pygame.font.Font(SCORE_FONT_PATH, SCORE_FONT_SIZE)
PAUSE_FONT = pygame.font.Font(PAUSE_FONT_PATH, PAUSE_FONT_SIZE)

# =======================
# CLASSES
# =======================

class Button ():
    """Controls the button drawing, hovering states and mouse detection."""

    def __init__(self, text, x, y, w, h, normal_color, hover_color, font, angle=0): 
        """Initializes a button with with a given text, color, font, and default angle initially set to zero."""

        self._w = w
        self._h = h

        self._normal_color = normal_color
        self._hover_color = hover_color

        self._font = font
        self._text = text

        self._angle = angle  # rotation angle
        
        self._hovered = False

        self._surface = pygame.Surface((w, h), pygame.SRCALPHA)  
        self._rect = self._surface.get_rect(topleft = (x, y))  # creates the rectangle

    def draw (self, game_window):  
        """Draws a rotated button that detects when it is hovered over or not."""

        #  Clears surface before drawing to prevent visual smearing
        self._surface.fill((0, 0, 0, 0))  

        #  Hover State Logic to control button color
        if self._hovered:  
            button_color = self._hover_color

        else:
            button_color = self._normal_color

        pygame.draw.rect(self._surface, button_color, (0, 0, self._w, self._h), border_radius = 15)

        #  Rendering button text and Retrieving Rectangle for button rotation design
        button_text = self._font.render(self._text, True, UI_WHITE)
        button_text_rect = button_text.get_rect(center = (self._w // 2, self._h // 2))
        self._surface.blit(button_text, button_text_rect)

        #  Rendering and Retrieving button surface and rectangle to prevent jumping 
        rotated_surface = pygame.transform.rotate(self._surface, self._angle)
        rotated_rect = rotated_surface.get_rect(center = (self._rect.center)) 
        game_window.blit(rotated_surface, rotated_rect)   

    def get_text(self):
        """returns the text for this button"""
        return self._text

    def set_text(self, new_text):
        """update the text for this button
            expects a string
        """
        if isinstance(new_text, str):
            self._text = new_text
    text = property(get_text, set_text)

    def get_rect(self):
        """ returns the rectangle for this button """
        return self._rect

    def set_rect(self, new_rect):
        """ update the rectangke for this button
            expects a pygame rectangle
        """
        # check if it's a rectangle
        if type(new_rect).__name__ == "Rect":
            self._rect = new_rect

    rect = property(get_rect, set_rect)

    def get_surface(self):
        """returns the surface for this button"""
        return self._surface

    def set_surface(self, new_surface):
        """ update the surfacee for this button
            expects a pygame surface
        """
        # check if it's a rectangle
        if isinstance(new_surface, pygame.Surface):
            self._surface = new_surface
    surface = property(get_surface, set_surface)

    def get_w(self):
        """ returns the width for this button """
        return self._w
    def set_w(self, new_w):
        """ set the width for this button 
            expects an integer with a positive dimension"""
        if isinstance (new_w, (int, float)) and new_w > 0:
            self._w = new_w
    w = property(get_w, set_w)

    def get_h(self):
        """returns the height for this button"""
        return self._h
    def set_h(self, new_h):
        """ set the height for this button 
            expects an integer with a positve dimension"""
        if isinstance(new_h, (int, float)) and new_h > 0:
            self._h = new_h
    h = property(get_h, set_h) 


    def update(self, mouse_position):  
        """Detects whether button is hovered over or not."""

        #  Checks if mouse position is inside the button rect. and executes hovering
        if self._rect.collidepoint(mouse_position):
            self._hovered = True

        else:
            self._hovered = False

    def handle_event(self, event): 
        """Handles event decision upon mouse click detection."""

        # Returns positon of the mouse at the instant if it's clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                return True
            
        return False

class Screen: 
    """Allows Children classes inherit the current methods or override them."""

    #  Allows Child classes to inherit update method for processing events
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
    """Controls behaiviour of elements contained in the Menu (Button, Text etc.)"""
    def __init__(self, screen_width, screen_height, font, normal_color, hover_color):
        """ Initializes Menu Object with required 
            attributes (screen width & height, font, 
            normal_color, hover_color).
        """
        
        self._screen_width = screen_width  
        self._screen_height = screen_height

        self._font = font

        self._normal_color = normal_color
        self._hover_color = hover_color

        self._buttons = []
        self._angle = MENU_BTN_ANGLE

        # Menu Title
        self._title = [
            Title("Not", BLACK, TITLE_FONT, 0, 0),
            Title("Snake", BLACK, TITLE_FONT, 0, 0)
        ]

        self.create_buttons()  # creates Menu Button
        self.update_layout(screen_width, screen_height)  

    def create_buttons(self): 
        """Creates Menu buttons with the init parameters."""
        play_button = Button("Play", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font, self._angle)
        setting_button = Button("Speed", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font, self._angle)
        quit_button = Button("Quit", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font,  self._angle)
        self._buttons.extend([play_button, setting_button, quit_button])

    def update_layout(self, width, height):
        """Creates the layout arrangement for Menu Buttons."""

        # Receives current screen width & height from the Game Class update_layout method
        self._screen_width = width
        self._screen_height = height

        # Calculates resizable Button height & width using percentages 
        button_height = self._screen_height * 0.3
        button_width =  self._screen_width * 0.45

        # Calculates total button height
        total_button_height = 3 * button_height

        # Calculates spacing between each button 
        remaining_height = self._screen_height - total_button_height
        space = remaining_height / 2

        # Sets initial coordinates of button on Menu Screen
        x = -50
        y = 0

        # Iterates and arrange all the buttons in the list
        for button in self._buttons: 
            button.w = button_width
            button.h = button_height

            # creates a surfaceobject for the button and sets the position
            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(center=(x + button.w / 2, y + button.h / 2))

            #  Updates button y position and creates the space between buttons
            y += button_height + space

        # Calculates Menu title position as a percentage
        title_x = self._screen_width * 0.85  
        title_y = self._screen_height * 0.80

        # Moves [1] in title by a fixed amount 
        spacing = 45

        # Updates Title Text position on the Menu screen
        self._title[0].text_set_position(title_x, title_y)  
        self._title[1].text_set_position(title_x - spacing, title_y + self._title[0].rect.height - spacing )  

    def draw(self, game_window):
        """Draws all elements in Menu."""
        for button in self._buttons:
            button.draw(game_window)
        
        for text in self._title:
            text.draw(game_window)

        # Draws a Strikethrough line onto the first text in the title list
        pygame.draw.line(game_window, BLACK, (self._title[0].rect.left, self._title[0].rect.centery),
                         (self._title[0].rect.right, self._title[0].rect.centery), 5)
        
    def update(self):
        """Stores mouse coordinates in a variable and passes it to button."""
        mouse_position = pygame.mouse.get_pos() # gets mouse position and stores it an object  

        # Calls button update function and passes mouse position
        for button in self._buttons:
            button.update(mouse_position)

    def handle_event(self, event):
        """Handles the response the button passes when it is clicked."""
        for button in self._buttons:
             if button.handle_event(event):
                 return button.text  # returns name of clicked button to Game Class for processing 
             
        return None

class Title():
    """Controls the attributes of the Menu Title."""

    def __init__(self, text, color, font, x, y):
        """Initializes the Menu text with the required parameters."""

        self._text = text
        self._font = font

        self._color = color

        self._surface = self._font.render(self._text, True, self._color)
        self._rect = self._surface.get_rect(center = (x, y))

    def get_rect(self):
        """Returns the rectangle used to posiiton the Menu title"""
        return self._rect
    rect = property(get_rect)
    
    def text_set_position(self, x, y):
        """Sets Menu text position with rect."""
        self._rect.center = (x, y) # uses and stores rect when called
        
    def draw(self, game_window):
        """Draws the Title."""
        game_window.blit(self._surface, self._rect)

class Settings (Screen):
    """Controls the speed of the game."""

    def __init__(self, screen_width, screen_height, font, normal_color, hover_color):
        """Initializes the attributes of Settings Screen"""
        self._screen_width = screen_width
        self._screen_height = screen_height

        self._font = font

        self._normal_color = normal_color
        self._hover_color = hover_color

        self._angle = 0

        self._buttons = []

        self._selected_speed = "Normal"

        self.create_setting_buttons()
        self.update_layout(screen_width, screen_height)


    def create_setting_buttons (self):
        """Creates the Settings Buttons."""
        fast_button = Button("Fast", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font, self._angle)
        normal_button = Button("Normal", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font, self._angle)
        slow_button = Button("Slow", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font,  self._angle)
        back_button = Button("Back", 0, 0, 300, 100, self._normal_color, self._hover_color, self._font, self._angle)
        self._buttons.extend([fast_button, normal_button, slow_button, back_button])

    def update(self):
        """Stores mouse coordinates in a variable and passes it to the settings button."""

        mouse_position = pygame.mouse.get_pos() # Stores mouse position 

        for button in self._buttons:
            button.update(mouse_position)

    
    def draw(self, game_window):
        """Loops through defined list and executes their draw function."""

        # draws settings buttons
        for button in self._buttons:
            button.draw(game_window)

        # Draws text that shows selected speed choice
        selected_setting_surface = SCORE_FONT.render(f"Selected speed: {self._selected_speed}", True, UI_WHITE)
        selected_setting_rect = selected_setting_surface.get_rect(center = (self._screen_width // 2, 35))

        game_window.blit (selected_setting_surface, selected_setting_rect)
    
    def handle_event(self, event):
        """Handles (button) events in the setting screen."""
        for button in self._buttons:
            if button.handle_event(event): 

                # return button text if it is a speed option      
                if button.text in ("Fast", "Normal", "Slow"):
                    self._selected_speed = button.text # Assigns equivalent speed value based on text 
                return button.text # returns name of clicked button to Game Class for processing 
            
        return None
    
    def update_layout(self, width, height):
        """Updates the layout of elements in the Setting screen."""

        #  Receives current screen width & height from the Game Class
        self._screen_width = width
        self._screen_height = height

        #  Calculates Button height & width using percentages 
        button_height = self._screen_height * 0.15
        button_width =  self._screen_width * 0.4

        #  Calculates total button height
        total_button_height = len(self._buttons) * button_height

         #  Calculates vertical spacing between each button 
        remaining_height = self._screen_height - total_button_height
        vertical_space = remaining_height / (len(self._buttons) + 1)

        #  Defines coordinate position to start drawing the buttons
        start_x = (self._screen_width - button_width) / 2
        y = vertical_space        

        # Loop to iterate and arrange all the buttons in the list
        for button in self._buttons: 
            button.w = button_width
            button.h = button_height

            button.surface = pygame.Surface((button.w, button.h), pygame.SRCALPHA)
            button.rect = button.surface.get_rect(topleft = (start_x, y))#center=(start_x + button.w / 2, y + button.h / 2))

            #  Updates button y position and creates the space between buttons
            y += button_height + vertical_space

class SnakeGame(Screen):
    """Controls Snake Game Screen Properties."""

    def __init__(self, screen_width, screen_height, move_delay):
        """Initializes screen width & height and initializes game board and snake."""
        self._paused = False # Set Pause to False

        # Allows update_layout to create the board
        self._board = None 

        # Sets up high score for game over
        self._high_score = load_high_score()

        # Sets up game over attributes
        self._game_over = False
        self._game_over_buttons = []
        self.create_game_over_buttons()

        # set initial window parameters
        self.update_layout(screen_width, screen_height)

        # Set up the Snake Game & Board
        self._board = Board(self._margin, self._margin + self._hs_bar_height, screen_width - self._margin * 2, screen_height - self._margin * 2)

        # Sets snake speed while playing
        self._move_delay = move_delay

        # Starts game in a fresh state
        self.reset_game ()

    def create_game_over_buttons(self):
        """Creates Game Over Screen Buttons."""
        retry_button = Button("Retry", 0, 0, 180, 50, BTN_RED, BTN_HOVER_RED, SCORE_FONT, 0)
        menu_button = Button("Menu", 0, 0, 180, 50, BTN_RED, BTN_HOVER_RED, SCORE_FONT, 0)
        self._game_over_buttons.extend([retry_button, menu_button])

    def update_high_score(self):
        """Replace the high score when the current score is greater."""
        if self._score > 0 and self._score > self._high_score:
            self._high_score = self._score
            save_high_score(self._high_score) # Saves new record and persists it after program closes

    def set_move_delay (self, move_delay):
        """Sets appropriate speed value to the SnakeGame to pass to snake."""
        self._move_delay = move_delay

    def reset_game(self):
        """Responsible for Snake Game & Board set up when called."""
        self._snake = Snake(self._move_delay)
        self._food  = Food(self._board, self._snake._body)

        # pause is false on restart
        self._paused = False

        # Game over is False on restart
        self._game_over = False

        # Current score resets for every new round
        self._score = 0

    def update(self):
        """Calls a method that updates entities on the Screen."""
        if self._game_over:  # Only perform updates while the game is not over
            mouse_position = pygame.mouse.get_pos()

            for button in self._game_over_buttons:
                button.update(mouse_position)
                
            return
        
        if self._paused:
            return

        # move the snake
        moved = self._snake.move(self._board)
        if not moved:
            return

        # Snake grows after eating, updates current score, and spaws food randomly elsewhere           
        if self._snake.position == self._food._position:
            self._snake.growing = True
            self._score += 1
            self._food.respawn(self._board, self._snake._body)

        # Update snake highscore after death
        if self._snake._dying:
            self.update_high_score()
            self._game_over = True

    def draw(self, game_window):
        """Draw all entities in the game."""

        # Draws game over screen after loss
        if self._game_over == True:
            self.draw_game_over(game_window)
            return 
        
        self._board.draw(game_window)

        self._snake.draw(game_window, self._board)

        self._food.draw(game_window, self._board)

        self.draw_hud(game_window)

    def draw_hud(self,game_window):
        """Draws the elements of the HUD bar."""

        # Draws current score
        score_surface = SCORE_FONT.render(f"Score: {self._score}", False, UI_WHITE)
        score_surface_rect = score_surface.get_rect()
        score_surface_rect.topleft = (self._margin, self._margin)
        pygame.draw.rect(game_window, BTN_RED, pygame.Rect(0, 0, self._screen_width, self._hs_bar_height) )
        game_window.blit(score_surface, score_surface_rect)

        # Draws highscore
        high_score_surface = SCORE_FONT.render(f"High Score: {self._high_score}", False, UI_WHITE )
        high_score_surface_rect = high_score_surface.get_rect()
        high_score_surface_rect.topright = (self._screen_width - self._margin, self._margin)
        game_window.blit(high_score_surface, high_score_surface_rect)

        # Gives visual hint about pausing to users
        if self._paused:
            pause_hint = "SPACEBAR: Press to Resume"
        else:
            pause_hint = "SPACEBAR: Press to pause"

        # Draws visual hint
        pause_hint_surface = PAUSE_FONT.render(pause_hint, True, UI_WHITE)
        pause_hint_surface_rect = pause_hint_surface.get_rect(center = (self._screen_width // 2, self._hs_bar_height // 2))
        game_window.blit(pause_hint_surface, pause_hint_surface_rect)

    def draw_game_over(self, game_window):
        """Draws the game over screen."""

        # Clears Screen before drawing the game over
        game_window.fill(BKGD_RED)

        game_over_surface = TITLE_FONT.render("GAME OVER", True, UI_WHITE)
        game_over_surface_rect = game_over_surface.get_rect(center = (self._screen_width // 2, self._screen_height * 0.35))

        score_over_surface = SCORE_FONT.render(f"Score: {self._score}", False, UI_WHITE)
        score_over_surface_rect = score_over_surface.get_rect(center =(self._screen_width // 2, self._screen_height * 0.45))
        high_score_surface = SCORE_FONT.render(f"High Score: {self._high_score}", False, UI_WHITE )
        high_score_surface_rect = high_score_surface.get_rect(center = (self._screen_width // 2, self._screen_height * 0.55))

        # Draws the Gameover, score, highscore text
        game_window.blit (game_over_surface, game_over_surface_rect)
        game_window.blit (score_over_surface, score_over_surface_rect)
        game_window.blit (high_score_surface, high_score_surface_rect)

        # Draws game over buttons underneath the Scores
        for button in self._game_over_buttons:
            button.draw(game_window)

    def handle_event(self, event):
        """Handles event and executes response to event trigger."""
        if self._game_over:
            for button in self._game_over_buttons:
                if button.handle_event(event):
                     return button.text  # sends the name of clicked button to Game Class for processing 
                
            return None   

        #  Determines the exact moment a key transitions from pressed to released
        keys = pygame.key.get_just_released()

        # Arrow Keys movement logic
        if keys[pygame.K_LEFT] :
            self._snake.direction = Snake.MOVE_LEFT
        elif keys[pygame.K_RIGHT]:
           self._snake.direction = Snake.MOVE_RIGHT
        elif keys[pygame.K_UP]:
            self._snake.direction = Snake.MOVE_UP
        elif keys[pygame.K_DOWN]:
            self._snake.direction = Snake.MOVE_DOWN

        #  Handles event for pausing using only space bar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._paused = not self._paused   

    def update_layout(self, width, height):
        """Receives current layout properties from Game Class and updates its entities."""

        #  Receives Screen Width & Height Properties
        self._screen_width = width
        self._screen_height = height

        #  Defines spacing for high score 
        self._margin = 20
        self._hs_bar_height = int(height * 0.12)

        #  Passes Current Screen Width & Height to the Board
        if not self._board == None:
            self._board.update_layout(self._margin, self._margin + self._hs_bar_height, width - (self._margin * 2), height - self._hs_bar_height - (self._margin * 2))

        # Calculates Game Over button appearance layout
        button_width = 180
        button_height = 50
        button_gap = 20

        total_width = button_width * 2 + button_gap

        # Defines starting position to draw the button
        start_x = (self._screen_width - total_width) // 2
        button_y = int(self._screen_height * 0.65)


        for index, button in enumerate(self._game_over_buttons):
            button.w = button_width
            button.h = button_height

            button.surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)

            # Allows button to be spaced appropriately depending on index number
            x = start_x + index * (button_width + button_gap)

            button.rect = button.surface.get_rect(topleft=(x, button_y))

class Board:
    """Creates the Game Board."""
    def __init__(self, x, y, screen_width, screen_height):

        #  Initializes screen width & screen height 
        self._screen_width = screen_width
        self._screen_height = screen_height

        #  Sets No. of row and columns
        self._columns = 30
        self._rows = 18

        # stores the calculated size of each square boarad cell
        self._cell_size = 0

        self._rect = pygame.Rect(0, 0, 0, 0)

        # calls update_layout method to process screen width and height
        self.update_layout(x, y, screen_width, screen_height)

    def get_columns(self):
        """Returns the number of columns in the board."""
        return self._columns
    columns = property(get_columns)

    def get_rows(self):
        """Returns teh number of rows in the board."""
        return self._rows
    rows = property(get_rows)

    def get_rect(self):
        """Returns the rectangle representing the board."""
        return self._rect
    rect = property(get_rect)

    def get_cell_size(self):
        "Returns the size of each board cell (for unit test code)"
        return self._cell_size
    cell_size = property(get_cell_size)

    def update_layout(self, x, y, width, height):
        """Responsible for handling board layout and receiving updated screen sizes."""

        # calculates individual cell width & height
        cell_width = width // self._columns
        cell_height = height // self._rows

        # makes each cell a square 
        self._cell_size = min(cell_width, cell_height)

        # defines board width & height
        board_width = self._columns * self._cell_size
        board_height = self._rows * self._cell_size

        # defines rect. for board width & height
        self._rect.width = board_width
        self._rect.height = board_height

        # sets position
        self._rect.x = x + ((width - board_width) // 2)
        self._rect.y = y

    def draw (self, game_window): 
        """Draws the board tiles."""

        # draw the board tiles using a nested loop
        for row in range(self._rows):

            for column in range(self._columns):

                # defines x-coordinates of each tile
                x = self._rect.left + column * self._cell_size

                # defines y-coordinate of each tile
                y = self._rect.top + row * self._cell_size

                tile  = pygame.Rect(x, y, self._cell_size, self._cell_size)

                # sets grid color
                if (row + column) % 2 == 0:
                    color = TILE_WHITE
                else:
                    color = TILE_RED

                pygame.draw.rect(game_window, color, tile)

    def get_tile_rect (self, column, row): 
        """Returns cell coordinate, size when called."""
        x = self._rect.left + column * self._cell_size
        y = self._rect.top + row * self._cell_size

        return pygame.Rect(x, y, self._cell_size, self._cell_size)

    def valid_tile(self, tile_pos):
        """Checks if the tile is inside the board(for snake death)."""
        column, row = tile_pos
        if column < 0 or column >= self._columns or row < 0 or row >= self._rows:
            return False
        
        return True   

class Snake:
    """Handles all attributes related to the snake."""

    # Directional constants - rotational so we can check opposites easily
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_VECTORS = [ (0,-1), (1,0), (0,1), (-1,0)]
    SEG_HEAD = 0
    MIN_DELAY = 0.05
    DELAY_MULTIPLIER = 0.95 # decreases delay by 5% which will increase the speed 

    def __init__(self, move_delay):
        """Initializes all the attriutes necessary for snake."""
        self._body = [ (5,7), (4,7), (3,7) ]

        self._direction = self.MOVE_RIGHT
        self._direction_vector = self.MOVE_VECTORS[self._direction]

        self._color = SNAKE_GREEN

        self._growing = False
        self._dying = False

        # Handles snake speed & direction
        self._move_delay = move_delay
        self._next_move = time.time() + self._move_delay
        self._pending_direction = None

    def get_body(self):
        """Returns teh positions occupied by the snake"""
        return self._body
    body = property(get_body)

    def draw(self, game_window, board):
        """Draws the snake onto the board."""
        for column, row in self._body:

            # retrieves correct rect for particular board position
            tile = board.get_tile_rect(column, row)
            pygame.draw.rect(game_window, self._color, tile)
            pygame.draw.rect (game_window, BLACK, tile, width = 1)  # Draws Snake Outline

    def move(self, board):
        """Moves the snake."""
        if time.time() > self._next_move:
            self.update_direction()  # Process any pending direction change

            head_column, head_row = self._body[0]
            direction_column, direction_row = self._direction_vector

            # creates new head
            new_head = (head_column + direction_column, head_row + direction_row)

            # inserts new head
            self._body.insert(0, new_head)

            # Snake eats & grows once, then reset till next cycle
            if self._growing:
                self._growing = False 

                # Updates snake speed incrementally after eating
                new_delay = self._move_delay * self.DELAY_MULTIPLIER

                # stops speed from exceeding defined constant
                self._move_delay = max(self.MIN_DELAY, new_delay )

            else:
                self._body.pop() # adds new head & removes old tail

            # set next move time
            self._next_move = time.time() + self._move_delay

            # Checks for wall collision 
            if not board.valid_tile(self._body[0]):
                self._dying = True 

            # Checks for self collision
            if self._body[0] in self._body[1:]:
                self._dying = True
                
            return True
        
        return False
        
    def get_direction(self):
        """return the snake's current direction."""
        return self._direction
    
    def set_direction(self, new_direction):
        """set the current direction."""
        # Checks for a valid direction
        if new_direction in (0,1,2,3):
            self._pending_direction = new_direction     
    # property declaration for convenience
    direction = property(get_direction, set_direction)

    def get_growing(self):
        """returns internal "_growing" status."""
        return self._growing
    
    def set_growing(self, new_growing):
        """Updates the snake's growing state."""
        if isinstance(new_growing, bool):
            self._growing = new_growing
    growing = property( get_growing, set_growing )

    def get_position(self):
        """Returns position of the snake head."""
        return self._body[self.SEG_HEAD]
    position = property(get_position)
 
    def get_dying(self):
        """Returns whether snake is dying."""
        return self._dying 

    dying = property( get_dying )

    def update_direction(self):
        """Process one pending direction before the snake moves."""

        # Checks if direction is pending
        if not self._pending_direction is None:

            # Checks for reversal with a mod operation
            if not (self._pending_direction + 2) % 4 == self._direction: 

                # sets the direction and the vector
                self._direction = self._pending_direction
                self._direction_vector = self.MOVE_VECTORS[self._direction]
                self._pending_direction = None

class Food:
    """Responsible for Food attributes."""

    def __init__(self, board, snake_body):
        """Initializes the food parameters."""
        self._color = FOOD_COLOUR
        self._border_outline_color = BLACK

        self._position = None
        self.respawn (board, snake_body) 

    def get_position(self):
        """Returns the food current board position."""
        return self._position
    position = property(get_position)

    def draw(self, game_window, board):
        """Draws Food."""
        column, row = self._position
        
        tile = board.get_tile_rect(column, row)

        pygame.draw.rect (game_window, self._color, tile, width = 0, border_radius = 10)
        pygame.draw.rect (game_window, self._border_outline_color, tile, width = 1, border_radius= 10)

    def respawn(self, board, snake_body):
        """Spawns food at random unnoccupied positions."""

        column = random.randint(0, board.columns - 1)
        row = random.randint(0, board.rows -1)

        # stores random column, row as a tuple in position
        position = (column, row)

        # prevent food from spawning anywhere on snake
        while position in snake_body:
            column = random.randint(0, board.columns -1)
            row = random.randint(0, board.rows - 1)

            position = (column, row)

        self._position = position
    
class Game: 
    """Controls Game Loop, and overall Game attributes."""
    def __init__(self):
        self._running = True

        self._clock = pygame.time.Clock()

        self._width = SCREEN_WIDTH
        self._height = SCREEN_HEIGHT

        self._game_window = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)

        # game speed attributes
        self._speed_delays = {
            "Fast": 0.051,
            "Normal": 0.25,
            "Slow": 0.35
        }

        # Game Current Speed
        self._current_speed = "Normal"
        self._current_delay = self._speed_delays[self._current_speed]

        # Screens
        self._menu = Menu(self._width, self._height, MAIN_FONT, BTN_RED, BTN_HOVER_RED)
        self._snake_game = SnakeGame(self._width, self._height, self._current_delay)
        self._settings = Settings(self._width, self._height, MAIN_FONT, BTN_RED, BTN_HOVER_RED)

        self._current_screen = self._menu

    def get_running(self):
        """returns whether game is running."""
        return self._running
    running = property(get_running)

    def process_events(self):
        """main event processing loop."""

        # processes event list
        for event in pygame.event.get():

            # quits
            if event.type == pygame.QUIT:
                self._running = False

            # window resize
            elif event.type == pygame.VIDEORESIZE:

                # updates width, height when window resizes
                self._width = event.w
                self._height = event.h 

                # Screen
                self._game_window = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)

                # passes new width, heigt to respective update_layout
                self._menu.update_layout(self._width, self._height)
                self._snake_game.update_layout(self._width, self._height)
                self._settings.update_layout(self._width, self._height)
                

            # handle the current screen's events
            action = self._current_screen.handle_event(event)

            # button click
            if action == "Play":
                # resets game before starting 
                self._snake_game.reset_game() 

                # switches current screen (Menu) to snake game screen
                self._current_screen = self._snake_game 

            elif action == "Retry": 
                self._snake_game.reset_game()

            elif action == "Menu":
                self._snake_game.reset_game()
                self._current_screen = self._menu

            # When Speed button is selected switch to the setting screen
            elif action == "Speed":
                self._current_screen = self._settings

            # In setting screen, update speed depending on the button clicked
            elif action in ("Fast", "Normal", "Slow"):
                self._current_speed = action
                self._current_delay = self._speed_delays[action]
                self._snake_game.set_move_delay(self._current_delay) 

            # Switches setting screen to menu
            elif action == "Back":
                self._current_screen = self._menu

            # Quits
            elif action == "Quit":
                self._running = False

    def update (self):
        """runs the current screen (Menu, Setting, SnakeGame) update function."""
        self._current_screen.update()

    def draw (self):
        """runs the draw function of the current screen."""
        self._game_window.fill(BKGD_RED)
        self._current_screen.draw(self._game_window)

    def render (self):
        """renders the display and sets the FPS."""
        pygame.display.flip()
        self._clock.tick(60)
