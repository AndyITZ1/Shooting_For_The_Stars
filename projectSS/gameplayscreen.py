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
        self.__btn_settings = Button(8, 8,
                                     self.game.assets["btn_settings"], self.game.assets["btn_settings_light"],
                                     self.game.show_settings_screen, self.game)
        self.__btn_quit = Button(self.game.WIDTH - 40, 8,
                                 self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                                 sys.exit, self.game)
        self.__buttons = []
        self.__buttons.append(self.__btn_quit)
        self.__buttons.append(self.__btn_settings)

        # Framerate smoothing objects/variables. Used in update() method.
        self.__FPS = 60
        self.__FramePerSecond = pygame.time.Clock()

        # Creation of the player and base platform
        self.__platform1 = Platform(game)
        self.__player = Player(game)

        # Creating a list of sprites and adding platform & player in it. Allows easy sprite access later in code.
        self.__sprites = pygame.sprite.Group()
        self.__sprites.add(self.__platform1)
        self.__sprites.add(self.__player)

    # All game logic and their changes go in this method
    def update(self):
        # This FramePerSecond clock object limits the FPS, determined by the FPS variable. Smooths gameplay.
        self.__FramePerSecond.tick(self.__FPS)
        self.update_buttons()

        # Update the movement of the player
        self.__player.move()

    # All game visuals and their changes go in this method
    def render(self):
        # Draws the background and buttons
        self.game.screen.blit(self.game.assets["game_bg"], (0, 0))
        self.render_buttons()

        # Draw all sprites in our sprite group
        for entity in self.__sprites:
            self.game.screen.blit(entity.surface, entity.rectangle)

    def update_buttons(self):
        for btn in self.__buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.__buttons:
            btn.render()
