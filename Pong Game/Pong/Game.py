from .Paddle import (Paddle)
from .Ball import (Ball)
import pygame
from Widgets import (Image)
from .Constants import (SCREEN_PADDING, SCREEN_WIDTH, SCREEN_HEIGHT,
                        WHITE, BLACK, LIGHT_RED, RED, DARK_RED, LIGHT_BLUE, BLUE, GREY)


class GameInformation:
    def __init__(self, left_hits:int=None, right_hits:int=None, left_score:int=None, right_score:int=None) -> None:
        self.left_hits = 0 if left_hits is None else left_hits
        self.right_hits = 0 if right_hits is None else right_hits
        self.left_score = 0 if left_score is None else left_score
        self.right_score = 0 if right_score is None else right_score
    
    def _update_score(self, left:bool=False) -> None:
        if left:
            self.left_score += 1
        else:
            self.right_score += 1

    def _update_hits(self, left:bool=False) -> int:
        if left:
            self.left_hits += 1
        else:
            self.right_hits += 1

    def __str__(self) -> str:
        return (f"LEFT PLAYER [{self.left_score}] : [{self.right_score}] RIGHT PLAYER")

class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the game by calling
    .reset().
    """

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)

    def __init__(self) -> None:
        # Referencing the Game Elements
        self.left_paddle = Paddle(SCREEN_PADDING + 10, (SCREEN_HEIGHT - 2*SCREEN_PADDING) // 2 - Paddle.HEIGHT // 2 + SCREEN_PADDING, LIGHT_BLUE)
        self.right_paddle = Paddle(SCREEN_WIDTH - 10 - SCREEN_PADDING - Paddle.WIDTH, (SCREEN_HEIGHT - 2*SCREEN_PADDING) // 2 - Paddle.HEIGHT // 2 + SCREEN_PADDING)
        self.ball = Ball((SCREEN_WIDTH - 2*SCREEN_PADDING) // 2 + SCREEN_PADDING, (SCREEN_HEIGHT - 2*SCREEN_PADDING) // 2 + SCREEN_PADDING)

        # Creating an instance of Game Information to keep track of the scores and hits per player
        self.game_info = GameInformation()

    def _draw_score(self, Window:pygame.Surface) -> None:
        left_score_text = self.SCORE_FONT.render(f"{self.game_info.left_score}", 1, self.left_paddle.COLOR)
        right_score_text = self.SCORE_FONT.render(f"{self.game_info.right_score}", 1, self.right_paddle.COLOR)
        
        Window.blit(left_score_text, ((SCREEN_WIDTH - 2*SCREEN_PADDING) // 4 - left_score_text.get_width() // 2 + SCREEN_PADDING + 70, -7))
        Window.blit(right_score_text, ((SCREEN_WIDTH - 2*SCREEN_PADDING) * (3/4) - right_score_text.get_width() // 2 + SCREEN_PADDING - 70, -7))
        pygame.draw.rect(Window, WHITE, (SCREEN_WIDTH // 2 - 25, SCREEN_PADDING // 2 - 20, 50, 10), 0, 8)

    def _draw_hits(self, Window:pygame.Surface) -> None:
        hits_text = self.SCORE_FONT.render(f"{self.game_info.left_hits + self.game_info.right_hits}", 1, RED)
        Window.blit(hits_text, (SCREEN_WIDTH // 2 - hits_text.get_width() // 2, -7))

    def _draw_divider(self, Window:pygame.Surface) -> None:
        for i in range(SCREEN_PADDING + 10, SCREEN_HEIGHT - SCREEN_PADDING, (SCREEN_HEIGHT - 2*SCREEN_PADDING) // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(Window, WHITE, ((SCREEN_WIDTH - 2*SCREEN_PADDING) // 2 - 5 + SCREEN_PADDING, i, 5, (SCREEN_HEIGHT - SCREEN_PADDING) // 20))

    def _handle_collision(self) -> None:
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= SCREEN_HEIGHT - SCREEN_PADDING:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= SCREEN_PADDING:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1
                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.game_info._update_hits(left=True)

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1
                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.game_info._update_hits(left=False)

    def draw(self, Window:pygame.Surface, draw_score:bool=True, draw_hits:bool=False) -> None:
        # Creating the Background
        Window.fill(GREY)
        PC_IMG = pygame.image.load('./Assets/PC.png').convert_alpha()
        PC = Image(PC_IMG, -88, -140, 2.7)
        PC.Display(Window)

        # pygame.draw.rect(Window, WHITE, (SCREEN_PADDING, SCREEN_PADDING, SCREEN_WIDTH - 2*SCREEN_PADDING + 23, SCREEN_HEIGHT - 2*SCREEN_PADDING + 23), 0, 10)
        pygame.draw.rect(Window, GREY , (SCREEN_PADDING - 13, SCREEN_PADDING - 15, SCREEN_WIDTH - 2*SCREEN_PADDING + 26, SCREEN_HEIGHT - 2*SCREEN_PADDING + 35), 0, 10)
        pygame.draw.rect(Window, LIGHT_RED, (SCREEN_PADDING-10, SCREEN_PADDING-10, SCREEN_WIDTH - 2*SCREEN_PADDING + 20, SCREEN_HEIGHT - 2*SCREEN_PADDING + 20), 0, 16)
        pygame.draw.rect(Window, RED, (SCREEN_PADDING, SCREEN_PADDING, SCREEN_WIDTH - 2*SCREEN_PADDING, SCREEN_HEIGHT - 2*SCREEN_PADDING), 0, 10)
        self._draw_divider(Window)

        if draw_score:
            self._draw_score(Window)

        if draw_hits:
            self._draw_hits(Window)

        self.left_paddle.draw(Window, left=True)
        self.right_paddle.draw(Window, left=False)
        self.ball.draw(Window)

    def move_paddle(self, left:bool=True, up:bool=True) -> bool:
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        """
        if left:
            if up and self.left_paddle.y - Paddle.VEL < SCREEN_PADDING:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > SCREEN_HEIGHT - SCREEN_PADDING - 5:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < SCREEN_PADDING:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > SCREEN_HEIGHT - SCREEN_PADDING - 5:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self) -> GameInformation:
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self._handle_collision()

        if self.ball.x < SCREEN_PADDING:
            self.ball.reset()
            self.game_info._update_score(left=False)

        elif self.ball.x > SCREEN_WIDTH - SCREEN_PADDING:
            self.ball.reset()
            self.game_info._update_score(left=True)

        return self.game_info

    def reset(self) -> None:
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.game_info = GameInformation()