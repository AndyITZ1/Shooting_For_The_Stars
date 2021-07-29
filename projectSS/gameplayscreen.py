import os
import pygame.math
from projectSS.gamescreen import GameScreen
from projectSS.menus import Button
from projectSS.entities import *
from projectSS.spritesheet import *


class GameplayScreen(GameScreen):
    """
    The main gameplay screen class that manages the rhythm-based 2D vertical game. Implements GameScreen interface:

    * Super().__init__(game) will bind the Game object to variable self.game.
    * on_show() will initialize/reinitialize the GameplayScreen when Game switches to this screen.
    * update() will process the GameplayScreen's logic.
    * render() will draw all assets in their current state to the screen.
    """

    def __init__(self, game):

        super().__init__(game)  # Binds the Game object to variable self.game.

        # --------------- Clickable UI Buttons --------------- #

        self.btn_settings = Button(8, 8,
                                   self.game.assets["btn_settings"], self.game.assets["btn_settings_light"],
                                   self.game.show_settings_screen, self.game)
        self.btn_quit = Button(self.game.WIDTH - 40, 8,
                               self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                               self.game.show_main_menu_screen, self.game)
        self.buttons = []
        self.buttons.append(self.btn_quit)
        self.buttons.append(self.btn_settings)

        # --------------- Entities Lists --------------- #

        # These lists allow for easy sprite access.
        self.entities = pygame.sprite.Group()  # Master list, since all inherit from Entities class.
        self.platforms = pygame.sprite.Group()  # Used in player update() method.
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pushers = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()

        self.boss_spawned = False
        self.boss_platform_space = 0

        self.camera_y = 0
        # Despawn point for entities. Anything below this y-limit gets destroyed.
        self.despawn_y = 0

        # Creation of player character.
        self.player = Player(self)

        # --------------- Platform Generation Variables and Constants --------------- #

        # Non-constant variables here can be changed with difficulty
        self.plat_count = 7  # Total platforms on screen at once
        self.plat_width_min = 70  # Minimum platform width
        self.plat_width_max = 120  # Maximum platform width
        self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
        self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn
        self.PLAT_MIN_SCREEN_GAP = 20  # Minimum horizontal gap between screen edge and platform
        self.PLAT_MIN_VERTICAL_GAP = 10  # Minimum distance above the screen a platform can spawn
        self.PLAT_VERTICAL_OFFSET = 20  # Maximum random variation in y position for whole-screen generation

        # --------------- Rhythm-Based Mechanic --------------- #

        # Music file
        self.music_file = 'assets/retrofunk.mp3'

        # Rhythm timing variables
        self.rhy_bpm = 165  # Music BPM
        self.rhy_offset = 0.120  # Time (s) to first beat
        self.rhy_beat_divisions = 1  # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)
        self.rhy_next_beat = 0
        self.rhy_prev_beat = 0
        self.rhy_closest_beat_time = 0  # Time (s) to closest beat
        # Factor multiplied with 1/BPM to determine "how long" the beat is
        # 0.5 = on beat 50% of the time, 0.25 = on beat 25% of the time, etc.
        # Smaller values mean a shorter beat time and harder rhythm timing
        self.rhy_beat_threshold = 0.5
        self.rhy_on_beat = False
        self.rhy_start_time = 0

        # --------------- Distance and Score --------------- #

        # Current level
        self.level = 0
        # Highest level
        self.highest_level = self.game.user_data[0]
        self.high_score = self.game.user_data[1]
        self.distance_requirement = 10000
        self.endless = False

        # Keeping track of distance for score
        self.best_distance = 0
        self.progress = 0
        self.times_hit = 0
        self.goal = False

        # Variables for enemy generation, each 500 dist roll a 1/10 chance to generate a new enemy
        self.enemy_dist = 0
        self.rand_dist = 0

        # Enemy and powerup generation chances
        self.enm_spawn_dist = 1000  # Start spawning at this height
        self.enm_min_dist = 300  # Lowest random gap between enemies
        self.enm_max_dist = 500  # Lower limit to highest random gap between enemies
        self.enm_max_dist_start = 1200  # Initial value to highest random gap
        self.enm_hit_penalty = 1500  # Amount to lower progress by when hit
        self.enm_pusher_chance = 15

        self.pwr_shield_chance = 7
        self.pwr_jump_chance = 7

        # --------------- Level appearance ------------------ #
        
        self.plat_color = (255, 128, 0)


        # --------------- Powerup Sprites --------------- #

        abs_dir = os.path.dirname(__file__)
        self.jump_boost = Spritesheet(os.path.join(abs_dir, 'assets/jumpboost_flashr.png'))
        self.invincibility = Spritesheet(os.path.join(abs_dir, 'assets/invinc_spritesheetre.png'))
        self.j_boost_frames = [self.jump_boost.get_image(0, 0, 64, 64),
                               self.jump_boost.get_image(64, 0, 64, 64)]
        self.invinc_frames = [self.invincibility.get_image(0, 0, 64, 64),
                              self.invincibility.get_image(64, 0, 64, 64)]

        # --------------- Pusher Sprite ----------------- #

        self.pusher_sprite = Spritesheet(os.path.join(abs_dir, 'assets/pusherspritesheetr.png'))
        self.pusher_walk_frames_l = [self.pusher_sprite.get_image(0, 0, 60, 66),
                                     self.pusher_sprite.get_image(0, 66, 60, 66)]
        self.pusher_walk_frames_r = [self.pusher_sprite.get_image(60, 0, 60, 66),
                                     self.pusher_sprite.get_image(60, 66, 60, 66)]
        self.pusher_thrust = [self.pusher_sprite.get_image(0, 132, 60, 66),
                              self.pusher_sprite.get_image(60, 132, 60, 66)]

        # --------------- Pause Screen ------------------ #

        self.paused = False
        self.pause_key_pressed = False
        self.trans_screen = pygame.Surface((self.game.WIDTH, self.game.HEIGHT)).convert_alpha()
        self.trans_screen.fill((0, 0, 0, 50))

        # --------------- Debug Variables --------------- #

        # TODO Disable this for production release
        self.enable_debug = False  # Change to False for production release to disable debug mode
        self.debug = False
        self.debug_key_pressed = False
        self.debug_platform = None

    def set_level_variables(self):
        """
        Sets up the gameplay variables for different levels.
        """

        if self.level == 0:
            self.distance_requirement = 8000
            self.endless = False
            
            # Appearance
            self.plat_color = (255, 128, 0)

            # Music / Rhythm
            self.music_file = 'assets/BlipStream.mp3'
            self.rhy_bpm = 150
            self.rhy_offset = 0.24  # Time (s) to first beat
            self.rhy_beat_divisions = 0.5  # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)

            # Platform generation
            self.plat_count = 8  # Total platforms on screen at once
            self.plat_width_min = 90  # Minimum platform width
            self.plat_width_max = 130  # Maximum platform width
            self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
            self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn

            # Enemies / Powerups
            self.enm_spawn_dist = 1000
            self.enm_min_dist = 600
            self.enm_max_dist = 800
            self.enm_max_dist_start = 1200
            self.enm_hit_penalty = 1000
            self.enm_pusher_chance = 0

            self.pwr_shield_chance = 7
            self.pwr_jump_chance = 7

        elif self.level == 1:
            self.distance_requirement = 9000
            self.endless = False
            
            # Appearance
            self.plat_color = (255, 128, 0)

            # Music / Rhythm
            self.music_file = 'assets/8bitmusic.mp3'
            self.rhy_bpm = 97
            self.rhy_offset = 0.132  # Time (s) to first beat
            self.rhy_beat_divisions = 1  # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)

            # Platform generation
            self.plat_count = 7  # Total platforms on screen at once
            self.plat_width_min = 70  # Minimum platform width
            self.plat_width_max = 120  # Maximum platform width
            self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
            self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn

            # Enemies / Powerups
            self.enm_spawn_dist = 1000
            self.enm_min_dist = 600
            self.enm_max_dist = 800
            self.enm_max_dist_start = 1200
            self.enm_hit_penalty = 1250
            self.enm_pusher_chance = 7

            self.pwr_shield_chance = 7
            self.pwr_jump_chance = 7

        elif self.level == 2:
            self.distance_requirement = 10000
            self.endless = False
            
            # Appearance
            self.plat_color = (255, 128, 0)

            # Music / Rhythm
            self.music_file = 'assets/retrofunk.mp3'
            self.rhy_bpm = 165
            self.rhy_offset = 0.120  # Time (s) to first beat
            self.rhy_beat_divisions = 1  # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)

            # Platform generation
            self.plat_count = 6  # Total platforms on screen at once
            self.plat_width_min = 70  # Minimum platform width
            self.plat_width_max = 120  # Maximum platform width
            self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
            self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn

            # Enemies / Powerups
            self.enm_spawn_dist = 1000
            self.enm_min_dist = 300
            self.enm_max_dist = 500
            self.enm_max_dist_start = 1200
            self.enm_hit_penalty = 1500
            self.enm_pusher_chance = 15

            self.pwr_shield_chance = 7
            self.pwr_jump_chance = 7
        else:
            self.distance_requirement = float('inf')
            self.endless = True

            # Music / Rhythm
            self.music_file = 'assets/retrofunk.mp3'
            self.rhy_bpm = 165
            self.rhy_offset = 0.120  # Time (s) to first beat
            self.rhy_beat_divisions = 1  # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)

            # Platform generation
            self.plat_count = 6  # Total platforms on screen at once
            self.plat_width_min = 70  # Minimum platform width
            self.plat_width_max = 120  # Maximum platform width
            self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
            self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn

            # Enemies / Powerups
            self.enm_spawn_dist = 1000
            self.enm_min_dist = 400
            self.enm_max_dist = 900
            self.enm_max_dist_start = 1200
            self.enm_hit_penalty = 2000
            self.enm_pusher_chance = 15

            self.pwr_shield_chance = 7
            self.pwr_jump_chance = 7

    def on_show(self):
        """
        This method initializes/re-initializes the GameplayScreen object's variables. This is done when the next screen
        in Game is GameplayScreen.
        """

        # Reset variables.
        self.camera_y = -self.game.HEIGHT + 10
        self.despawn_y = self.camera_y + self.game.HEIGHT + 32
        self.best_distance = 0
        self.enemy_dist = 0
        self.times_hit = 0
        self.goal = False
        self.progress = 0
        self.rand_dist = 0
        self.paused = False
        self.boss_spawned = False
        self.boss_platform_space = 0

        # Set up variables for individual levels
        self.set_level_variables()

        # Reset player character.
        self.player.reset()

        # Kill all entities that may have been left over from previous game.
        for e in self.entities:
            e.kill()

        # Add base platform.
        base_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, 0, (255, 0, 0))
        self.debug_platform = None

        # Call the platform generator method to add additional platforms above the base platform.
        self.gen_platforms(True)

        # Reset the background music and start the rhythm mechanic timer.
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), self.music_file))
        pygame.mixer.music.play(-1)
        self.rhy_start_time = time.time()

    def gen_platforms(self, whole_screen=False):
        """
        This method handles all platform generation. This includes creating the first initial platforms and the later
        dynamically created platforms. Also handles the random generation of powerups and the pusher entity.

        :param whole_screen: True indicates that the whole screen should be filled with the appropriate number of
            platforms. This is done in the on_show() method. The default False value instead indicates that platforms
            should be spawned above the screen height limit. This is done during game progression.
        """

        # For i in range number of platforms missing from required number of platforms.
        for i in range(self.plat_count - len(self.platforms)):
            # Set width/position.
            width = random.randrange(self.plat_width_min, self.plat_width_max)
            x = None

            # Generate platforms on the entire screen.
            if whole_screen:
                # Space platforms equally, then add a random offset
                y = self.camera_y + i * (self.game.HEIGHT / self.plat_count) \
                    + random.randrange(-self.PLAT_VERTICAL_OFFSET, self.PLAT_VERTICAL_OFFSET)

            # Dynamically generator platforms during gameplay.
            else:
                # Generate platforms at the top of the screen, just offscreen.
                y = self.camera_y - random.randrange(self.PLAT_MIN_VERTICAL_GAP, self.plat_max_vertical_gap)
                # If the last platform is boss-platform, add extra vertical space to next platform.
                if self.boss_platform_space != 0:
                    y += self.boss_platform_space
                    self.boss_platform_space = 0

                # Find closest existing platform
                if len(self.platforms) > 0:
                    closest_platform = self.platforms.sprites()[0]
                    closest_dist = abs(closest_platform.rect.centery - y)
                    for p in self.platforms:
                        dist = abs(p.rect.centery - y)
                        if dist < closest_dist:
                            closest_platform = p

                    # Check which sides of the existing platform have enough room
                    gap_left = (closest_platform.rect.left - self.plat_min_horizontal_gap) \
                               - self.PLAT_MIN_SCREEN_GAP - width
                    gap_right = (self.game.WIDTH - self.PLAT_MIN_SCREEN_GAP) - \
                                closest_platform.rect.right + self.plat_min_horizontal_gap - width

                    # Generate x with minimum gap
                    if gap_left > 0:
                        x_left = self.PLAT_MIN_SCREEN_GAP + int(width / 2) + random.randrange(gap_left)

                    if gap_right > 0:
                        x_right = self.game.WIDTH - self.PLAT_MIN_SCREEN_GAP - int(width / 2) - random.randrange(
                            gap_right)

                    if gap_left > 0 and gap_right > 0:
                        if random.randrange(gap_left + gap_right) < gap_left:
                            x = x_left
                        else:
                            x = x_right
                    elif gap_left > 0:
                        x = x_left
                    elif gap_right > 0:
                        x = x_right

            # Default random x value.
            if x is None:
                x = random.randrange(self.PLAT_MIN_SCREEN_GAP + int(width / 2),
                                     self.game.WIDTH - (self.PLAT_MIN_SCREEN_GAP + int(width / 2)))

            # Create platform with the calculated x and y values.
            # If we haven't spawned a boss for this level and we are at half progress, spawn boss-platform
            if not self.boss_spawned and self.progress >= self.distance_requirement / 2:
                plat = Platform(self, self.game.WIDTH - 200, self.game.WIDTH / 2, y, self.plat_color)
                Boss(self, plat.pos.x, y - 52, plat)
                self.boss_platform_space = -100
                self.boss_spawned = True
                continue
            else:
                plat = Platform(self, width, x, y, self.plat_color)

            # --------------- Powerups and Pusher Spawning --------------- #

            if random.randrange(100) < self.pwr_jump_chance:
                Powerup(self, x, y - 25, 'boost')
            elif random.randrange(100) < self.pwr_shield_chance:
                Powerup(self, x, y - 25, 'invincible')
            elif random.randrange(100) < self.enm_pusher_chance:
                Pusher(self, x, y - 36, plat)

    def gen_enemies(self):
        """
        This method handles the enemy generation using a custom algorithm. Enemy generation increases when player
        reaches higher level progression.
        """

        # enemy generation algorithm 300 to 1200 spaces after 1000, maximum is lowered by 100 every 1000
        if self.progress > self.enm_spawn_dist and len(self.enemies) < 3:
            if self.rand_dist == 0:
                self.rand_dist = random.randrange(self.enm_min_dist, max(self.enm_max_dist,
                                                                         self.enm_max_dist_start - 100 * (
                                                                                 self.progress - 1000) // 1000))
                self.enemy_dist = self.progress
            if self.progress - self.enemy_dist > self.rand_dist:
                Enemy(self,
                      random.randrange(self.game.WIDTH // 6, self.game.WIDTH // 4),  # Platform span
                      random.randrange(0, self.game.WIDTH // 2),  # Platform x
                      self.camera_y - 15)
                self.rand_dist = 0

    def gen_goal(self):
        """
        This method generates the goal platform once the player fills the progress bar.
        """

        self.goal = True
        goal_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, self.camera_y - 150, (255, 215, 0), True)

    def update_beat(self):
        """
        This method handles the rhythm mechanic and updating the corresponding variables based on timer.
        """

        # Current time.
        cur_time = time.time() - (self.rhy_start_time + self.rhy_offset)

        # Get time between beats.
        beat_time = 60 / (self.rhy_bpm * self.rhy_beat_divisions)

        # Get previous and next beat times.
        self.rhy_prev_beat = int(cur_time / beat_time) * beat_time
        self.rhy_next_beat = int((cur_time + beat_time) / beat_time) * beat_time

        # Get time to closest beat.
        prev_beat_time = cur_time - self.rhy_prev_beat
        next_beat_time = self.rhy_next_beat - cur_time
        self.rhy_closest_beat_time = prev_beat_time if prev_beat_time < next_beat_time else next_beat_time

        # On beat?
        self.rhy_on_beat = self.rhy_closest_beat_time <= beat_time * (self.rhy_beat_threshold / 2)

    # All game logic and their changes go in this method
    def update(self):
        """
        This method is called on each iteration of Game's update() function. This update function, in particular,
        handles the GameplayScreen's logic and updates its variables when needed.
        """

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_p] or pressed_keys[K_ESCAPE]:
            if not self.pause_key_pressed:
                self.paused = not self.paused
                self.pause_key_pressed = True
        else:
            self.pause_key_pressed = False

        self.update_buttons()  # Update all UI buttons for user interaction.
        if not self.paused:
            self.update_beat()  # Update rhythm mechanic variables.
            self.entities.update()  # Call the update method of all entities.
            self.player.update()  # Update the player character.

            # Debug mode
            if self.enable_debug:
                pressed_keys = pygame.key.get_pressed()
                # Enable / Disable debug mode
                if pressed_keys[K_i]:
                    if not self.debug_key_pressed:
                        self.debug = not self.debug
                        self.debug_key_pressed = True
                else:
                    self.debug_key_pressed = False

                # Create debug platform
                if self.debug and self.debug_platform is None:
                    self.highest_level = 3
                    self.debug_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, 0, (128, 0, 255))

                # Delete debug platform
                if not self.debug and self.debug_platform is not None:
                    self.debug_platform.kill()

                # Keep debug platform at screen edge
                if self.debug_platform is not None:
                    self.debug_platform.pos.y = self.camera_y + self.game.HEIGHT - 10
                    self.debug_platform.update_rect()

            # Check if player has hit an enemy, lowering progress by 1500.
            if self.player.hit and not self.debug:
                self.player.hit = False
                self.times_hit += 1
                self.progress = self.best_distance - self.enm_hit_penalty * self.times_hit
                self.rand_dist = 0

            # Check if the player has died.
            if not self.player.alive or self.progress < 0:
                if self.endless:
                    if self.high_score < self.best_distance:
                        self.high_score = self.best_distance
                self.game.show_game_over_screen()

            # Check if goal has been reached
            if self.player.won:
                # Increment level and show level complete screen
                self.level += 1
                if self.highest_level < self.level:
                    self.highest_level = self.level
                self.game.show_level_complete_screen()

            # allows for screen to scroll up and destroy.
            if self.player.rect_render.top <= self.game.HEIGHT / 4:
                self.camera_y = self.player.rect.top - self.game.HEIGHT / 4

                # Don't move camera too far above completion height
                self.camera_y = max(self.camera_y, -self.distance_requirement - (
                            self.enm_hit_penalty * self.times_hit) - self.game.HEIGHT - 200)

                self.despawn_y = self.camera_y + self.game.HEIGHT + 32

            # Tracking player distance/progress, adjusted to start point.
            if self.player.pos.y + 64 < -self.best_distance:
                self.best_distance = -(self.player.pos.y + 64)
                self.progress = self.best_distance - self.enm_hit_penalty * self.times_hit

            # Generate platforms and enemies.
            if self.progress < self.distance_requirement - 150:
                self.gen_platforms()
                self.gen_enemies()
            elif not self.goal:
                self.gen_goal()

    def render(self):
        """
        This method handles drawing to the screen all visual aspects of the game. Called in iteration of Game's
        game_loop() method.
        """

        # Draw background image.
        self.game.screen.blit(self.game.assets["bg_game"], (0, 0))

        # Call on all entities to draw themselves to the screen.
        for e in self.entities:
            e.render()

        # Call on player to draw itself.
        self.player.render()

        # Draw all buttons using this helper method.
        self.render_buttons()

        # Draw progress bar using this helper method.
        if self.level < 3:
            self.draw_progress()

        # Draws pause screen
        if self.paused:
            self.draw_pause_screen()

        # Draw current score
        self.game.draw_text(str(round(self.progress)), 30, self.game.WIDTH / 2, 50 if not self.endless else 20)

    def draw_progress(self):
        """
        This method draws the progress bar that fills up as the player progresses.
        """

        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.WIDTH / 3, 10, self.game.WIDTH / 3, 20), 3, 5, 5, 5, 5)
        pygame.draw.rect(self.game.screen, (76, 187, 23), (self.game.WIDTH / 3 + 2, 12,
                                                           min(self.game.WIDTH / 3 * (
                                                                   self.progress / self.distance_requirement),
                                                               self.game.WIDTH / 3 - 2), 16), 0, 5, 5, 5, 5)

    def draw_pause_screen(self):
        """
        This method draws the pause screen
        """
        self.game.screen.blit(self.trans_screen, (0, 0))
        self.game.draw_text('Paused', 30, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 40)

    def update_buttons(self):
        """
        This method invokes all buttons to update their logic.
        """

        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        """
        This method invokes all buttons to draw themselves to the screen.
        """

        for btn in self.buttons:
            btn.render()
