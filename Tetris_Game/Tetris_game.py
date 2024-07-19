import pygame
from Tetris_Variables import *
from Tetris_Shape import *
from Tetris_score import *
from Tetris_nextBlock import *
from Tetris_LCleared import *
from Tetris_Level import *
from Tetris_GameOver import *
from Tetris_main import *


class Tetris:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("TETRIS")
        self.__score = Score(None)

        # Create the game surface
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))

        # Get the display surface
        self.game_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.sprite_group = pygame.sprite.Group()
        self.speed_up = False
        self.last_move_time = pygame.time.get_ticks()

        # Initialize game components
        self.game_level = GameLevel()
        self.__score = Score(self.game_level)
        self.current_shape = Tetromino(self)
        self.next_shape = Tetromino(self, current=False)

        # Fill the game background
        self.surface.fill(BLUE_BLACK)

        # Game Array
        self.game_array = self.get_game_array()

        # Landing timer
        self.landing_time = None

        # Initialize NextBlock object
        self.next_block_preview = NextBlock()

        # Initialize LinesCleared object
        self.lines_cleared_ui = LinesCleared()

        # Initial update of the next block preview
        self.next_block_preview.set_next_shape(self.next_shape)

        # Initialize fall speed
        self.fall_speed =  self.__score.DEFAULT_FALL_SPEED  # Assuming DEFAULT_FALL_SPEED is defined in Score

        # Create an instance of runGame and pass self
        self.main = runGame(self)

        # Ensure game over screen has access to the main surface
        game_over_screen = GameOverScreen(self.game_surface,  self.__score.score, self.lines_cleared_ui.lines_cleared,
                                          self.game_level.level)

    def update_score(self, lines_cleared):
        # Update score using the Score class method
         self.__score.update_score(lines_cleared)

    def check_lines(self):
        lines_to_clear = []
        for y in range(ROWS):
            if all(self.game_array[y]):
                lines_to_clear.append(y)

        for row in lines_to_clear:
            for x in range(COLUMNS):
                if self.game_array[row][x]:
                    self.game_array[row][x].alive = False
                    self.game_array[row][x] = 0

            for y in range(row, 0, -1):
                for x in range(COLUMNS):
                    if self.game_array[y - 1][x]:
                        self.game_array[y - 1][x].position.y += 1
                    self.game_array[y][x] = self.game_array[y - 1][x]

            for x in range(COLUMNS):
                self.game_array[0][x] = 0

        if lines_to_clear:
            lines_cleared = len(lines_to_clear)
            self.update_score(lines_cleared)
            self.lines_cleared_ui.update_lines_cleared(lines_cleared)

        return len(lines_to_clear)

    def landing_checker(self):
        if self.current_shape.landing:
            self.speed_up = False
            self.put_blocks_in_array()
            lines_cleared = self.check_lines()  # Check and remove completed lines immediately
            # Move the next shape to current and generate a new next shape
            self.current_shape = self.next_shape
            self.next_shape = Tetromino(self, current=False)
            self.next_block_preview.set_next_shape(self.next_shape)  # Update next shape preview

    def controller(self, pressed_key):
        # Handle player input for moving the tetromino
        if pressed_key == pygame.K_LEFT:
            self.current_shape.move(direction='LEFT')
            print("Left Button Pressed")

        elif pressed_key == pygame.K_RIGHT:
            self.current_shape.move(direction='RIGHT')
            print("Right Button Pressed")

        elif pressed_key == pygame.K_UP:
            self.current_shape.rotate()
            print("Up Button Pressed")

        elif pressed_key == pygame.K_SPACE:
            self.drop_block()  # Drop the block immediately
            print("Space Button Pressed")

        elif pressed_key == pygame.K_DOWN:
            self.speed_up = True  # Start accelerating the block
            print("Down Button Pressed")

    def handle_key_release(self, released_key):
        if released_key == pygame.K_DOWN:
            self.speed_up = False
            print("Down Button Released Pressed")

    def get_game_array(self):
        # Initialize the game array with zeros
        return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

    def put_blocks_in_array(self):
        for block in self.current_shape.blocks:
            x = int(block.position.x)
            y = int(block.position.y)

            self.game_array[y][x] = block

    def draw_grid(self):
        # Draw the grid on the game surface
        for col in range(COLUMNS):
            for row in range(ROWS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.surface, (GRAY), rect, 1)

    def drop_block(self):
        # Move the block all the way down until it collides
        while not self.current_shape.landing:
            self.current_shape.move('DOWN')

        # Lock the block in place and proceed to the next tetromino
        self.current_shape.landing = True
        self.landing_checker()

    def calculate_ghost_position(self):
        ghost_blocks = [block.position.copy() for block in self.current_shape.blocks]
        while True:
            moved = [pos + vector(0, 1) for pos in ghost_blocks]
            if any(self.collides(pos) for pos in moved):
                break
            ghost_blocks = moved
        return ghost_blocks

    def collides(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < COLUMNS and y < ROWS:
            if y < 0 or self.game_array[y][x] == 0:
                return False
        return True

    def draw_ghost(self):
        ghost_positions = self.calculate_ghost_position()
        for pos in ghost_positions:
            rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.surface, OUTER_LINE_COLOR, rect, 1)

    def game_over(self):
        # Display game over message or perform any other end-game actions
        print("Game Over!")
        game_over_screen = GameOverScreen(self.game_surface,  self.__score.score, self.lines_cleared_ui.lines_cleared,
                                          self.game_level.level)
        game_over_screen.run()

    def check_game_over(self):
        # Check if any block in the game grid is anchored at the top
        for row in range(ROWS):
            for col in range(COLUMNS):
                block = self.game_array[row][col]
                if block and block.alive and row <= 0:  # Check if block is alive and at or above the top row
                    self.game_over()  # Trigger game over logic

    def update(self, anim_trigger=False):
        current_time = pygame.time.get_ticks()
        # Check if it's time to move the block
        time_interval = FAST_ANIM_TIME_INTERVAL if self.speed_up else  self.__score.DEFAULT_FALL_SPEED
        if current_time - self.last_move_time >= time_interval:
            self.current_shape.update()
            self.last_move_time = current_time
            self.landing_checker()  # Check for landing before removing lines
            self.check_game_over()  # Check for game over condition
        self.sprite_group.update()

    def update_level_surface(self):
        # Update the game level surface
        level_surface = self.game_level.surface
        level_rect = self.game_level.rect
        self.game_surface.blit(level_surface, level_rect)

    def run(self):
        # Draw the game elements on the screen
        self.game_surface.blit(self.surface, (PADDING, PADDING))
        self.draw_grid()
        self.draw_ghost()
        self.sprite_group.draw(self.game_surface)

        # Draw the outline of the game area
        pygame.draw.rect(self.game_surface, OUTER_LINE_COLOR, self.rect, 2)

        # Draw the next block preview
        self.next_block_preview.draw()

        # Adjusted blit position for the score surface
        score_x = WINDOW_WIDTH - SIDEBAR_WIDTH - PADDING  # Align to right side
        score_y = 200  # Top of the window
        self.game_surface.blit( self.__score.surface, (score_x, score_y))  # Blit score surface

        # Adjusted blit position for the lines cleared surface
        lines_cleared_x = WINDOW_WIDTH - SIDEBAR_WIDTH - PADDING  # Align to right side
        lines_cleared_y = 333  # Below score surface
        self.game_surface.blit(self.lines_cleared_ui.surface,
                               (lines_cleared_x, lines_cleared_y))  # Blit lines cleared surface

        # Position for game level UI
        game_level_x = WINDOW_WIDTH - SIDEBAR_WIDTH  # Align to right side
        game_level_y = 465  # Below lines cleared surface
        self.game_surface.blit(self.game_level.surface, (game_level_x, game_level_y))  # Blit game level surface

        pygame.display.flip()