"""
main.py

This module serves as the entry point for the Snake game application.

It initialises the Game object and starts the main game loop, 
which controls the event handling, game states updates , drawing 
display rendering.
"""

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

    #  Calls game class to update events that affect the enitre game 
    #  such as passing updated screen sizes etc.  
    game.update()

    # Draws game_window and tells current screen to draw itself.
    game.draw()

    # Controls game rendering (Display, FPS).
    game.render()

pygame.quit()

