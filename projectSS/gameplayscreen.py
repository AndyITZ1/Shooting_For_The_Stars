import os
import sys
import pygame.math
from projectSS.gamescreen import GameScreen
from projectSS.menus import Button
from projectSS.entities import *
from projectSS.spritesheet import *


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
        
        # Platform generation variables / constants
        # Non-constant variables here can be changed with difficulty
        self.plat_count = 7  # Total platforms on screen at once
        self.plat_width_min = 70  # Minimum platform width
        self.plat_width_max = 120  # Maximum platform width
        self.plat_min_horizontal_gap = 20  # Minimum horizontal gap between two platforms
        self.plat_min_screen_gap = 20  # Minimum horizontal gap between screen edge and platform
        self.plat_max_vertical_gap = 40  # Maximum distance above the screen a platform can spawn
        self.PLAT_MIN_VERTICAL_GAP = 10  # Minimum distance above the screen a platform can spawn
        self.PLAT_VERTICAL_OFFSET = 20  # Maximum random variation in y position for whole-screen generation
        
        # Rhythm timing variables
        self.rhy_bpm = 165              # Music BPM
        self.rhy_offset = 0.120         # Time (s) to first beat
        self.rhy_beat_divisions = 1     # Adjust divisions of beat (2, 4 = faster, 0.5, 0.25 = slower)
        self.rhy_next_beat = 0
        self.rhy_prev_beat = 0
        self.rhy_closest_beat_time = 0  # Time (s) to closest beat
        # Factor multiplied with 1/BPM to determine "how long" the beat is
        # 0.5 = on beat 50% of the time, 0.25 = on beat 25% of the time, etc.
        # Smaller values mean a shorter beat time and harder rhythm timing
        self.rhy_beat_threshold = 0.5
        self.rhy_on_beat = False
        self.rhy_start_time = 0
        
        # Keeping track of distance for score
        self.best_distance = 0
        self.progress = 0
        self.times_hit = 0
        self.goal = False
        
        # Variables for enemy generation, each 500 dist roll a 1/10 chance to generate a new enemy
        self.enemy_dist = 0
        self.rand_dist = 0
        
        # Sprite for powerup
        abs_dir = os.path.dirname(__file__)
        self.jump_boost = Spritesheet(os.path.join(abs_dir, 'assets/jumpboost_flashr.png'))
        self.invincibility = Spritesheet(os.path.join(abs_dir, 'assets/invinc_spritesheetre.png'))
        self.j_boost_frames = [self.jump_boost.get_image(0, 0, 64, 64),
                               self.jump_boost.get_image(64, 0, 64, 64)]
        self.invinc_frames = [self.invincibility.get_image(0, 0, 64, 64),
                              self.invincibility.get_image(64, 0, 64, 64)]
    
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
        self.rhy_start_time = time.time()
    
    def gen_platforms(self, whole_screen=False):
        
        for i in range(self.plat_count - len(self.platforms)):
            # Set width/position
            width = random.randrange(self.plat_width_min, self.plat_width_max)
            x = None
            
            # Generate platforms on the entire screen
            if whole_screen:
                # Space platforms equally, then add a random offset
                y = self.camera_y + i * (self.game.HEIGHT / self.plat_count) \
                    + random.randrange(-self.PLAT_VERTICAL_OFFSET, self.PLAT_VERTICAL_OFFSET)
            else:
                # Generate platforms at the top of the screen, just offscreen
                y = self.camera_y - random.randrange(self.PLAT_MIN_VERTICAL_GAP, self.plat_max_vertical_gap)
                
                # Find closest existing platform
                if len(self.platforms) > 0:
                    closest_platform = self.platforms.sprites()[0]
                    closest_dist = abs(closest_platform.rect.centery - y)
                    
                    for p in self.platforms:
                        dist = abs(p.rect.centery - y)
                        if dist < closest_dist:
                            dist = closest_dist
                            closest_platform = p
                    
                    # Check which sides of the existing platform have enough room
                    gap_left = (closest_platform.rect.left - self.plat_min_horizontal_gap) - self.plat_min_screen_gap - \
                               width
                    gap_right = (self.game.WIDTH - self.plat_min_screen_gap) - \
                                closest_platform.rect.right + self.plat_min_horizontal_gap - width
                    
                    # Generate x with minimum gap
                    if gap_left > 0:
                        x_left = self.plat_min_screen_gap + int(width / 2) + random.randrange(gap_left)
                    
                    if gap_right > 0:
                        x_right = self.game.WIDTH - self.plat_min_screen_gap - int(width / 2) - random.randrange(
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
            
            # Default random x value
            if x is None:
                x = random.randrange(self.plat_min_screen_gap + int(width / 2),
                                     self.game.WIDTH - (self.plat_min_screen_gap + int(width / 2)))
            
            # Create platform
            plat = Platform(self, width, x, y)
            
            # Random powerup spawn
            if random.randrange(100) < 15:
                p = Powerup(self, x, y - 25, 'boost')
            elif random.randrange(100) < 7:
                p = Powerup(self, x, y - 25, 'invincible')
            elif random.randrange(100) < 22:
                p = Pusher(self, x, y - 23, plat)
    
    # enemy generation algorithm 300 to 1200 spaces after 1000, maximum is lowered by 100 every 1000
    def gen_enemies(self):
        if self.progress > 1000 and len(self.enemies) < 3:
            if self.rand_dist == 0:
                self.rand_dist = random.randrange(300, max(500, 1200 - 100 * (self.progress - 1000) // 1000))
                self.enemy_dist = self.progress
            if self.progress - self.enemy_dist > self.rand_dist:
                Enemy(self,
                      random.randrange(self.game.WIDTH // 6, self.game.WIDTH // 4),  # Platform span
                      random.randrange(0, self.game.WIDTH // 2),  # Platform x
                      self.camera_y - 15)
                self.rand_dist = 0
    
    # generates the goal if the progress bar is filled
    def gen_goal(self):
        # Add goal
        self.goal = True
        goal_platform = Platform(self, self.game.WIDTH, self.game.WIDTH / 2, self.camera_y - 500)
        goal_platform.surf.fill((255, 215, 0))
    
    # Update beat variables
    def update_beat(self):
        # Current time
        cur_time = time.time() - (self.rhy_start_time + self.rhy_offset)
        
        # Get time between beats
        beat_time = 60 / (self.rhy_bpm * self.rhy_beat_divisions)
        
        # Get previous and next beat times
        self.rhy_prev_beat = int(cur_time / beat_time) * beat_time
        self.rhy_next_beat = int((cur_time + beat_time) / beat_time) * beat_time
        
        # Get time to closest beat
        prev_beat_time = cur_time - self.rhy_prev_beat
        next_beat_time = self.rhy_next_beat - cur_time
        self.rhy_closest_beat_time = prev_beat_time if prev_beat_time < next_beat_time else next_beat_time
        
        # On beat?
        self.rhy_on_beat = self.rhy_closest_beat_time <= beat_time * (self.rhy_beat_threshold / 2)
    
    # All game logic and their changes go in this method
    def update(self):
        self.update_buttons()
        self.update_beat()
        self.entities.update()
        self.player.update()
        
        # Check if player has hit an enemy, lowering progress by 1500
        if self.player.hit:
            self.player.hit = False
            self.times_hit += 1
            self.progress = self.best_distance - 1500 * self.times_hit
            self.rand_dist = 0
        
        # Check if the player has died
        if not self.player.alive or self.progress < 0:
            self.game.show_game_over_screen()
        
        # allows for screen to scroll up and destroy
        if self.player.rect_render.top <= self.game.HEIGHT / 4:
            self.camera_y = self.player.rect.top - self.game.HEIGHT / 4
            self.despawn_y = self.camera_y + self.game.HEIGHT + 32
        
        # Tracking player distance/progress, adjusted to start point
        if self.player.pos.y + 64 < -self.best_distance:
            self.best_distance = -(self.player.pos.y + 64)
            self.progress = -(self.player.pos.y + 64) - 1500 * self.times_hit
        
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
        self.game.draw_text(str(round(self.progress)), 30, self.game.WIDTH / 2, 50)
    
    def draw_progress(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), (self.game.WIDTH / 3, 10, self.game.WIDTH / 3, 20), 3, 5, 5, 5, 5)
        pygame.draw.rect(self.game.screen, (76, 187, 23), (self.game.WIDTH / 3 + 2, 12,
                                                           min(self.game.WIDTH / 3 * (self.progress / 10000),
                                                               self.game.WIDTH / 3 - 2), 16), 0, 5, 5, 5, 5)
    
    def update_buttons(self):
        for btn in self.buttons:
            btn.update()
    
    def render_buttons(self):
        for btn in self.buttons:
            btn.render()
