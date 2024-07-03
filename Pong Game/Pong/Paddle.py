import pygame
from .Constants import (WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL)

class Paddle:
    COLOR = WHITE # Color for the Paddles
    VEL = PADDLE_VEL # Velocity of the Paddles
    WIDTH = PADDLE_WIDTH
    HEIGHT = PADDLE_HEIGHT

    def __init__(self, X, Y):
        self.initial_x = self.x = X
        self.initial_y = self.y = Y

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        if (up):
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y

if __name__ == "__main__":
    pygame.init()
    # TEST CODE HERE    