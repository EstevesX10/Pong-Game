import pygame

class Button:
    def __init__(self, image:pygame.image, x:int, y:int, scale:float) -> None:
        self.Height = image.get_height() # Defining Button's Height
        self.Width = image.get_width() # Defining Button's Width
        self.scale = scale # Defining a Scale to which the sprite will be resized
        self.image = pygame.transform.scale(image, (int(self.Width*self.scale), int(self.Height*self.scale))) # Resizing the Sprite
        self.rect = self.image.get_rect() # Creating a Rectangle for the Button's Sprite
        self.rect.topleft = (x,y) # Defining the Position where the button must be placed at
        self.clicked = False # Flag that determines if the button has been clicked

        self.FirstContact = 0 # State of the Mouse when he fisrtly approached a button's region
        self.NumContacts = 0 # Total contacts the mouse has made with the button

    def Action(self, Screen:pygame.Surface) -> int:
        Action = False # Flag to determine if the button has been activated
        Mouse_Pos = pygame.mouse.get_pos() # Gets Mouse Position

        if self.rect.collidepoint(Mouse_Pos): # Checks if the mouse position collides with the Button sprite

            if pygame.mouse.get_pressed()[0] == 0: # If the Mouse is not clicking inside a button's region then we can reset the Number of Contacts
                self.clicked = False
                self.NumContacts = 0

            if (self.NumContacts == 0): # Checks if it's the first contact between the mouse and the button [and Stores the Mouse's state]
                self.FirstContact = (pygame.mouse.get_pressed()[0])

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if (self.FirstContact == 0): # The mouse did not reach the Sprite's Area while being pressed on
                    self.clicked = True
                    Action = True
                
            self.NumContacts += 1 # If the Mouse is above the Button then we increment the Number of Contacts

        else: # Resets total Contacts
            self.NumContacts = 0

        # Inserting the Sprite into the Screen
        Screen.blit(self.image, (self.rect.x, self.rect.y)) 

        # Returning if the button was activated
        return Action 