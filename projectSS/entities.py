import pygame
from pygame.locals import *


# For now, player will be represented with red squares.
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.__game = game
        self.__surface = pygame.Surface((30, 30))
        self.__surface.fill((237, 55, 55))
        self.__rectangle = self.__surface.get_rect()

        # Kinematics: Governs the physics of player movement. __vector allows us to make 2D vector variables.
        self.__vector = pygame.math.Vector2
        self.__ACCEL = 0.5
        self.__FRICTION = -0.12     # Can be adjusted to modify player movement
        self.__position = self.__vector((20, 565))
        self.__velocity = self.__vector(0, 0)
        self.__acceleration = self.__vector(0, 0)

    # This method allows us to control our player. Heavy use of physics and kinematics.
    def move(self):
        # Reset acceleration, or else player ends up wobbling back and forth
        self.__acceleration = self.__vector(0, 0)

        # Check if any keyboard keys have been pressed. Modify acceleration accordingly.
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.__acceleration.x = -self.__ACCEL
        if pressed_keys[K_RIGHT]:
            self.__acceleration.x = self.__ACCEL

        # Basic kinematics. They all change based on the acceleration from above.
        self.__acceleration.x += self.__velocity.x * self.__FRICTION
        self.__velocity += self.__acceleration
        self.__position += self.__velocity + 0.5 * self.__acceleration

        # FEATURE: Screen Warping. Player will wrap around screen borders. Can be removed with border acting as barrier.
        if self.__position.x > self.__game.WIDTH:
            self.__position.x = 0
        if self.__position.x < 0:
            self.__position.x = self.__game.WIDTH

        # Update the player rectangle to be at the new position that was calculated above
        self.__rectangle.midbottom = self.__position

    @property
    def surface(self):
        return self.__surface

    @property
    def rectangle(self):
        return self.__rectangle


# For now, platforms will be represented with gray rectangles.
class Platform(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.__game = game
        self.__surface = pygame.Surface((game.WIDTH, 20))
        self.__surface.fill((211, 211, 211))
        self.__rectangle = self.__surface.get_rect(center=(game.WIDTH/2, game.HEIGHT - 10))    # center = spawn position

    @property
    def surface(self):
        return self.__surface

    @property
    def rectangle(self):
        return self.__rectangle
