import os
import random
import time
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
        self.outer_radius_delta = -1.75  # The change over time of the outer_radius ring. Can be changed.

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
        self.difficulty = 4
        self.minigame_mode = False

        self.active_rings = []
        self.dormant_rings = []

        # ----- Ring spawn time variables. -----#

        self.max_spawn_time = None  # Indicates the longest spawn time possible.
        self.min_spawn_time = None  # Indicates the shortest spawn time possible.

    def on_show(self):
        """
        The method is is first run when game.py switches to this GameScreen. It cleans up any and resets any previous
        minigame variables.
        """
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/minigame_bgm.mp3'))
        pygame.mixer.music.play(-1)

        # If the previous minigame was played from main menu, reset the bool.
        self.minigame_mode = False

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

        # Ring spawn time variables. All of them can be changed to suite needs of the game
        if self.gameplay_screen.level == 0:
            self.difficulty = 0
            self.max_spawn_time = 1.75
            self.min_spawn_time = 0.84
        elif self.gameplay_screen.level == 1:
            self.difficulty = 1
            self.max_spawn_time = 1.50
            self.min_spawn_time = 0.68
        else:
            self.difficulty = 2
            self.max_spawn_time = 1.25
            self.min_spawn_time = 0.52

        # Set the beginning state of MinigameScreen to be in countdown mode.
        self.counting_down = True
        self.counter = 7  # 7 was chosen since the background music's beat drops after 7 seconds.
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
                    # User clicked too late. User lost!
                    if self.game.prev_game_screen == self.game.scrn_main_menu:
                        self.minigame_mode = True
                        self.punishment()
                        self.game.show_main_menu_screen()
                        return
                    else:
                        self.minigame_mode = False
                        self.punishment()
                        self.game.show_gameplay_screen()
                        return

            if not self.active_rings and not self.dormant_rings:
                # User has successfully clicked all rings in time. User won!
                if self.game.prev_game_screen == self.game.scrn_main_menu:
                    self.minigame_mode = True
                    self.reward()
                    self.game.show_main_menu_screen()
                else:
                    self.minigame_mode = False
                    self.reward()
                    self.game.show_gameplay_screen()

    def render(self):
        """
        The render method draws all minigame elements onto the screen. This includes the countdown and the rings.
        """
        self.game.screen.blit(self.game.assets["bg_minigame"], (0, 0))
        if self.counting_down:
            self.game.draw_text('Boss battle! Get ready to click!', 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 80)
            self.game.draw_text(self.counter_str, 80, self.game.WIDTH / 2, self.game.HEIGHT / 2)

            difficulty_string = "Difficulty: "
            if self.difficulty == 0:
                difficulty_string += "Easy"
            elif self.difficulty == 1:
                difficulty_string += "Medium"
            else:
                difficulty_string += "Hard"

            self.game.draw_text(difficulty_string, 30, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 80)
        else:
            for ring in self.active_rings:
                ring.render()

    def reward(self):
        pygame.mixer.music.stop()

        self.game.screen.blit(self.game.assets["bg_minigame"], (0, 0))
        self.game.draw_text("Success!", 60, self.game.WIDTH / 2, self.game.HEIGHT / 2)

        if self.game.prev_game_screen != self.game.scrn_main_menu:
            self.game.draw_text("You will now be granted a massive", 50, self.game.WIDTH / 2,
                                self.game.HEIGHT / 2 + 80)
            self.game.draw_text("boost with invincibility!", 50, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 150)

            self.gameplay_screen.player.immune = True
            self.gameplay_screen.player.vel.y = -50

        pygame.display.update()

        self.game.assets["sfx_boss_win"].play()
        while pygame.mixer.get_busy():
            continue

        if self.game.prev_game_screen != self.game.scrn_main_menu:
            self.game.assets["sfx_boostjump"].play()

    def punishment(self):
        pygame.mixer.music.stop()

        self.game.screen.blit(self.game.assets["bg_minigame"], (0, 0))
        self.game.draw_text("Better luck next time!", 60, self.game.WIDTH / 2, self.game.HEIGHT / 2)

        if self.game.prev_game_screen != self.game.scrn_main_menu:
            self.game.draw_text("Your progress will now be", 40, self.game.WIDTH / 2,
                                self.game.HEIGHT / 2 + 80)
            self.game.draw_text("decreased substantially!", 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 120)

            self.gameplay_screen.times_hit += 2
            self.gameplay_screen.progress = self.gameplay_screen.best_distance - \
                self.gameplay_screen.enm_hit_penalty * self.gameplay_screen.times_hit
            self.gameplay_screen.rand_dist = 0

        pygame.display.update()

        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/gameover_bgm.mp3'))
        pygame.mixer.music.play(-1)
        time.sleep(3.5)
        pygame.mixer.music.stop()
