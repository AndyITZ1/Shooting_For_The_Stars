import pygame


# For now, player will be represented with red squares.
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.__game = game
        self.__surface = pygame.Surface((30, 30))
        self.__surface.fill((237, 55, 55))
        self.__rectangle = self.__surface.get_rect(center=(10, 420))


# For now, platforms will be represented with gray rectangles.
class Platform(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.__game = game
        self.__surface = pygame.Surface((game.WIDTH, 20))
        self.__surface.fill((211, 211, 211))
