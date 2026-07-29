# ========================
# IMPORT LIBRARIES
# ========================

import pygame
from game import Game

# ========================
# INITIALIZATION
# ========================

pygame.init()
pygame.display.set_caption("Not Snake game")

# ========================
#  GAME LOOP 
# ========================

#  Creates a game object that refers to Game Class.
game = Game()

while game.running:

    #  Calls game class to process events contained in the main loop.
    game.process_events()

    #  Calls game class to update events that affects the enitre game 
    #  such as passing updated screen sizes etc.  
    game.update()

    # Draws game_window and tells current screen to draw itself.
    game.draw()

    # Controls game rendering (Display, FPS).
    game.render()

pygame.quit()

#buttons
#play_button = Button(-50, 50, 300, 100, BTN_RED, MAIN_FONT, angle= MENU_ANGLE)


#Note currently my device is syncing my code, and im not able to commit on my current device, major changes
# till i get to school, so appologies if there any big block of code