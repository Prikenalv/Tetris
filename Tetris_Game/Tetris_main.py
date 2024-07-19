import pygame
import sys
from Tetris_Variables import *
from Tetris_game import *  # Import Tetris class
from Tetris_score import *
from Tetris_nextBlock import NextBlock
from Tetris_LCleared import LinesCleared
from Tetris_Level import GameLevel
from Tetris_TitleScreen import *
from Tetris_Pause import *
from Tetris_GameOver import *


class runGame:
    def __init__(self, game):
        pygame.init()  # Initialize pygame modules
        pygame.font.init()  # Initialize fonts
        pygame.display.set_caption("TETRIS")  # Set window title

        # Set up main game surface
        self.main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()  # Create a clock to control FPS
        self.FPS = 30  # Frames per second
        self.__running = True  # Flag to control the game loop
        self.paused = False  # Flag to indicate if the game is paused

        # Initialize game components
        self.game_level = GameLevel()  # Initialize GameLevel instance
        self.__score = Score(self.game_level)  # Initialize Score instance with GameLevel dependency
        self.lines_cleared = LinesCleared()  # Initialize LinesCleared instance
        self.preview = NextBlock()  # Initialize NextBlock instance
        self.game = game  # Assign the passed Tetris instance to self.game

        # Timer for game updates
        self.timer()

    def timer(self):
        # Set up custom pygame events for game timing
        self.user_event = pygame.USEREVENT + 0  # Custom event for regular game updates
        self.fast_user_event = pygame.USEREVENT + 1  # Custom event for fast animation updates
        self.anim_trigger = False  # Flag to trigger regular game updates
        self.fast_anim_trigger = False  # Flag to trigger fast animation updates
        pygame.time.set_timer(self.user_event,  self.__score.DEFAULT_FALL_SPEED)  # Set regular update timer based on score
        pygame.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)  # Set fast update timer

    def update(self):
        # Update game logic and components
        if not self.paused:
            self.game.update(self.anim_trigger)  # Update Tetris game state based on anim_trigger
            self.__score.update_score(self.game.check_lines())  # Update score based on lines cleared by the game
            self.lines_cleared.render_lines_cleared()  # Render lines cleared on the lines_cleared surface
            self.game_level.update_level( self.__score.score)  # Update game level based on current score
            self.clock.tick(self.FPS)  # Control game loop FPS

    def draw(self):
        # Draw game elements on the main surface
        self.main_surface.fill(BLACK)  # Fill main surface with black
        score_x = WINDOW_WIDTH - SIDEBAR_WIDTH
        score_y = 200
        self.main_surface.blit( self.__score.surface, (score_x, score_y))  # Blit score surface to main surface

        lines_cleared_x = WINDOW_WIDTH - SIDEBAR_WIDTH
        lines_cleared_y = 333
        self.main_surface.blit(self.lines_cleared.surface, (lines_cleared_x, lines_cleared_y))  # Blit lines cleared surface

        game_level_x = WINDOW_WIDTH - SIDEBAR_WIDTH
        game_level_y = 465
        self.main_surface.blit(self.game_level.surface, (game_level_x, game_level_y))  # Blit game level surface

        self.preview.draw()  # Draw the next block preview

    def event_listener(self):
        # Listen for events (user input and pygame events)
        self.anim_trigger = False  # Reset animation trigger
        self.fast_anim_trigger = False  # Reset fast animation trigger
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit system
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused  # Toggle pause state with ESC key
                else:
                    self.game.controller(event.key)  # Pass key press to Tetris game controller
            elif event.type == pygame.KEYUP:
                self.game.handle_key_release(event.key)  # Pass key release to Tetris game controller
            elif event.type == self.user_event:
                self.anim_trigger = True  # Set animation trigger for regular game update
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True  # Set fast animation trigger

    def run(self):
        # Run the title screen first
        title_screen = TitleScreen(self.main_surface)
        title_screen.run()  # Execute the title screen loop

        # Once title screen is done, run the main game loop
        while self.__running:
            self.event_listener()  # Listen for events
            if self.paused:
                # Run the pause screen if paused
                pause_screen = PauseScreen(self.main_surface)
                pause_screen.run()  # Execute the pause screen loop
                self.paused = False  # Resume the game after pause screen exits
            else:
                self.update()  # Update game state
                self.draw()  # Draw game elements
                self.game.run()  # Execute Tetris game loop
                self.preview.set_next_shape(self.game.next_shape)  # Update next block preview
                pygame.display.flip()  # Update display

        pygame.quit()  # Quit pygame
        sys.exit()  # Exit system


if __name__ == '__main__':
    game = Tetris()  # Initialize Tetris game instance
    main = runGame(game)  # Initialize runGame instance with Tetris game instance
    main.run()  # Run the main game loop