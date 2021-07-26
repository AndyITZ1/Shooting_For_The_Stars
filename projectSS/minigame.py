import os
import random
from math import sqrt
import pygame
from projectSS.gamescreen import GameScreen


class ClickedTooLate(Exception):
    """
    A custom-made exception used if the player did not click on the minigame rings in time.
    """
    def __init__(self, message="Didn't click the minigame button in time"):
        self.message = message


class Ring(pygame.sprite.Sprite):
    """
    The class that represents the ring objects that appear in the minigame.
    """
    def __init__(self, x, y, sprite, game):
        super().__init__()
        self.x = x
        self.y = y
        self.sprite = sprite
        self.game = game

        self.width = sprite.get_width()
        self.height = sprite.get_height()
        self.inner_radius = self.width / 2  # Inner sprite radius. Used in collision detection
        self.outer_radius = 200  # Outer ring. Decreases in size during gameplay. Can be changed.
        self.outer_radius_delta = -1.75     # The change over time of the outer_radius ring. Can be changed.

        self.mouse_hover = False  # Boolean used in mouse detection.

    def update(self):
        """
        The individual ring update method. Handles user interaction, outer ring size, and clicking timing.
        """
        # Checks if mouse is hovering over the sprite using the sprite's position and size.
        self.mouse_hover = (self.x <= self.game.mouse_pos[0] < self.x + self.width and
                            self.y <= self.game.mouse_pos[1] < self.y + self.height)

        # Player is hovering over ring, has clicked on it, and the outer ring is the correct size.
        if self.mouse_hover and self.game.mouse_clicked and 52 <= self.outer_radius <= 67:
            self.game.assets["sfx_blip"].play()
            return True
        else:
            # Player has clicked on the ring too late. Exception is raised and handled in MinigameScreen.update().
            if self.outer_radius < 52:
                raise ClickedTooLate
            else:
                self.outer_radius += self.outer_radius_delta

    def render(self):
        """
        The individual ring render method. Draws the ring sprite and the outer circle.
        """
        self.game.screen.blit(self.sprite, (self.x, self.y))
        pygame.draw.circle(self.game.screen, (134, 144, 250), (self.x + 64, self.y + 64), self.outer_radius, width=3)

    def center(self):
        """
        Helper method. Calculates the ring's center coordinates. Used in MinigameScreen.on_show() in collision detect.

        :return: (ring_x, ring_y)
        """
        return self.x + self.width, self.y + self.height

    @property
    def radius(self):
        return self.inner_radius


class MinigameScreen(GameScreen):
    """
    The GameScreen that represents the ring-clicking minigame.
    """
    def __init__(self, game, gameplay_screen):
        super().__init__(game)
        self.game = game
        self.gameplay_screen = gameplay_screen

        self.counting_down = True
        self.start_ticks = None  # Countdown ticks
        self.ring_ticks = None  # Ring spawn ticks
        self.counter = 7
        self.counter_str = str(self.counter)

        self.active_rings = []
        self.dormant_rings = []

        # ----- Ring spawn time variables. All of them can be changed to suite needs of the game -----#

        self.max_spawn_time = 2.0   # Indicates the longest spawn time possible.
        self.smallest_max_time = 1.30   # Indicates the smallest value max_spawn_time can be decreased to.
        self.max_spawn_time_delta = -0.25   # Change of max_spawn_time per iteration of minigame.

        self.min_spawn_time = 1.0   # Indicates the shortest spawn time possible.
        self.smallest_min_time = 0.53   # Indicates the smallest value min_spawn_time can be decreased to.
        self.min_spawn_time_delta = -0.16   # Change of min_spawn_time per iteration of minigame.

        # --------------- Minigame Rewards/Punishments -------------- #

        self.reward = 2000
        self.punishment = -2000

    def on_show(self):
        """
        The method is is first run when game.py switches to this GameScreen. It cleans up any and resets any previous
        minigame variables.
        """
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/minigame_bgm.mp3'))
        pygame.mixer.music.play(-1)

        self.dormant_rings.clear()
        self.active_rings.clear()

        num_rings = 15  # The number of rings used in the game. CAN BE CHANGED.
        while len(self.dormant_rings) < num_rings:
            new_ring = Ring(random.randrange(self.game.WIDTH - 128), random.randrange(self.game.HEIGHT - 128),
                            self.game.assets["circle"], self.game)
            # If this is the first ring to be inserted, don't check for collisions since none exist.
            if not self.dormant_rings:
                self.dormant_rings.append(new_ring)
            else:
                # Check the distance between neighboring rings. If it is shorter than radius * 2 (diameter), the rings
                # are too close together. Discard the newly generated ring.
                collided = False
                for neighbor in self.dormant_rings:
                    new_x, new_y = new_ring.center()
                    neighbor_x, neighbor_y = neighbor.center()
                    distance = sqrt(((new_x - neighbor_x) ** 2) + ((new_y - neighbor_y) ** 2))
                    if distance < new_ring.radius * 2:
                        collided = True
                if not collided:
                    self.dormant_rings.append(new_ring)

        # Game speed change.
        if self.max_spawn_time > self.smallest_max_time:
            self.max_spawn_time += self.max_spawn_time_delta
        if self.min_spawn_time > self.smallest_min_time:
            self.min_spawn_time += self.min_spawn_time_delta

        # Set the beginning state of MinigameScreen to be in countdown mode.
        self.counting_down = True
        self.counter = 7    # 7 was chosen since the background music's beat drops after 7 seconds.
        self.counter_str = str(self.counter)
        self.start_ticks = pygame.time.get_ticks()
        self.ring_ticks = pygame.time.get_ticks()

    def update(self):
        """
        The update method controls the logic of either the game's countdown or the ring spawn times and user interaction
        """
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
            # Change rings from dormant to active based on spawn times.
            if self.dormant_rings:
                seconds = (pygame.time.get_ticks() - self.ring_ticks) / 1000
                if seconds >= random.uniform(self.min_spawn_time, self.max_spawn_time):
                    self.active_rings.append(self.dormant_rings.pop(0))
                    self.ring_ticks = pygame.time.get_ticks()

            for ring in self.active_rings:
                try:
                    clicked = ring.update()
                    if clicked:
                        self.active_rings.remove(ring)
                except ClickedTooLate:
                    # User clicked too late. Return to main menu, for now.
                    self.gameplay_screen.progress += self.punishment
                    self.game.show_gameplay_screen()

            if not self.active_rings and not self.dormant_rings:
                # User has successfully clicked all rings in time. Return to main menu, for now.
                self.gameplay_screen.progress += self.reward
                self.gameplay_screen.best_distance += self.reward
                self.game.show_gameplay_screen()

    def render(self):
        """
        The render method draws all minigame elements onto the screen. This includes the countdown and the rings.
        """
        self.game.screen.blit(self.game.assets["bg_minigame"], (0, 0))
        if self.counting_down:
            self.game.draw_text('Boss battle! Get ready to click!', 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 80)
            self.game.draw_text(self.counter_str, 80, self.game.WIDTH / 2, self.game.HEIGHT / 2)
            return
        else:
            for ring in self.active_rings:
                ring.render()
