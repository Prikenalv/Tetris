import pygame
import sys
from Tetris_Variables import *

class TitleScreen:
    def __init__(self, surface):
        self.surface = surface

        # Initialize font for text rendering
        self.font = pygame.font.SysFont("Arial", 60)

        # Load and scale the background image to fit the window
        self.background_image = pygame.image.load("TetrisBlocks/Title_Background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Load the button images for start and quit buttons
        self.start_button_image = pygame.image.load("TetrisBlocks/Start_Button.png").convert_alpha()
        self.quit_button_image = pygame.image.load("TetrisBlocks/Quit_Button.png").convert_alpha()

        # Set the positions of the buttons
        start_button_x = (WINDOW_WIDTH - self.start_button_image.get_width()) // 2
        start_button_y = WINDOW_HEIGHT // 2 + 70
        quit_button_x = (WINDOW_WIDTH - self.quit_button_image.get_width()) // 2
        quit_button_y = WINDOW_HEIGHT // 2 + 180

        # Get the rectangles of the buttons and set their positions
        self.start_button_rect = self.start_button_image.get_rect(topleft=(start_button_x, start_button_y))
        self.quit_button_rect = self.quit_button_image.get_rect(topleft=(quit_button_x, quit_button_y))

        # Initialize clock for controlling FPS
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.__running = True

    def draw(self):
        # Draw the background image
        self.surface.blit(self.background_image, (0, 0))

        # Draw the start and quit buttons on the surface
        self.surface.blit(self.start_button_image, self.start_button_rect.topleft)
        self.surface.blit(self.quit_button_image, self.quit_button_rect.topleft)

        # Update the display
        pygame.display.flip()

    def event_listener(self):
        # Handle events such as quit and mouse button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.start_button_rect.collidepoint(event.pos):
                        self.__running = False  # Set running flag to False to exit the title screen loop
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()  # Quit the game if the quit button is clicked

    def run(self):
        # Main loop for the title screen
        while self.__running:
            self.event_listener()  # Listen for events
            self.draw()  # Draw the title screen
            self.clock.tick(self.FPS)  # Cap the frame rate

        return True  # Return True when the title screen exits