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

game = Game()

while game.running:

    game.process_events()

    game.update()

    game.draw()

    game.render()

pygame.quit()

#buttons
#play_button = Button(-50, 50, 300, 100, BTN_RED, MAIN_FONT, angle= MENU_ANGLE)


#Note currently my device is syncing my code, and im not able to commit on my current device, major changes
# till i get to school, so appologies if there any big block of code