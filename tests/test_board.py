import pygame
from game import Board

def test_board_get_tile_rect():
    """Tests that get_tile_rect returns expected rectangle."""
    pygame.init()

    # Creates a board instance with given screen dimension.
    board = Board(800, 600)

    tile = board.get_tile_rect (5,3)

    #  Calculates expected position of the tile based on coordinates
    #  of the row and column, and size of each cell.
    expected_x = board._rect.left + 5 * board._cell_size
    expected_y = board._rect.top + 3 * board._cell_size

    # Could use later as the tricky debugging error I faced expected_y = board.rect.top + 3 * board.cell_size

    # Verifies that actual tile position coordinates matches expected coordinates.
    assert tile.x == expected_x
    assert tile.y == expected_y
    assert tile.width == board._cell_size
    assert tile.height == board._cell_size