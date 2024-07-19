import pygame
from Tetris_Variables import *


class NextBlock:
    def __init__(self):
        # Initialize the surface for the next block preview with transparent alpha channel
        self.surface = pygame.Surface((SIDEBAR_WIDTH, PREVIEW_HEIGHT), pygame.SRCALPHA)

        # Position the preview surface at the top-right corner of the game window
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))

        # Define the text label for the "NEXT" indicator
        self.next_text = NEXT_TEXT

        # Initialize variables for the next shape and to track the last drawn shape
        self.next_shape = None
        self.last_drawn_shape = None  # To avoid unnecessary blits, track the last drawn shape

    def set_next_shape(self, next_shape):
        """
        Set the next tetromino shape to be displayed in the preview.

        Parameters:
        next_shape (Tetromino): The next tetromino shape object to display.
        """
        self.next_shape = next_shape

    def draw(self):
        """
        Draw the next block preview on the preview surface.
        """
        # Clear the preview surface with a black fill
        self.surface.fill(BLACK)

        # Draw the next shape only if it has changed since the last draw
        if self.next_shape:
            for block in self.next_shape.blocks:
                # Calculate and adjust position for each block in the preview
                x = block.position.x * CELL_SIZE + (-80)  # Adjusted x position
                y = block.position.y * CELL_SIZE + 170  # Adjusted y position
                if isinstance(block.image, pygame.Surface):
                    # Blit the block's image onto the preview surface
                    self.surface.blit(block.image, (x, y))

        # Draw the "NEXT" text at a fixed position and draw a white outline around the preview surface
        self.surface.blit(self.next_text, (10, 10))
        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), 2)

        # Blit the preview surface onto the main display surface
        pygame.display.get_surface().blit(self.surface, self.rect)