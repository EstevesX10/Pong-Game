import pygame
pygame.init()
import os
import neat
import pickle
from Pong import (SCREEN_WIDTH, SCREEN_HEIGHT, Game)

class PongGame:
    def __init__(self, Window:pygame.Surface, config:neat.Config) -> None:
        # Creating a instance of the Game Class
        self.game = Game()

        # Saving the Game's Paddles as well as the Ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

        # Creating a variable for the Configuration
        self.config = config

        # Creating a Screen for the Application
        self.window = Window

    def Test_AI(self, Genome:neat.DefaultGenome) -> None:
        # Create a Network for the best genome
        Network = neat.nn.FeedForwardNetwork.create(Genome, self.config)
        
        # Flag to control the flow of the game
        run = True

        # Creating a Clock to Control the Ball's Movement
        # by later limiting the number of frames to render
        clock = pygame.time.Clock()

        while run:
            clock.tick(60) # Setting the Clock to max fps = 60 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # Getting the list of keys the user has pressed
            keys = pygame.key.get_pressed()

            # Setting the Paddle's Movement Mechanics
            if keys[pygame.K_w]: # Left Paddle Up
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]: # Left Paddle Down
                self.game.move_paddle(left=True, up=False)
            
            # Feed the Right Paddle's Network with the y pos of the padde, the y pos of the ball and the distance between the paddle and the ball
            Output_Network = Network.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            # Save the best decision threshold [the one that allowed to obtain the greater output]
            Decision = Output_Network.index(max(Output_Network))

            # Discriminating the Right Paddle's Movement based on the Network's Output
            if Decision == 0: # Stay Still
                pass
            elif Decision == 1: # Move Up
                self.game.move_paddle(left=False, up=True)
            else: # Move Down
                self.game.move_paddle(left=False, up=False)

            self.game.loop()
            self.game.draw(self.window, True, False)
            pygame.display.update()
        pygame.quit()

    def run(self) -> None:
        # Initializing Window / Screen
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong-Game")
        ICON_PATH = pygame.image.load('Assets/Icons/Pong_Icon.png').convert_alpha()
        ICON_IMG = pygame.image.load(ICON_PATH).convert_alpha()
        pygame.display.set_icon(ICON_IMG)
        
        # Add Buttons


        # Main Loop
        run = True
        while run:
            pass
        
        pygame.quit()

def Test_AI(config):
    # Creating a Window
    Window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load the best NN
    with open("Best_Neural_Network.pickle", "rb") as f:
        best_neural_network = pickle.load(f)

    # Creating a Pong Game instance to Test the saved model
    Game = PongGame(Window, config)
    Game.Test_AI(best_neural_network)

if __name__ == "__main__":
    # Loading the Configuration
    local_dir = os.path.dirname(__file__)
    configuration_path = os.path.join(local_dir, "config.txt")
    configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_path)
    
    Test_AI(configuration)
    # App = PongGame()