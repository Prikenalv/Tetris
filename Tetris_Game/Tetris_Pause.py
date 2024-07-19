import pygame
import sys
from Tetris_Variables import *

class PauseScreen:
    def __init__(self, surface):
        # Initialize with the main surface where the pause screen will be drawn
        self.surface = surface

        # Load the button images for resume and quit
        self.resume_button_image = pygame.image.load("TetrisBlocks/Resume_Button.png").convert_alpha()
        self.quit_button_image = pygame.image.load("TetrisBlocks/Quit_Button.png").convert_alpha()

        # Calculate positions for resume and quit buttons
        resume_button_x = (WINDOW_WIDTH - self.resume_button_image.get_width()) // 2
        resume_button_y = WINDOW_HEIGHT // 2 + 70
        quit_button_x = (WINDOW_WIDTH - self.quit_button_image.get_width()) // 2
        quit_button_y = WINDOW_HEIGHT // 2 + 180

        # Define rectangles for buttons and set their positions
        self.resume_button_rect = self.resume_button_image.get_rect(topleft=(resume_button_x, resume_button_y))
        self.quit_button_rect = self.quit_button_image.get_rect(topleft=(quit_button_x, quit_button_y))

        # Initialize font and render the "Game Paused" text
        self.font = pygame.font.SysFont(None, 80)
        self.paused_text = self.font.render("Game Paused", True, WHITE)
        paused_text_x = (WINDOW_WIDTH - self.paused_text.get_width()) // 2
        paused_text_y = WINDOW_HEIGHT // 4
        self.paused_text_position = (paused_text_x, paused_text_y)

        # Initialize clock for controlling FPS
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.__running = True  # Flag to control the pause screen loop

    def draw(self):
        # Draw a semi-transparent overlay over the main surface
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)  # Set transparency level (0 to 255)
        overlay.fill((0, 0, 0))  # Fill with black color
        self.surface.blit(overlay, (0, 0))  # Blit overlay onto the main surface

        # Draw "Game Paused" text at predefined position
        self.surface.blit(self.paused_text, self.paused_text_position)

        # Draw resume and quit buttons on the main surface
        self.surface.blit(self.resume_button_image, self.resume_button_rect.topleft)
        self.surface.blit(self.quit_button_image, self.quit_button_rect.topleft)

        pygame.display.flip()  # Update the display

    def event_listener(self):
        # Event handling loop for handling user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if self.resume_button_rect.collidepoint(event.pos):
                        self.__running = False  # Set running flag to False to exit the pause loop
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def run(self):
        # Main loop to run the pause screen until resume button is clicked
        while self.__running:
            self.event_listener()  # Handle events (mouse clicks, quit)
            self.draw()  # Draw the pause screen elements
            self.clock.tick(self.FPS)  # Cap the frame rate

        return True  # Return True to indicate the game should resume after the pause screen