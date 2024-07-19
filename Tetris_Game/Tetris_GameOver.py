import pygame
import sys
from Tetris_Variables import *  # Import necessary constants and variables

class GameOverScreen:
    def __init__(self, surface, score, lines_cleared, game_level):
        # Initialize the Game Over Screen object
        self.surface = surface  # The surface to draw the game over screen on
        self.clock = pygame.time.Clock()  # Clock to control frame rate
        self.FPS = 30  # Frames per second for the game over screen
        self.__running = True  # Flag to control the main game loop

        # Initialize fonts for rendering text
        self.game_over_font = pygame.font.SysFont(None, 90)  # Font for "Game Over" text
        self.font = pygame.font.SysFont(None, 50)  # General font for other text

        # Render "Game Over" text
        self.game_over_text = self.game_over_font.render("Game Over", True, WHITE)  # Render the "Game Over" text
        self.game_over_text_x = (WINDOW_WIDTH - self.game_over_text.get_width()) // 2  # Center horizontally
        self.game_over_text_y = WINDOW_HEIGHT // 4 - 20  # Position vertically

        # Initialize game variables passed from Tetris game
        self.__score = score  # Final score of the game
        self.lines_cleared = lines_cleared  # Number of lines cleared during the game
        self.game_level = game_level  # Current game level

        # Load quit button image and position it
        self.quit_button_image = pygame.image.load("TetrisBlocks/Quit_Button.png").convert_alpha()
        self.quit_button_x = (WINDOW_WIDTH - self.quit_button_image.get_width()) // 2  # Center horizontally
        self.quit_button_y = WINDOW_HEIGHT // 2 + 180  # Position vertically
        self.quit_button_rect = self.quit_button_image.get_rect(topleft=(self.quit_button_x, self.quit_button_y))

    def draw(self):
        # Draw overlay to dim the background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)  # Set transparency level
        overlay.fill((0, 0, 0))  # Fill with black
        self.surface.blit(overlay, (0, 0))  # Draw overlay on the surface

        # Draw "Game Over" text
        self.surface.blit(self.game_over_text, (self.game_over_text_x, self.game_over_text_y))

        # Calculate initial y position for subsequent text elements
        initial_y = self.game_over_text_y + self.game_over_text.get_height() + 60

        # Draw "Final Score" text
        score_text = self.font.render(f"Final Score: { self.__score}", True, WHITE)
        score_text_rect = score_text.get_rect(left=self.game_over_text_x, top=initial_y)
        self.surface.blit(score_text, score_text_rect)

        # Draw "Level" text
        level_text = self.font.render(f"Level: {self.game_level}", True, WHITE)
        level_text_rect = level_text.get_rect(left=self.game_over_text_x, top=initial_y + score_text.get_height() + 20)
        self.surface.blit(level_text, level_text_rect)

        # Draw "Lines Cleared" text
        lines_text = self.font.render(f"Lines Cleared: {self.lines_cleared}", True, WHITE)
        lines_text_rect = lines_text.get_rect(left=self.game_over_text_x, top=initial_y + score_text.get_height() + level_text.get_height() + 40)
        self.surface.blit(lines_text, lines_text_rect)

        # Draw quit button image
        self.surface.blit(self.quit_button_image, self.quit_button_rect.topleft)

        # Update the display
        pygame.display.flip()

    def event_listener(self):
        # Event handling for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.quit_button_rect.collidepoint(event.pos):  # Check if the quit button is clicked
                        pygame.quit()  # Quit pygame
                        sys.exit()  # Exit the program

    def run(self):
        # Main game loop for the game over screen
        while self.__running:
            self.event_listener()  # Handle events
            self.draw()  # Draw the screen
            self.clock.tick(self.FPS)  # Cap frame rate