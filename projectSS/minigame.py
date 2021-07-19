import os
import random
from math import sqrt
import pygame
from projectSS.gamescreen import GameScreen


class ClickedTooLate(Exception):

    def __init__(self, message="Didn't click the minigame button in time"):
        self.message = message


class Ring(pygame.sprite.Sprite):

    def __init__(self, x, y, sprite, game):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = sprite
        self.game = game

        self.width = sprite.get_width()
        self.height = sprite.get_height()
        self.outer_radius = 200  # Outer ring starting outer_radius.
        self.inner_radius = self.width / 2  # Inner sprite radius. Used in collision detection

        self.mouse_hover = False  # Boolean used in mouse detection.

    def update(self):
        # Checks if mouse is hovering over the sprite using the sprite's position and size.
        self.mouse_hover = (self.x <= self.game.mouse_pos[0] < self.x + self.width and
                            self.y <= self.game.mouse_pos[1] < self.y + self.height)

        if self.mouse_hover and self.game.mouse_clicked and 52 <= self.outer_radius <= 67:
            self.game.assets["sfx_blip"].play()
            return True
        else:
            if self.outer_radius < 52:
                raise ClickedTooLate
            self.outer_radius -= 1.75

    def render(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))
        pygame.draw.circle(self.game.screen, (134, 144, 250), (self.x + 64, self.y + 64), self.outer_radius, width=3)

    def center(self):
        return self.x + self.width, self.y + self.height

    @property
    def radius(self):
        return self.inner_radius


class MinigameScreen(GameScreen):

    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.counting_down = True
        self.start_ticks = None  # Countdown ticks
        self.ring_ticks = None  # Ring spawn ticks
        self.counter = 7
        self.counter_str = str(self.counter)
        self.active_circles = []
        self.dormant_circles = []
        self.max_spawn_time = 1.8  # TODO: Make boss battles harder per iteration
        self.min_spawn_time = 0.7

    def on_show(self):
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/minigame_bgm.mp3'))
        pygame.mixer.music.play(-1)

        self.dormant_circles.clear()
        self.active_circles.clear()

        num_rings = 15
        while len(self.dormant_circles) < num_rings:
            new_ring = Ring(random.randrange(self.game.WIDTH - 128), random.randrange(self.game.HEIGHT - 128),
                            self.game.assets["circle"], self.game)
            if not self.dormant_circles:
                self.dormant_circles.append(new_ring)
            else:
                collided = False
                for neighbor in self.dormant_circles:
                    new_x, new_y = new_ring.center()
                    neighbor_x, neighbor_y = neighbor.center()
                    distance = sqrt(((new_x - neighbor_x) ** 2) + ((new_y - neighbor_y) ** 2))
                    if distance < new_ring.radius * 2:
                        collided = True
                if not collided:
                    self.dormant_circles.append(new_ring)

        self.counting_down = True
        self.counter = 7
        self.counter_str = str(self.counter)
        self.start_ticks = pygame.time.get_ticks()
        self.ring_ticks = pygame.time.get_ticks()

    def update(self):
        if self.counting_down:
            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            if seconds >= 1 and self.counter > 0:
                self.counter -= 1
                if self.counter > 0:
                    self.counter_str = str(self.counter)
                    self.start_ticks = pygame.time.get_ticks()
            elif self.counter == 0:
                self.counting_down = False

        else:
            if self.dormant_circles:
                seconds = (pygame.time.get_ticks() - self.ring_ticks) / 1000
                if seconds >= random.uniform(self.min_spawn_time, self.max_spawn_time):
                    self.active_circles.append(self.dormant_circles.pop(0))
                    self.ring_ticks = pygame.time.get_ticks()

            for circle in self.active_circles:
                try:
                    clicked = circle.update()
                    if clicked:
                        self.active_circles.remove(circle)
                except ClickedTooLate:
                    self.game.show_main_menu_screen()

            if not self.active_circles and not self.dormant_circles:
                self.game.show_main_menu_screen()

    def render(self):
        self.game.screen.fill((251, 171, 52))
        if self.counting_down:
            self.game.draw_text('Boss battle! Get ready to click!', 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 80)
            self.game.draw_text(self.counter_str, 80, self.game.WIDTH / 2, self.game.HEIGHT / 2)
            return
        else:
            for circle in self.active_circles:
                circle.render()
