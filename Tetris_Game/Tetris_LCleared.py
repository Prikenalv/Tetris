import pygame
from Tetris_Variables import *

pygame.font.init()

class LinesCleared:
    def __init__(self):
        # Initialize LinesCleared object
        self.__LC_TITLE_FONT = pygame.font.Font(None, 30)  # Font for title text
        self.__LC_TITLE_VALUE_FONT = pygame.font.Font(None, 50)  # Font for title text
        self.__lines_cleared = 0  # Initialize lines cleared counter
        # Create transparent surface for displaying lines cleared information
        self.__surface = pygame.Surface((SIDEBAR_WIDTH, LCLEARED_HEIGHT - PADDING), pygame.SRCALPHA)
        # Position the surface in the sidebar
        self.__rect = self.__surface.get_rect(topright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.render_lines_cleared()  # Initial rendering of lines cleared

    def update_lines_cleared(self, lines_cleared):
        # Update the lines cleared count
        self.__lines_cleared += lines_cleared
        self.render_lines_cleared()  # Update rendered lines cleared text

    def render_lines_cleared(self):
        # Render lines cleared text on the surface
        self.__surface.fill(BLACK)  # Clear the surface with black

        lines_text = "LINES CLEARED:"
        lines_text_value = str(self.__lines_cleared)

        # Render text using predefined fonts
        rendered_lines = self.__LC_TITLE_FONT.render(lines_text, True, WHITE)
        rendered_lines_value = self.__LC_TITLE_VALUE_FONT.render(lines_text_value, True, WHITE)

        # Blit rendered text onto the surface
        self.__surface.blit(rendered_lines, (10, 10))
        self.__surface.blit(rendered_lines_value, (10, 50))

        # Draw outline of the surface
        pygame.draw.rect(self.__surface, WHITE, self.__surface.get_rect(), 2)

    @property
    def lines_cleared(self):
        # Getter for lines_cleared
        return self.__lines_cleared

    @lines_cleared.setter
    def lines_cleared(self, value):
        # Setter for lines_cleared with validation
        if value < 0:
            raise ValueError("Lines cleared count cannot be negative")
        self.__lines_cleared = value
        self.render_lines_cleared()

    @property
    def surface(self):
        # Getter for surface
        return self.__surface

    @property
    def rect(self):
        # Getter for rect
        return self.__rect

    @property
    def LC_TITLE_FONT(self):
        # Getter for LC_TITLE_FONT
        return self.__LC_TITLE_FONT