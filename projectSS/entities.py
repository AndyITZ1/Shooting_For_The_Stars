import math
import time
import random
import pygame
from pygame.locals import *
from pygame.math import Vector2
from abc import ABC, abstractmethod


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

        # Rendering surface
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((237, 55, 55))

        # Velocity and acceleration variables
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

        self.alive = True
        self.hit = False
        self.on_ground = False
        self.jumping = False
        self.jumped = False

        # Physics constants
        # TODO: Adjust values for game balance
        self.ACCELERATION = 0.5
        self.FRICTION = 0.1
        self.AIR_FRICTION = 0.06
        self.GRAVITY = 0.5
        self.MAX_FALL_VELOCITY = 15

        # Power-up effects
        self.boosted = False

        # Rhythm gameplay.
        self.start_time = time.time() + 0.01

    # Reset player variables when starting gameplay
    def reset(self):
        self.pos.x = self.game.WIDTH / 2
        self.pos.y = -25

        self.vel.x = 0
        self.vel.y = 0

        self.acc.x = 0
        self.acc.y = 0

        self.alive = True
        self.hit = False
        self.on_ground = False
        self.jumping = False
        self.jumped = False

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
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.ACCELERATION
        elif pressed_keys[K_RIGHT]:
            self.acc.x = self.ACCELERATION

        # Player is holding space key? Jump until max jump height is reached. Space key is let go? Stop jump.
        if pressed_keys[K_SPACE]:
            self.jump()
            self.jumping = True
        else:
            self.cancel_jump()
            self.jumping = False

        # Apply friction
        if self.on_ground:
            self.acc.x -= self.vel.x * self.FRICTION
        else:
            self.acc.x -= self.vel.x * self.AIR_FRICTION

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
            else:
                # Rhythm detection
                curr_time = time.time()
                if curr_time - self.start_time <= 0.15 or curr_time - self.start_time >= (1/83)*60-0.15:
                    self.vel.y = -20
                    self.vel.x *= 2
                    self.game.assets["sfx_blip"].play()
                else:
                    self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5

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

        # Ignore collisions if the player jumped this frame
        if not self.jumped and plat_collisions:
            for p in plat_collisions:
                # Place the player on the platform if they are high enough (w/ vel forgiveness) and falling
                if self.vel.y > 0 and self.rect.bottom < p.rect.centery + self.vel.y:
                    # Set player to be slightly inside platform, otherwise they will jitter
                    self.pos.y = p.rect.top - 14.9
                    self.vel.y = 0
                    self.on_ground = True

        # If player is not colliding with a platform
        else:
            self.on_ground = False

        self.update_rect()

        if self.boosted:
            self.surf.fill((255,165,0))
        else:
            cur_time = time.time()
            # turn green within a 0.3 interval of the bpm start time
            if cur_time - self.start_time <= 0.15:
                self.surf.fill((0, 255, 0))
            elif cur_time - self.start_time >= (1/83)*60-0.15:
                self.surf.fill((0, 255, 0))
            else:
                self.surf.fill((237, 55, 55))
        # 83 BPM or 0.7229 seconds-per-beat: (1 / 83 bpm) * 60 to get exact seconds
        if (time.time() - self.start_time) > (1/83)*60:
            self.start_time = time.time()

        # Check if player hits powerups
        pows_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.powerups, True)
        for p in pows_collisions:
            if p.type == 'boost':
                self.boosted = True

        # Check if player hits enemy
        enemy_collisions = pygame.sprite.spritecollide(self, self.gameplay_screen.enemies, True)
        if enemy_collisions:
            self.game.assets["sfx_hit"].play()
            self.hit = True
            for e in enemy_collisions:
                e.kill()


# For now, platforms will be represented with gray rectangles.
class Platform(Entity):
    def __init__(self, gameplay_screen, width, x, y):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.platforms)
        self.surf = pygame.Surface((width, 20))
        self.surf.fill((211, 211, 211))
        self.pos.x = x
        self.pos.y = y

        self.update_rect()


# Representing enemies with yellow squares
class Enemy(Entity):
    def __init__(self, gameplay_screen, span, x, y):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.enemies)
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((211, 211, 0))

        # Vectors for simple enemy movement
        self.pos.x = x
        self.pos.y = y
        self.start = self.pos.x
        self.span = span

        self.update_rect()

    def update(self):
        # Sine wave oscillation for basic enemies, could be improved
        self.pos.x = self.start + (self.span * math.sin(time.time() * 83/120 * 2 * math.pi) + self.span)

        if self.pos.y > self.gameplay_screen.despawn_y:
            self.kill()

        self.update_rect()


class Powerup(Entity):
    def __init__(self, gameplay_screen, x, y):
        super().__init__(gameplay_screen, gameplay_screen.entities, gameplay_screen.powerups)
        self.type = random.choice(['boost'])
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((200, 100, 200))

        self.pos.x = x
        self.pos.y = y

        self.update_rect()
