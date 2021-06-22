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

        # Framerate smoothing objects/variables. Used in update() method.
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()

        # Creation of the player and base platform
        self.PT1 = Platform(game)
        self.P1 = Player(game, self)

        # Creating a list of sprites and adding platform & player in it. Allows easy sprite access later in code.
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.PT1)
        self.all_sprites.add(self.P1)

        # Creating a list of platforms. Allows easy platform collision detection. Used in player update() method.
        self.platforms = pygame.sprite.Group()
        self.platforms.add(self.PT1)

    # All game logic and their changes go in this method
    def update(self):
        # This FramePerSecond clock object limits the FPS, determined by the FPS variable. Smooths gameplay.
        self.FramePerSec.tick(self.FPS)
        self.update_buttons()

        # Update the movement of the player
        self.P1.move()
        self.P1.update()

    # All game visuals and their changes go in this method
    def render(self):
        # Draws the background and buttons
        self.game.screen.blit(self.game.assets["game_bg"], (0, 0))
        self.render_buttons()

        # Draw all sprites in our sprite group
        for entity in self.all_sprites:
            self.game.screen.blit(entity.surf, entity.rect)

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
