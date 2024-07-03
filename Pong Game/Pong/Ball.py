import pygame
import math
import random
from .Constants import (WHITE, BALL_RADIUS, BALL_MAX_VEL)

class Ball:
    MAX_VEL = BALL_MAX_VEL # Defining the Max Velocity
    RADIUS = BALL_RADIUS # Defining the Ball's Radius
    MAIN_COLOR = WHITE # Defining the Ball's Color

    def __init__(self, X:int, Y:int) -> None:
        self.initial_x = self.x = X
        self.initial_y = self.y = Y
        
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    def _get_random_angle(self, min_angle:int, max_angle:int, excluded:list) -> int:
        # Getting a Random Angle to impact the Ball's movement 
        # when it is going straight horizontaly
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle

    def draw(self, Window:pygame.Surface) -> None:
        pygame.draw.circle(Window, self.MAIN_COLOR, (self.x, self.y), self.RADIUS)

    def move(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self) -> None:
        self.x = self.initial_x
        self.y = self.initial_y
        
        self.angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(self.angle) * self.MAX_VEL)
        y_vel = math.sin(self.angle) * self.MAX_VEL

        self.y_vel = y_vel
        self.x_vel *= -1