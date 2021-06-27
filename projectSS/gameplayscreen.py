import time
import random
import sys
import pygame
import pygame.math
from projectSS.gamescreen import GameScreen
from projectSS.menus import Button
from projectSS.entities import Player, Platform, Enemy


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

        # Creating a list of sprites, platforms, and powerups. Allows easy sprite access.
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()  # Used in player update() method.
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Creation of the player and base platform. Base platform colored red
        self.PT1 = Platform(game, self, game.WIDTH, game.WIDTH / 2, game.HEIGHT - 10)
        self.PT1.surf.fill((255, 0, 0))
        self.P1 = Player(game, self)

        # self.all_sprites.add(self.P1)
        # self.all_sprites.add(self.PT1)
        # self.platforms.add(self.PT1)

        # Keeping track of distance for score
        self.total_distance = 0
        self.best_distance = 0

        # Stuff for enemy generation, each 500 dist roll a 1/10 chance to generate a new enemy
        self.enemy_dist = 0

        # Putting gameover screen here


        for x in range(6):  # TODO: Adjust number of starting platforms
            width = random.randrange(50, 100)
            # pl =
            Platform(game, self, width, random.randrange(0, game.WIDTH - width), random.randrange(0, game.HEIGHT - 60))
            # check = True
            # while check:
            #     pl = Platform(game, self, width, random.randrange(0, game.WIDTH - width), random.randrange(0, game.HEIGHT - 60))
            #     check = self.check_plat(pl, self.platforms)
            # self.all_sprites.add(pl)
            # self.platforms.add(pl)

    # Check to see if newly generated platform is "decently" spaced from other previously-gen platforms
    def check_plat(self, platform, group_plat):
        if pygame.sprite.spritecollideany(platform, group_plat):
            return True
        else:
            for entity in group_plat:
                if entity == platform:
                    continue
                # TODO: Find appropriate spacing value between platforms.
                # Note: Values above 50 may cause freezing of game.
                # print("PRT %d PRB %d ERB %d ERT %d" % (platform.rect.top, platform.rect.bottom, entity.rect.bottom, entity.rect.top))
                if (abs(platform.rect.top - entity.rect.bottom) < 80) and (
                        abs(platform.rect.bottom - entity.rect.top) < 80):
                    return True
            return False

    def plat_gen(self):
        while len(self.platforms) < 7:
            width = random.randrange(50, 100)
            # p =
            Platform(self.game, self, width, random.randrange(0, self.game.WIDTH - width), random.randrange(-95, -30))
            # check = True
            # while check:
            #     p = Platform(self.game, self, width, random.randrange(0, self.game.WIDTH - width), random.randrange(-95, -30))
            #     # TODO: Adjust platform center height in accordance with checking platform spacing.
            #     check = self.check_plat(p, self.platforms)
            # self.all_sprites.add(p)
            # self.platforms.add(p)

    # enemy generation algorithm 30% every 500 spaces after 1500
    def enemy_gen(self):
        if self.best_distance > 1500 and len(self.enemies) < 3:
            if self.best_distance - self.enemy_dist > 500:
                if random.random() >= 0.7:
                    self.enemies.add(Enemy(self.game, self, 30, self.game.WIDTH/2))
                self.enemy_dist = self.best_distance

    # All game logic and their changes go in this method
    def update(self):
        # This FramePerSecond clock object limits the FPS, determined by the FPS variable. Smooths gameplay.
        self.FramePerSec.tick(self.FPS)
        self.update_buttons()
        self.all_sprites.update()

        # allows for screen to scroll up and destroy
        if self.P1.rect.top <= self.game.HEIGHT / 3:
            self.P1.pos.y += abs(self.P1.vel.y)
            self.total_distance += abs(self.P1.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.P1.vel.y)
                if plat.rect.top >= self.game.HEIGHT:
                    plat.kill()
            for enem in self.enemies:
                enem.pos.y += abs(self.P1.vel.y)
        # Player is holding space key? Jump until max jump height is reached. Space key is let go? Stop jump.
        if self.game.player_jump:
            self.P1.jump()
        if self.game.player_jump_c:
            self.P1.cancel_jump()

        # Update the movement of the player
        self.P1.move()
        self.P1.update()

        # Check if the player has died
        if not self.P1.alive:
            self.game.show_game_over_screen()

        # Tracking player distance/progress
        if self.total_distance > self.best_distance:
            self.best_distance = self.total_distance

    # All game visuals and their changes go in this method
    def render(self):
        # Draws the background and buttons
        self.game.screen.blit(self.game.assets["game_bg"], (0, 0))
        self.render_buttons()

        # Draw all sprites in our sprite group
        for entity in self.all_sprites:
            self.game.screen.blit(entity.surf, entity.rect)

        # Draw current score
        self.game.draw_text(str(int(self.best_distance)), 30, self.game.WIDTH/2, 20)

        # Creates platforms as screen scrolls upward
        self.plat_gen()

        self.enemy_gen()

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
