import math
import time
import random
import os.path
from pygame.locals import *
from pygame.math import Vector2
from abc import ABC
from projectSS.spritesheet import *


# Abstract entity class
class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, gameplay_screen, *groups):
        super().__init__(groups)
        self.gameplay_screen = gameplay_screen
        self.game = gameplay_screen.game

        self.surf = pygame.Surface((0, 0))
        self.rect = self.surf.get_rect()
        self.rect_render = self.surf.get_rect()

        self.pos = Vector2(0, 0)
        self.last_pos = self.pos

    def update(self):
        if self.pos.y > self.gameplay_screen.despawn_y:
            self.kill()

        self.update_rect()

    def update_rect(self):
        self.rect = self.surf.get_rect(center=self.pos)
        self.rect_render = self.surf.get_rect(
            center=(self.pos.x, self.pos.y - self.gameplay_screen.camera_y))

    def render(self):
        self.game.screen.blit(self.surf, self.rect_render)


# For now, player will be represented with red squares.
class Player(Entity):
    def __init__(self, gameplay_screen):
        super().__init__(gameplay_screen)

        # This can be refactor if needed, but uses the Spritesheet class to load and pick out images
        abs_dir = os.path.dirname(__file__)
        self.player_spritesheet = Spritesheet(os.path.join(abs_dir, 'assets/player_spritesheet.png'))
        # Variables for animation/switching of sprites
        self.play_walk = False
        self.play_jump = False
        self.current_frame = 0
        self.last_update = 0
        # Variable to detect what was the last direction the player moved (Either left or right) F = left, T = right
        self.last_direction = False
        # To reduce clutter in init all frames images are put in load_images()
        self.load_images()
        # surf used to be the rectangle/square player and now is changed to hold the first frame of idle sprite
        # surf variable will be changed often for each different frame of animation
        self.surf = self.idle_walk_frames_r[0]

        # Rendering surface
        # self.surf = pygame.Surface((30, 30))
        # self.surf.fill((237, 55, 55))

        # Velocity and acceleration variables
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.alive = True
        self.won = False
        self.hit = False
        self.on_ground = False
        self.jumping = False
        self.jumped = False
        self.pushed = False
        self.push_time = 0

        # Physics constants
        self.ACCELERATION = 0.5
        self.FRICTION = 0.1
        self.AIR_FRICTION = 0.06
        self.GRAVITY = 0.5
        self.MAX_FALL_VELOCITY = 15

        # Power-up effects
        self.boosted = False
        self.immune = False

    def load_images(self):
        self.idle_walk_frames_l = [self.player_spritesheet.get_image(3, 3, 58, 58),
                                   self.player_spritesheet.get_image(2, 136, 56, 60)]
        self.idle_walk_frames_r = [self.player_spritesheet.get_image(137, 3, 58, 58),
                                   self.player_spritesheet.get_image(140, 136, 56, 60)]
        self.jump_frames = [self.player_spritesheet.get_image(2, 70, 64, 60),
                            self.player_spritesheet.get_image(134, 70, 64, 60)]
        # IL, IR, WL, WR, JL, JR
        self.rhythm_jump_frames = [self.player_spritesheet.get_image(68, 3, 58, 58),
                                   self.player_spritesheet.get_image(204, 3, 58, 58),
                                   self.player_spritesheet.get_image(67, 136, 56, 60),
                                   self.player_spritesheet.get_image(207, 136, 56, 60),
                                   self.player_spritesheet.get_image(66, 69, 64, 60),
                                   self.player_spritesheet.get_image(200, 70, 64, 60)]
        self.player_boost_frames = [self.player_spritesheet.get_image(0, 198, 66, 66),
                                    self.player_spritesheet.get_image(66, 198, 66, 66)]
        self.invinc_idle_walk_frames_l = [self.player_spritesheet.get_image(0, 264, 66, 66),
                                          self.player_spritesheet.get_image(130, 198, 66, 66)]
        self.invinc_idle_walk_frames_r = [self.player_spritesheet.get_image(66, 264, 66, 66),
                                          self.player_spritesheet.get_image(196, 198, 66, 66)]
        self.invinc_jump_frames = [self.player_spritesheet.get_image(130, 264, 66, 66),
                                   self.player_spritesheet.get_image(196, 264, 66, 66)]
        # IL, WL, IR, WR, JL, JR
        self.invinc_rhythm_frames = [self.player_spritesheet.get_image(0, 396, 66, 66),
                                     self.player_spritesheet.get_image(130, 330, 66, 66),
                                     self.player_spritesheet.get_image(66, 396, 66, 66),
                                     self.player_spritesheet.get_image(196, 330, 66, 66),
                                     self.player_spritesheet.get_image(130, 396, 66, 66),
                                     self.player_spritesheet.get_image(196, 396, 66, 66)]

    # Reset player variables when starting gameplay
    def reset(self):
        self.pos.x = self.game.WIDTH / 2
        self.pos.y = -64

        self.vel.x = 0
        self.vel.y = 0

        self.acc.x = 0
        self.acc.y = 0

        self.alive = True
        self.won = False
        self.hit = False
        self.on_ground = False
        self.jumping = False
        self.jumped = False
        self.immune = False
        self.boosted = False
        self.pushed = False
        self.push_time = 0

    # This method allows us to control our player. Heavy use of physics and kinematics.
    def move(self):
        # Reset acceleration, or else player ends up wobbling back and forth
        self.acc.x = 0
        self.acc.y = 0

        # Apply gravity if player is not on a platform
        if not self.on_ground:
            self.acc.y = self.GRAVITY

        # Check if any keyboard keys have been pressed. Modify acceleration/velocity accordingly.
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.last_direction = False
            self.play_walk = True
            self.acc.x = -self.ACCELERATION
        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.last_direction = True
            self.play_walk = True
            self.acc.x = self.ACCELERATION

        # Player is holding space key? Jump until max jump height is reached. Space key is let go? Stop jump.
        if pressed_keys[K_SPACE] or pressed_keys[K_UP] or pressed_keys[K_w]:
            self.jump()
            self.jumping = True
            self.play_jump = True
        else:
            self.cancel_jump()
            self.jumping = False
            self.play_jump = False

        # Apply friction
        if self.on_ground:
            self.acc.x -= self.vel.x * self.FRICTION
        else:
            self.acc.x -= self.vel.x * self.AIR_FRICTION

        # See if player was pushed
        if self.pushed:
            self.push()
            self.pushed = False

        # Basic kinematics. They all change based on the acceleration from above.
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Apply maximum falling velocity
        if self.vel.y > self.MAX_FALL_VELOCITY:
            self.vel.y = self.MAX_FALL_VELOCITY

        # Screen Warping. Player will wrap around screen borders. Can be removed with border acting as barrier.
        if self.pos.x > self.game.WIDTH:
            self.pos.x = self.pos.x - self.game.WIDTH
        if self.pos.x < 0:
            self.pos.x = self.game.WIDTH - self.pos.x

    # Jump method first check if a player is on a platform before allowing player to jump
    def jump(self):
        if self.on_ground and not self.jumping:
            self.jumped = True

            if self.boosted:
                self.vel.y = -30
                self.boosted = False
                self.game.assets["sfx_boostjump"].play()
            else:
                # On beat jump
                if self.gameplay_screen.rhy_on_beat:
                    self.vel.y = -20
                    self.vel.x *= 2
                    self.game.assets["sfx_blip"].play()
                    if self.last_direction:
                        if self.immune:
                            self.surf = self.invinc_rhythm_frames[5]
                        else:
                            self.surf = self.rhythm_jump_frames[5]
                    else:
                        if self.immune:
                            self.surf = self.invinc_rhythm_frames[4]
                        else:
                            self.surf = self.rhythm_jump_frames[4]


                # Off beat jump
                else:
                    self.vel.y = -15
                    self.game.assets["sfx_jump"].play()
                    if self.last_direction:
                        if self.immune:
                            self.surf = self.invinc_jump_frames[1]
                        else:
                            self.surf = self.jump_frames[1]
                    else:
                        if self.immune:
                            self.surf = self.invinc_jump_frames[0]
                        else:
                            self.surf = self.jump_frames[0]

    def push(self):
        self.vel.y = random.randrange(-15, -5)
        self.acc.x = random.randrange(-15, 15)

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5

    def animate_walk(self, direction_frames):
        now = pygame.time.get_ticks()
        if self.play_walk:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(direction_frames)
                self.surf = direction_frames[self.current_frame]

    def animate(self, left_frames, right_frames):
        if not self.play_walk and not self.play_jump:
            if self.last_direction:
                self.surf = right_frames[0]
            else:
                self.surf = left_frames[0]
        elif self.play_walk:
            if self.last_direction:
                self.animate_walk(right_frames)
            else:
                self.animate_walk(left_frames)

    def rhythm_jump_animate(self):
        if not self.play_walk and not self.play_jump:
            if self.last_direction:
                if self.immune:
                    self.surf = self.invinc_rhythm_frames[2]
                else:
                    self.surf = self.rhythm_jump_frames[1]
            else:
                if self.immune:
                    self.surf = self.invinc_rhythm_frames[0]
                else:
                    self.surf = self.rhythm_jump_frames[0]
        elif self.play_walk:
            if self.last_direction:
                if self.immune:
                    self.surf = self.invinc_rhythm_frames[3]
                else:
                    self.surf = self.rhythm_jump_frames[3]
            else:
                if self.immune:
                    self.surf = self.invinc_rhythm_frames[1]
                else:
                    self.surf = self.rhythm_jump_frames[2]

    # Player platform collision detection & rhythm restart
    def update(self):
        self.jumped = False

        # Update movement
        self.move()

        # Check for for player death if player falls off of screen
        if self.pos.y > self.gameplay_screen.despawn_y:
            self.alive = False
            return

        # Platform collisions
        plat_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.platforms, False)
        self.on_ground = False
        
        # Ignore collisions if the player jumped this frame
        if not self.jumped and plat_collisions:
            for p in plat_collisions:
                # Place the player on the platform if they are high enough (w/ vel forgiveness) and falling
                if self.vel.y >= 0 and self.rect.bottom < p.rect.centery + self.vel.y:
                    # Set player to be slightly inside platform, otherwise they will jitter
                    self.pos.y = p.rect.top - ((self.rect.height / 2) - 0.1)
                    self.vel.y = 0
                    self.on_ground = True
                    
                    # Set win if goal platform
                    if p.goal:
                        self.won = True

        self.update_rect()

        if self.boosted:
            if self.last_direction:
                self.surf = self.player_boost_frames[1]
            else:
                self.surf = self.player_boost_frames[0]
        else:
            cur_time = time.time()
            # changes to rhythm jump animation when on beat
            if self.gameplay_screen.rhy_on_beat:
                self.rhythm_jump_animate()
            else:
                if self.immune:
                    self.animate(self.invinc_idle_walk_frames_l, self.invinc_idle_walk_frames_r)
                else:
                    self.animate(self.idle_walk_frames_l, self.idle_walk_frames_r)

        # Check if player hits powerups
        pows_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.powerups, True)
        for p in pows_collisions:
            self.game.assets["sfx_pickup"].play()
            if p.type == 'boost':
                self.boosted = True
            elif p.type == 'invincible':
                self.immune = True

        # Check if player hits enemy
        enemy_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.enemies, True)
        if enemy_collisions:
            # If player is in IMMUNE STATE, will lose immunity after hitting 1 enemy
            if self.immune:
                self.game.assets["sfx_loseshield"].play()
                self.immune = False
            else:
                self.game.assets["sfx_hit"].play()
                self.hit = True
                for e in enemy_collisions:
                    e.kill()

        # Check if player hits a pusher
        push_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.pushers, False)
        for p in push_collisions:
            # If player is in IMMUNE STATE, will lose immunity after hitting 1 enemy
            if self.immune and time.time() - self.push_time > 1.0:
                self.game.assets["sfx_loseshield"].play()
                self.push_time = time.time()
                self.immune = False
            if p.active and time.time() - self.push_time > 1.0:
                self.game.assets["sfx_pushed"].play()
                self.push_time = time.time()
                self.pushed = True

        # Walking to Idle Animation transition
        if self.last_pos.x + 0.005 >= self.pos.x >= self.last_pos.x - 0.005 and self.on_ground:
            self.play_walk = False

        # Check if player hits a boss
        boss_collision = pygame.sprite.spritecollide(self, self.gameplay_screen.bosses, True)
        if boss_collision:
            # Stop music and let SFX play for its duration before switching to minigame.
            pygame.mixer.music.stop()
            self.game.assets["sfx_boss"].play()
            while pygame.mixer.get_busy():
                continue

            # Set player's position to boss's
            self.pos = boss_collision[0].pos

            # Stop player movement, or else character moves in same direction as it was before boss collision.
            self.vel.x = 0
            self.vel.y = 0

            # Switch to minigame.
            self.game.show_minigame_screen()


# For now, platforms will be represented with gray rectangles.
class Platform(Entity):
    def __init__(self, gameplay_screen, width, x, y, color, goal=False):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.platforms)
        self.surf = pygame.Surface((width, 20))
        self.surf.fill(color)
        
        self.surf_inner = pygame.Surface((width - 8, 12))
        self.surf_inner.fill((32, 32, 32))
        self.rect_render_inner = None
        
        self.pos.x = x
        self.pos.y = y
        self.goal = goal

        self.update_rect()
    
    def update_rect(self):
        super().update_rect()
        self.rect_render_inner = self.surf_inner.get_rect(
            center=(self.pos.x, self.pos.y - self.gameplay_screen.camera_y))
    
    def render(self):
        super().render()
        self.game.screen.blit(self.surf_inner, self.rect_render_inner)


class Enemy(Entity):
    def __init__(self, gameplay_screen, span, x, y):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.enemies)
        self.surf = pygame.transform.scale(self.game.assets["enemy_disc"].convert_alpha(), (35, 35))
        # self.surf.fill((211, 211, 0))

        # Vectors for simple enemy movement
        self.pos.x = x
        self.pos.y = y
        self.start = self.pos.x
        self.span = span

        self.update_rect()

    def update(self):
        # Sine wave oscillation for basic enemies, could be improved
        self.pos.x = self.start + (self.span * math.sin(time.time() *
                                  (self.gameplay_screen.rhy_bpm * self.gameplay_screen.rhy_beat_divisions)/120 * math.pi) + self.span)

        if self.pos.y > self.gameplay_screen.despawn_y:
            self.kill()

        self.update_rect()


class Powerup(Entity):
    def __init__(self, gameplay_screen, x, y, type):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.powerups)
        self.type = type
        if self.type == 'boost':
            self.power_frames = gameplay_screen.j_boost_frames
        else:
            self.power_frames = gameplay_screen.invinc_frames
        self.surf = self.power_frames[0]
        self.last_update = 0
        self.current_frame = 0

        self.pos.x = x
        self.pos.y = y - 20

        self.update_rect()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.power_frames)
            self.surf = self.power_frames[self.current_frame]
        self.update_rect()


class Pusher(Entity):
    def __init__(self, gameplay_screen, x, y, platform):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.pushers)
        self.plat = platform
        self.surf = gameplay_screen.pusher_walk_frames_l[1]
        # self.surf = pygame.Surface((25, 25))
        # self.surf.fill((80, 80, 80))
        self.pos.x = x
        self.pos.y = y
        self.active = False
        self.vel = 1
        self.last_direction = True
        self.last_update = 0
        self.current_frame = 0

        self.update_rect()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            if self.last_direction:
                self.current_frame = (self.current_frame + 1) % len(self.gameplay_screen.pusher_walk_frames_r)
                self.surf = self.gameplay_screen.pusher_walk_frames_r[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.gameplay_screen.pusher_walk_frames_l)
                self.surf = self.gameplay_screen.pusher_walk_frames_l[self.current_frame]

    def update(self):
        old_pos_x = self.pos.x
        if self.plat.pos.x - self.plat.surf.get_rect().center[0] < self.pos.x < self.plat.pos.x + self.plat.surf.get_rect().center[0]:
            self.pos.x += self.vel
        else:
            self.vel *= -1
            self.pos.x += self.vel

        if self.pos.x > old_pos_x:
            self.last_direction = True
        elif self.pos.x < old_pos_x:
            self.last_direction = False

        self.animate()

        # turn light gray when on beat
        if self.gameplay_screen.rhy_on_beat:
            if self.last_direction:
                self.surf = self.gameplay_screen.pusher_thrust[1]
            else:
                self.surf = self.gameplay_screen.pusher_thrust[0]
            self.active = True
        else:
            # self.surf.fill((30, 30, 30))
            self.active = False

        self.update_rect()


class Boss(Entity):
    def __init__(self, gameplay_screen, x, y, platform):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.bosses)
        self.plat = platform
        abs_dir = os.path.dirname(__file__)
        self.boss_sprite = Spritesheet(os.path.join(abs_dir, 'assets/boss_sprite.png'))
        self.boss_frame = self.boss_sprite.get_image(0, 0, 44, 88)
        self.surf = self.boss_frame
        # self.surf = pygame.Surface((32, 32))
        # self.surf.fill((255, 0, 0))
        self.pos.x = x
        self.pos.y = y
        self.update_rect()

    def update(self):
        self.update_rect()
