import pygame

pygame.init()
pygame.font.init()

# Game sizes
COLUMNS = 10
ROWS = 20
CELL_SIZE = 30
GAME_HEIGHT = ROWS * CELL_SIZE
GAME_WIDTH = COLUMNS * CELL_SIZE

# Sidebar size
SIDEBAR_WIDTH = 200
HEIGHT_FRACTION = 0.6

PREVIEW_HEIGHT = int(GAME_HEIGHT / 3)

SCORE_HEIGHT_FRACTION = 1 - HEIGHT_FRACTION
SCORE_HEIGHT = int(GAME_HEIGHT / 4.5)

LCLEARED_HEIGHT = int(GAME_HEIGHT / 4.5)

LEVEL_HEIGHT = int(GAME_HEIGHT / 4.5) + 2

# WINDOW
PADDING = 0
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_BLACK = (2, 0, 19)
GRAY = (28, 28, 28)
INNER_LINE_COLOR = (105, 132, 138)
OUTER_LINE_COLOR = (255, 255, 255)  # Adjusted to match tuple format

# Font
TITLE_FONT = pygame.font.Font(None, 45)
NEXT_TEXT = TITLE_FONT.render("NEXT:", True, WHITE)

# Game behavior
ANIMATION_TIME_INTERVAL = 200
FAST_ANIM_TIME_INTERVAL = 5

# Image
ASSETS = {
    1: pygame.transform.scale(pygame.image.load("TetrisBlocks/Blue.png"), (CELL_SIZE, CELL_SIZE)),
    2: pygame.transform.scale(pygame.image.load("TetrisBlocks/Cyan.png"), (CELL_SIZE, CELL_SIZE)),
    3: pygame.transform.scale(pygame.image.load("TetrisBlocks/Green.png"), (CELL_SIZE, CELL_SIZE)),
    4: pygame.transform.scale(pygame.image.load("TetrisBlocks/Orange.png"), (CELL_SIZE, CELL_SIZE)),
    5: pygame.transform.scale(pygame.image.load("TetrisBlocks/Red.png"), (CELL_SIZE, CELL_SIZE)),
    6: pygame.transform.scale(pygame.image.load("TetrisBlocks/Purple.png"), (CELL_SIZE, CELL_SIZE)),
    7: pygame.transform.scale(pygame.image.load("TetrisBlocks/Yellow.png"), (CELL_SIZE, CELL_SIZE)),
}

# Tetromino shapes
TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

# Vector
vector = pygame.math.Vector2
INITIAL_POSITION_OFFSET = vector(COLUMNS // 2, -2)

# Move directions
MOVE_DIRECTIONS = {
    'LEFT': vector(-1, 0),
    'RIGHT': vector(1, 0),
    'DOWN': vector(0, 1)
}