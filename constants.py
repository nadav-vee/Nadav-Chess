import pygame, os
BOARD_ALT_ORIGINAL_WIDTH = 256
BOARD_ALT_ORIGINAL_HEIGHT = 256
SCALE_FACTOR = 3
BOARD_ALT_WIDTH = BOARD_ALT_ORIGINAL_WIDTH * SCALE_FACTOR
BOARD_ALT_HEIGHT = BOARD_ALT_ORIGINAL_HEIGHT * SCALE_FACTOR
PADDING = 18
SQUARE = 66
START_X = 120
START_Y = 120
ROWS = 8
COLS = 8
BOARD_WIDTH = COLS * SQUARE
BOARD_HEIGHT = ROWS * SQUARE
CHECKED = pygame.image.load(os.path.join("Assets", "checked.png"))

def dif_clr(_color):
    if _color == "w":
        return "b"
    return "w"

def clr(_color):
    if _color == "b":
        return "black"
    return "white"