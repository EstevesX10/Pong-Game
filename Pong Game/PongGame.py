import pygame
pygame.init()
import os
import neat
import pickle
from Pong import (SCREEN_WIDTH, SCREEN_HEIGHT, Game)
from Pong.Constants import (BLACK, WHITE, GREY, LIGHT_BLUE)
from Widgets import (Button, Image)

class PongGame:
    def __init__(self, Config:neat.Config, Best_Genome:neat.DefaultGenome) -> None:
        # Creating a Window/Screen for the Application
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Creating a instance of the Game Class
        self.game = Game()

        # Saving the Game's Paddles as well as the Ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

        # Creating a variable for the Configuration
        self.config = Config

        # Creating a Variable to store the Best Genome [Best NN obtained]
        self.best_genome = Best_Genome

        # Create a Network for the best genome
        self.network = neat.nn.FeedForwardNetwork.create(Best_Genome, Config)

    def write(self, font:str, text:str, size:tuple, color:str, bg_color:str, bold:bool, pos:tuple) -> None:
        # Writes Text into the Screen
        letra = pygame.font.SysFont(font, size, bold)
        frase = letra.render(text, 1, color, bg_color)
        self.window.blit(frase, pos)

    def run(self) -> None:
        # Customizing the Window
        pygame.display.set_caption("Pong Game")
        ICON_IMG = pygame.image.load('./Assets/Pong_Icon.png').convert_alpha()
        pygame.display.set_icon(ICON_IMG)

        # Variable to store the current menu
        menu = "Main_Menu"
        # menu = "Modes_Menu"
        # menu = "PVP"

        # Creating Wallpapers
        BG_IMG = pygame.image.load('./Assets/Pong_Game_BG.jpg').convert_alpha()
        Main_Menu = Image(BG_IMG, -160, 65, .4)

        # Creating Buttons
        START_IMG = pygame.image.load('./Assets/Start.png').convert_alpha()
        Start_Btn = Button(START_IMG, 420, 190, 0.4)

        BACK_IMG = pygame.image.load('./Assets/Back.png').convert_alpha()
        Back_Btn = Button(BACK_IMG, 20, 20, 0.1)

        PVP_IMG = pygame.image.load('./Assets/PVP.png').convert_alpha()
        PVP_Btn = Button(PVP_IMG, 160, 190, 0.22)

        AI_IMG = pygame.image.load('./Assets/AI.png').convert_alpha()
        AI_Btn = Button(AI_IMG, 440, 190, 0.22)

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
            
            if menu == "Main_Menu":
                # Customizing the Main Menu of the Application
                self.window.fill(GREY)
                Main_Menu.Display(self.window)
                self.write(font='Arial', text=" Pong Game ", size=50, color=GREY, bg_color=WHITE, bold=True, pos=((SCREEN_WIDTH - 230) // 2, 40))

                # Use a Start Button to initialize the Game
                if Start_Btn.Action(self.window):
                    menu = "Modes_Menu"

            elif menu == "Modes_Menu":
                # Reset the Game every time we switch Game Mode
                self.game.reset()

                # Customizing the Section of the App
                self.window.fill(GREY)  
                self.write(font='Arial', text=" Game Modes ", size=40, color=GREY, bg_color=WHITE, bold=True, pos=(250, 60))
                self.write(font='Arial', text=" PVP ", size=30, color=GREY, bg_color=WHITE, bold=True, pos=(185, 330))
                self.write(font='Arial', text=" AI → NEAT ", size=30, color=GREY, bg_color=WHITE, bold=True, pos=(422, 330))

                # Use Buttons to manage the flow of the application
                if (Back_Btn.Action(self.window)):
                    menu = "Main_Menu"
                if (AI_Btn.Action(self.window)):
                    menu = "AI"
                if (PVP_Btn.Action(self.window)):
                    menu = "PVP"

            elif menu == "PVP":
                # Getting the list of keys the user has pressed
                keys = pygame.key.get_pressed()

                # Setting the Paddle's Movement Mechanics
                if keys[pygame.K_w]: # Left Paddle Up
                    self.game.move_paddle(left=True, up=True)
                if keys[pygame.K_s]: # Left Paddle Down
                    self.game.move_paddle(left=True, up=False)
                if keys[pygame.K_UP]: # Right Paddle Up
                    self.game.move_paddle(left=False, up=True)
                if keys[pygame.K_DOWN]: # Right Paddle Down
                    self.game.move_paddle(left=False, up=False)
                
                # Bind the R key to easily restart the Game
                if keys[pygame.K_r]:
                    self.game.reset()
            
                self.game.loop()
                self.game.draw(self.window, True, False)

                # Return to Modes Menu [Using the Back_Btn]
                if (Back_Btn.Action(self.window)):
                    menu = "Modes_Menu"

            elif menu == "AI":
                # Getting the list of keys the user has pressed
                keys = pygame.key.get_pressed()

                # Setting the Paddle's Movement Mechanics
                if keys[pygame.K_w] or keys[pygame.K_UP]: # Left Paddle Up
                    self.game.move_paddle(left=True, up=True)
                if keys[pygame.K_s] or keys[pygame.K_DOWN]: # Left Paddle Down
                    self.game.move_paddle(left=True, up=False)
                
                # Bind the R key to easily restart the Game
                if keys[pygame.K_r]:
                    self.game.reset()
                
                # Feed the Right Paddle's Network with the y pos of the padde, the y pos of the ball and the distance between the paddle and the ball
                Output_Network = self.network.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
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

                # Return to Modes Menu [Using the Back_Btn]
                if (Back_Btn.Action(self.window)):
                    menu = "Modes_Menu"

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":

    # Loading the Configuration
    local_dir = os.path.dirname(__file__)
    configuration_path = os.path.join(local_dir, "config.txt")
    configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration_path)
    
    # Load the best NN
    with open("Best_Neural_Network.pickle", "rb") as f:
        best_neural_network = pickle.load(f)

    # Run the Application
    App = PongGame(configuration, best_neural_network)
    App.run()