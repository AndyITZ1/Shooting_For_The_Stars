import time
import random
import os
import sys
import pygame
import pygame.math
from projectSS.gamescreen import GameScreen
from projectSS.menus import Button
from projectSS.entities import *


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

        # Creating a list of sprites, platforms, and powerups. Allows easy sprite access.
        self.entities = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()  # Used in player update() method.
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pushers = pygame.sprite.Group()

        self.camera_y = 0

        # Despawn point for entities
        self.despawn_y = self.camera_y + self.game.HEIGHT + 32

        self.player = Player(self)

        # Keeping track of distance for score
        self.best_distance = 0
        self.progress = 0
        self.times_hit = 0
        self.goal = False

        # Variables for enemy generation, each 500 dist roll a 1/10 chance to generate a new enemy
        self.enemy_dist = 0
        self.rand_dist = 0

    def on_show(self):

        # Reset variables
        self.camera_y = -self.game.HEIGHT + 10
        self.despawn_y = self.camera_y + self.game.HEIGHT + 32
        self.best_distance = 0
        self.enemy_dist = 0
        self.times_hit = 0
        self.goal = False
        self.progress = 0
        self.rand_dist = 0

        self.player.reset()

        for e in self.entities:
            e.kill()

        # Add base platform
        base_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, 0)
        base_platform.surf.fill((255, 0, 0))

        self.gen_platforms(True)

        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/retrofunk.mp3'))
        pygame.mixer.music.play(-1)

    def gen_platforms(self, whole_screen=False):

        # TODO: Adjust platform position generation
        # Don't use a check function and infinite loop like before
        # Instead, base the random position on existing platforms
        # For whole_screen=True, generate one platform first, then the rest based on the first

        while len(self.platforms) < 7:
            # Set width/position
            width = random.randrange(50, 100)
            x = random.randrange(0, self.game.WIDTH - width)

            # Generate platforms at the top of the screen, just offscreen
            y = self.camera_y - random.randrange(10, 50)

            # Generate platforms on the entire screen
            if whole_screen:
                y = self.camera_y + random.randrange(20, self.game.HEIGHT - 60)

            # Create platform
            plat = Platform(self, width, x, y)

            # Random powerup spawn
            if random.randrange(100) < 15:
                p = Powerup(self, x, y - 25)
            elif random.randrange(100) < 22:
                p = Pusher(self, x, y-23, plat)

    # enemy generation algorithm 300 to 1200 spaces after 1000, maximum is lowered by 100 every 1000
    def gen_enemies(self):
        if self.progress > 1000 and len(self.enemies) < 3:
            if self.rand_dist == 0:
                self.rand_dist = random.randrange(300, max(500, 1200 - 100 * (self.progress - 1000)//1000))
                self.enemy_dist = self.progress
            if self.progress - self.enemy_dist > self.rand_dist:
                Enemy(self,
                      random.randrange(self.game.WIDTH//6, self.game.WIDTH//4),  # Platform span
                      random.randrange(0, self.game.WIDTH//2),                  # Platform x
                      self.camera_y - 15)
                self.rand_dist = 0

    # generates the goal if the progress bar is filled
    def gen_goal(self):
        # Add goal
        self.goal = True
        goal_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, self.camera_y-500)
        goal_platform.surf.fill((255, 215, 0))

    # All game logic and their changes go in this method
    def update(self):
        self.update_buttons()
        self.entities.update()
        self.player.update()

        # Check if player has hit an enemy, lowering progress by 1500
        if self.player.hit:
            self.player.hit = False
            self.times_hit += 1
            self.progress = self.best_distance - 1500*self.times_hit
            self.rand_dist = 0

        # Check if the player has died
        if not self.player.alive or self.progress < 0:
            self.game.show_game_over_screen()

        # allows for screen to scroll up and destroy
        if self.player.rect_render.top <= self.game.HEIGHT / 4:
            self.camera_y = self.player.rect.top - self.game.HEIGHT / 4
            self.despawn_y = self.camera_y + self.game.HEIGHT + 32

        # Tracking player distance/progress, adjusted to start point
        if self.player.pos.y + 25 < -self.best_distance:
            self.best_distance = -(self.player.pos.y + 25)
            self.progress = -(self.player.pos.y + 25) - 1500*self.times_hit

        # Generate platforms and enemies
        if self.progress < 9500:
            self.gen_platforms()
            self.gen_enemies()
        elif not self.goal:
            self.gen_goal()

    # All game visuals and their changes go in this method
    def render(self):
        # Draws the background and buttons
        self.game.screen.blit(self.game.assets["bg_game"], (0, 0))

        for e in self.entities:
            e.render()

        self.player.render()

        self.render_buttons()

        # Draw progress bar
        self.draw_progress()

        # Draw current score
        self.game.draw_text(str(round(self.progress)), 30, self.game.WIDTH/2, 50)

    def draw_progress(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.WIDTH/3, 10, self.game.WIDTH/3, 20), 3, 5, 5, 5, 5)
        pygame.draw.rect(self.game.screen, (76, 187, 23), (self.game.WIDTH/3+2, 12,
                                                           min(self.game.WIDTH/3*(self.progress/10000),
                                                               self.game.WIDTH/3-2), 16), 0, 5, 5, 5, 5)

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
