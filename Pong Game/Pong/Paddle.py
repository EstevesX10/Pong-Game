import pygame
from .Constants import (WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)

class Paddle:
    VEL = PADDLE_VEL # Velocity of the Paddles
    WIDTH = PADDLE_WIDTH
    HEIGHT = PADDLE_HEIGHT

    def __init__(self, X:int, Y:int, Color:tuple=None) -> None:
        self.initial_x = self.x = X
        self.initial_y = self.y = Y
        self.COLOR = WHITE if Color is None else Color

    def draw(self, Window:pygame.Surface) -> None:
        pygame.draw.rect(Window, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT), 0, 8)

    def move(self, up:bool=True) -> None:
        if (up):
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self) -> None:
        self.x = self.initial_x
        self.y = self.initial_y