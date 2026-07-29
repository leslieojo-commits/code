import pygame
from game import Button 

def test_button_initialization():

    """ Tests that button initializes with correct attributes. """

    pygame.init()

    #  Creates a default font object for the button.
    font = pygame.font.SysFont(None, 30) 

    #  Initializes button 
    button = Button(text = "Play", x=0, y=0, w=300, h=100, normal_color=(255, 0, 0), hover_color=(0, 255, 0), font=font)

    #  Verifies button initializes its correct attributes.
    assert button.text == "Play"
    assert button.w == 300
    assert button.h == 100
    assert button.hovered is False

def test_button_hover(): 

    """ Test to see that button detects mouse hovering, and responds appropriately. """

    pygame.init()
    font = pygame.font.SysFont(None, 30)
    button = Button(text = "Play", x=0, y=0, w=300, h=100, normal_color=(255, 0, 0), hover_color=(0, 255, 0), font=font)

    #  Creates object containing mouse position.
    mouse_position = (200, 80)

    # Passes mouse position to update method to check collision.
    button.update(mouse_position)

    #  Verifies if butt
    assert button.hovered is True

