import sys
import pygame.math
from projectSS.gamescreen import GameScreen
from projectSS.menus import Button
from projectSS.entities import Player, Platform


# TODO: write clean code pls


class GameplayScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        # Create two buttons so player can enter settings or exit game. Add them to our buttons list
        self.btn_settings = Button(8, 8,
                                   self.game.assets["btn_settings"], self.game.assets["btn_settings_light"],
                                   self.game.show_settings_screen, self.game)
        self.btn_quit = Button(self.game.WIDTH - 40, 8,
                               self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                               sys.exit, self.game)
        self.buttons = []
        self.buttons.append(self.btn_quit)
        self.buttons.append(self.btn_settings)

        # Initializing gameplay and calculation variables
        self.__vector = pygame.math.Vector2
        self.__acceleration = 0.5
        self.__friction = -0.12
        self.__FPS = 60
        self.__FramePerSecond = pygame.time.Clock()

        # Creation of the player and base platform
        self.__platform1 = Platform(game)
        self.__player = Player(game)

    def update(self):
        self.update_buttons()

    def render(self):
        # Draws the background using the image
        self.game.screen.blit(self.game.assets["game_bg"], (0, 0))
        self.render_buttons()

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
