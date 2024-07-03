from .Paddle import (Paddle)
from .Ball import (Ball)
import pygame
import random
from .Constants import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED)

class GameInformation:
    def __init__(self, left_hits=None, right_hits=None, left_score=None, right_score=None):
        self.left_hits = 0 if left_hits is None else left_hits
        self.right_hits = 0 if right_hits is None else right_hits
        self.left_score = 0 if left_score is None else left_score
        self.right_score = 0 if right_score is None else right_score
    
    def _update_score(self, left=False):
        if left:
            self.left_score += 1
        else:
            self.right_score += 1

    def _update_hits(self, left=False):
        if left:
            self.left_hits += 1
        else:
            self.right_hits += 1

    def __str__(self):
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

    def __init__(self):
        # Referencing the Game Elements
        self.left_paddle = Paddle(10, SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(SCREEN_WIDTH - 10 - Paddle.WIDTH, SCREEN_HEIGHT // 2 - Paddle.HEIGHT // 2)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Creating an instance of Game Information to keep track of the scores and hits per player
        self.game_info = GameInformation()

    def _draw_score(self, Window):
        left_score_text = self.SCORE_FONT.render(f"{self.game_info.left_score}", 1, WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.game_info.right_score}", 1, WHITE)
        
        Window.blit(left_score_text, (SCREEN_WIDTH // 4 - left_score_text.get_width() // 2, 20))
        Window.blit(right_score_text, (SCREEN_WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    def _draw_hits(self, Window):
        hits_text = self.SCORE_FONT.render(f"{self.game_info.left_hits + self.game_info.right_hits}", 1, RED)
        Window.blit(hits_text, (SCREEN_WIDTH // 2 - hits_text.get_width() // 2, 10))

    def _draw_divider(self, Window):
        for i in range(10, SCREEN_HEIGHT, SCREEN_HEIGHT//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(Window, WHITE, (SCREEN_WIDTH // 2 - 5, i, 10, SCREEN_HEIGHT // 20))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        if ball.y + ball.RADIUS >= SCREEN_HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
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

    def draw(self, Window, draw_score=True, draw_hits=False):
        Window.fill(BLACK)
        self._draw_divider(Window)

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(Window)

        self.ball.draw(Window)

    def move_paddle(self, left=True, up=True):
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        """
        if left:
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.left_paddle.y + Paddle.HEIGHT > SCREEN_HEIGHT:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > SCREEN_HEIGHT:
                return False
            self.right_paddle.move(up)

        return True

    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self._handle_collision()

        if self.ball.x < 0:
            self.ball.reset()
            self.game_info._update_score(left=False)

        elif self.ball.x > SCREEN_WIDTH:
            self.ball.reset()
            self.game_info._update_score(left=True)

        return self.game_info

    def reset(self):
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.game_info = GameInformation()

if __name__ == "__main__":
    pygame.init()
    WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(WINDOW)
    outcome = game.loop()
    print(outcome)