import pygame
from game import Button # Go to my main code and bring Button class to this test file

def test_button_initialization():

    pygame.init()
    font = pygame.font.SysFont(None, 30) 
    button = Button(text = "Play", x=0, y=0, w=300, h=100, normal_color=(255, 0, 0), hover_color=(0, 255, 0), font=font)

    assert button.text == "Play"
    assert button.w == 300
    assert button.h == 100
    assert button.hovered is False

def test_button_hover(): # test to check mouse is being hovered

    pygame.init()
    font = pygame.font.SysFont(None, 30)
    button = Button(text = "Play", x=0, y=0, w=300, h=100, normal_color=(255, 0, 0), hover_color=(0, 255, 0), font=font)

    mouse_position = (200, 80)

    button.update(mouse_position)

    assert button.hovered is True

