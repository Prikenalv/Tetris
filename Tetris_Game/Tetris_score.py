import pygame
from Tetris_Variables import *

class Score:
    def __init__(self, game_level):
        # Initialize default fall speed and other attributes
        self.__DEFAULT_FALL_SPEED = 1000  # Mangled attribute to store the default fall speed in milliseconds
        self.game_level = game_level  # Reference to GameLevel instance
        self.__score = 0  # Current score
        self.temporary_score = 0  # Temporary score used for level up calculations
        self.surface = pygame.Surface((SIDEBAR_WIDTH, SCORE_HEIGHT - PADDING), pygame.SRCALPHA)
        # Create a transparent surface for displaying the score
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        # Position the surface at the bottom right of the window
        self.render_score()  # Initial rendering of the score

    @property
    def score(self):
        return self.__score

    def update_score(self, lines_cleared):
        # Update score based on the number of lines cleared
        if lines_cleared == 1:
            self.__score += 100
            self.temporary_score += 100
        elif lines_cleared == 2:
            self.__score += 300
            self.temporary_score += 300
        elif lines_cleared == 3:
            self.__score += 500
            self.temporary_score += 500
        elif lines_cleared == 4:
            self.__score += 800
            self.temporary_score += 800

        # Level up if temporary score exceeds the threshold
        while self.temporary_score >= 1000:
            self.temporary_score -= 1000
            self.game_level.level += 1  # Increase game level by 1
            self.game_level.update_level(self.game_level.level)  # Update level display
            self.decrease_fall_speed()  # Adjust fall speed based on level

        self.render_score()  # Update rendered score on the surface

    def decrease_fall_speed(self):
        # Decrease fall speed when level up occurs
        self.__DEFAULT_FALL_SPEED -= 75  # Decrease the fall speed by 75 milliseconds
        print("---------LEVEL UP")
        print(f"Fall speed decreased to {self.__DEFAULT_FALL_SPEED} ms")
        print(f"---------Tempo: {self.temporary_score}")

    def render_score(self):
        # Render the current score onto the surface
        self.surface.fill(BLACK)  # Clear the surface with black
        score_text = "SCORE:"  # Text for the score label
        rendered_score = TITLE_FONT.render(score_text, True, WHITE)  # Render the score label

        score_value_text = f"{ self.__score}"  # Convert the score to string
        rendered_score_value = TITLE_FONT.render(score_value_text, True, WHITE)  # Render the score value

        # Blit score label and value onto the surface
        self.surface.blit(rendered_score, (10, 10))
        self.surface.blit(rendered_score_value, (10, 50))

        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), 2)  # Draw a white outline around the surface

    @property
    def DEFAULT_FALL_SPEED(self):
        # Property for accessing the default fall speed
        return self.__DEFAULT_FALL_SPEED