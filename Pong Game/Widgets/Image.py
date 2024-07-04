import pygame

class Image:
    def __init__(self, image:pygame.image, x:int, y:int, scale:float) -> None:
        self.Height = image.get_height() # Defining Image's Height
        self.Width = image.get_width() # Defining Image's Width
        self.scale = scale # Defining a Scale to which the sprite will be resized
        self.image = pygame.transform.scale(image, (int(self.Width*self.scale), int(self.Height*self.scale))) # Resizing the Sprite
        self.rect = self.image.get_rect() # Creating a Rectangle for the Image's Sprite
        self.rect.topleft = (x,y) # Defining the Position where the image must be placed at

    def Display(self, screen:pygame.Surface) -> None:
        screen.blit(self.image, (self.rect.x, self.rect.y)) # Displaying the Image into the given Screen