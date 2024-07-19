import pygame
from Tetris_Variables import *
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, tetromino, position):
        # Call the Sprite constructor
        super().__init__(tetromino.tetris.sprite_group)
        # Initialize the block with its tetromino and position
        self.tetromino = tetromino
        self.position = vector(position) + INITIAL_POSITION_OFFSET

        # Set the block's image based on the shape of its tetromino
        shape = self.tetromino.shape
        if shape == 'T':
            self.image = ASSETS[6]
        elif shape == 'O':
            self.image = ASSETS[7]
        elif shape == 'J':
            self.image = ASSETS[1]
        elif shape == 'L':
            self.image = ASSETS[4]
        elif shape == 'I':
            self.image = ASSETS[2]
        elif shape == 'S':
            self.image = ASSETS[3]
        elif shape == 'Z':
            self.image = ASSETS[5]

        self.rect = self.image.get_rect()  # Get rectangle of the block's image
        self.alive = True  # Flag to determine if block is alive

        # Update the block's position
        self.update()

    def is_alive(self):
        # Check if block is alive; if not, kill it
        if not self.alive:
            self.kill()

    def set_block_position(self):
        # Set the position of the block on the game grid
        self.rect.topleft = self.position * CELL_SIZE + vector(PADDING)

    def rotate(self, pivot_point):
        # Rotate the block around a pivot point
        translated = self.position - pivot_point
        rotated = translated.rotate(90)
        return rotated + pivot_point

    def update(self):
        # Update the block's position and check if it's alive
        self.set_block_position()
        self.is_alive()

    def collided(self, pos):
        # Check if the block has collided with another block or the game boundaries
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < COLUMNS and y < ROWS and (y < 0 or not self.tetromino.tetris.game_array[y][x]):
            return False  # No collision
        return True  # Collision detected


class Tetromino:
    def __init__(self, tetris, current=True):
        # Initialize the tetromino with its parent tetris game
        self.tetris = tetris
        self.current = current  # Flag to indicate if the tetromino is the current active one
        self.shape = random.choice(list(TETROMINOES.keys()))  # Randomly choose a shape from predefined shapes

        # Create blocks for the chosen shape
        self.blocks = [Block(self, position) for position in TETROMINOES[self.shape]]

        self.landing = False  # Flag to indicate if the tetromino has landed (stopped moving)

    def collided(self, block_position):
        # Check if the tetromino has collided with another block given a block position
        return any(map(Block.collided, self.blocks, block_position))

    def rotate(self):
        # Rotate the tetromino clockwise
        pivot_point = self.blocks[0].position  # Use the first block as the pivot point
        new_block_position = [block.rotate(pivot_point) for block in self.blocks]

        if not self.collided(new_block_position):
            # If rotation is valid (no collision), update block positions
            for i, block in enumerate(self.blocks):
                block.position = new_block_position[i]

    def move(self, direction):
        # Move the tetromino in the specified direction (left, right, down)
        move_direction = MOVE_DIRECTIONS[direction]

        new_block_position = [block.position + move_direction for block in self.blocks]
        collided = self.collided(new_block_position)

        if not collided:
            # If no collision, move each block to the new position
            for block in self.blocks:
                block.position += move_direction
        elif direction == 'DOWN':
            # If moving down and collided, set landing flag to True (tetromino has landed)
            self.landing = True

    def update(self):
        # Update the tetromino's position by moving it down (default behavior)
        self.move(direction='DOWN') 