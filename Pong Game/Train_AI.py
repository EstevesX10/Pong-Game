import neat.genome
import pygame
import os
import neat
import pickle
from Pong import (SCREEN_WIDTH, SCREEN_HEIGHT, Game)

class Train_AI_Pong_Game:
    def __init__(self, Window:pygame.Surface, Width:int, Height:int) -> None:
        # Creating a instance of the Game Class
        self.game = Game(Window, Width, Height)

        # Saving the Game's Paddles as well as the Ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def Train_AI(self, Genome_1:neat.genome, Genome_2:neat.genome, config:neat.Config) -> None:
        # Creating 2 Networks for each "AI" player
        Network_1 = neat.nn.FeedForwardNetwork.create(Genome_1, config)
        Network_2 = neat.nn.FeedForwardNetwork.create(Genome_2, config)
        
        # Game Loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Feed the Left Paddle's Network with the y pos of the padde, the y pos of the ball and the distance between the paddle and the ball
            Output_Network_1 = Network_1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            # Save the best decision threshold [the one that allowed to obtain the greater output]
            Decision_1 = Output_Network_1.index(max(Output_Network_1))
            
            # Discriminating the Left Paddle's Movement based on the Network's Output
            if Decision_1 == 0: # Stay Still
                pass
            elif Decision_1 == 1: # Move Up
                self.game.move_paddle(left=True, up=True)
            else: # Move Down
                self.game.move_paddle(left=True, up=False)

            # Feed the Right Paddle's Network with the y pos of the padde, the y pos of the ball and the distance between the paddle and the ball
            Output_Network_2 = Network_2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            # Save the best decision threshold [the one that allowed to obtain the greater output]
            Decision_2 = Output_Network_2.index(max(Output_Network_2))

            # Discriminating the Right Paddle's Movement based on the Network's Output
            if Decision_2 == 0: # Stay Still
                pass
            elif Decision_2 == 1: # Move Up
                self.game.move_paddle(left=False, up=True)
            else: # Move Down
                self.game.move_paddle(left=False, up=False)

            Game_Info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            # End the Game and Discard the worst paddle [The one that missed the ball] (We also limit the max amount of hits we can obtain in order to prevent extensive trainning)
            if Game_Info.left_score >= 1 or Game_Info.right_score >= 1 or Game_Info.left_hits > 50:
                self.Calculate_Fitness_Score(Genome_1, Genome_2, Game_Info)
                break

    def Calculate_Fitness_Score(self, Genome_1:neat.genome, Genome_2:neat.genome, Game_Info:Game) -> None:
        Genome_1.fitness += Game_Info.left_hits
        Genome_2.fitness += Game_Info.right_hits

def Evaluate_Genomes(genomes:neat.Population, config:neat.Config) -> None:
    """Score function used to evaluate the performance of a given genome"""
    
    # Creating a Window
    Window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    for i, (Genome_ID1, Genome_1) in enumerate(genomes):
        if i == len(genomes) - 1: # Used to Prevent the index out of range error
            break
        Genome_1.fitness = 0
        for Genome_ID2, Genome_2 in genomes[i+1:]:
            if Genome_2.fitness is None:
                Genome_2.fitness = 0
            game = Train_AI_Pong_Game(Window, SCREEN_WIDTH, SCREEN_HEIGHT)
            game.Train_AI(Genome_1, Genome_2, config)

def Run_NEAT(config:neat.Config, save_model:bool=True) -> None:
    # To start from a Checkpoint we would load it instead of creating one from scratch
    # population = neat.Checkpointer.restore_checkpoint('<CHECKPOINT_PATH>')

    # Creating a Population
    population = neat.Population(config)
    
    # Report Data to the Standard Output
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Save a Checkpointer at each new generation (1) -> Allows the algorithm to start from the checkpoint instead from the start 
    population.add_reporter(neat.Checkpointer(1))

    # Passing a function Evaluate_Genomes to evaluate the performance of each genome at each new generation
    # This process goes on for a maximum of 50 generations
    best_neural_network = population.run(Evaluate_Genomes, 2)

    # Save the Trained Model
    if save_model:
        # Pickle helps to save an entire python object [In this case we are saving the best NN obtained by the Algorithm]
        with open("Best_Neural_Network.pickle", "wb") as f:
            pickle.dump(best_neural_network, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    configuration_path = os.path.join(local_dir, "config.txt")
    configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_path)
    Run_NEAT(configuration, save_model=False)