import random
import sys

import pygame
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
        self.PT1.surf = pygame.Surface((game.WIDTH, 20))
        self.PT1.surf.fill((255, 0, 0))
        self.PT1.rect = self.PT1.surf.get_rect(center = (game.WIDTH / 2, game.HEIGHT - 10))
        self.P1 = Player(game, self)

        # Creating a list of sprites and adding platform & player in it. Allows easy sprite access later in code.
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.PT1)
        self.all_sprites.add(self.P1)

        # Creating a list of platforms. Allows easy platform collision detection. Used in player update() method.
        self.platforms = pygame.sprite.Group()
        self.platforms.add(self.PT1)

        for x in range(random.randint(5,6)):
            pl = Platform(game)
            self.platforms.add(pl)
            self.all_sprites.add(pl)

    def plat_gen(self):
        while len(self.platforms) < 7 :
            width = random.randrange(50, 100)
            p = Platform(self.game)
            p.rect.center = (random.randrange(0, self.game.WIDTH - width), random.randrange(-50, 0))
            self.platforms.add(p)
            self.all_sprites.add(p)

    # All game logic and their changes go in this method
    def update(self):
        # This FramePerSecond clock object limits the FPS, determined by the FPS variable. Smooths gameplay.
        self.FramePerSec.tick(self.FPS)
        self.update_buttons()

        # allows for screen to scroll up and destroy
        if self.P1.rect.top <= self.game.HEIGHT / 3:
            self.P1.pos.y += abs(self.P1.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.P1.vel.y)
                if plat.rect.top >= self.game.HEIGHT:
                    plat.kill()

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

        # Creates platforms as screen scrolls upward
        self.plat_gen()

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
