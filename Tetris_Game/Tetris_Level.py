import pygame
from Tetris_Variables import *

class GameLevel:
    def __init__(self):
        # Initialize the GameLevel object
        self.__level = 1  # Private attribute to store the game level, starting at level 1
        self.surface = pygame.Surface((SIDEBAR_WIDTH, LEVEL_HEIGHT - PADDING), pygame.SRCALPHA)
        # Create a transparent surface for displaying the level
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        # Position the surface at the bottom right of the window
        self.render_level()  # Initial rendering of the level

    @property
    def level(self):
        # Getter for the level
        return self.__level

    @level.setter
    def level(self, new_level):
        # Setter for the level with automatic re-rendering of the level display
        self.__level = new_level
        self.render_level()

    def update_level(self, new_level):
        # Update the level manually and re-render the display
        self.__level = new_level
        self.render_level()

    def render_level(self):
        # Render the current level onto the surface
        self.surface.fill(BLACK)  # Clear the surface with black

        level_text = "LEVEL:"  # Text label for the level
        rendered_level = TITLE_FONT.render(level_text, True, WHITE)  # Render the level text

        level_value_text = f"{self.level}"  # Text value of the current level
        rendered_level_value = TITLE_FONT.render(level_value_text, True, WHITE)  # Render the level value

        self.surface.blit(rendered_level, (10, 10))  # Position the level text on the surface
        self.surface.blit(rendered_level_value, (10, 50))  # Position the level value below the text

        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), 2)  # Draw a white outline around the surface