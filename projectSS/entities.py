import math
import time
import random
import pygame
from pygame.locals import *


# For now, player will be represented with red squares.
class Player(pygame.sprite.Sprite):
    def __init__(self, game, gameplayscreen):
        self.groups = gameplayscreen.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.gameplayscreen = gameplayscreen
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((237, 55, 55))
        self.rect = self.surf.get_rect()
        self.alive = True
        self.jumping = False

        # Kinematics: Governs the physics of player movement. vec allows us to make 2D vector variables.
        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12     # TODO: Change friction value to suit game needs.
        self.pos = self.vec((20, 565))
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.last_y = self.pos.y

        # Power-up effects
        self.boosted = False

        # Rhythm gameplay.
        self.start_time = time.time() + 0.01

    # This method allows us to control our player. Heavy use of physics and kinematics.
    def move(self):
        # Reset acceleration, or else player ends up wobbling back and forth
        self.acc = self.vec(0, 0.5)     # TODO: Change gravity (y) value to suit game needs.

        # Check if any keyboard keys have been pressed. Modify acceleration/velocity accordingly.
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.ACC

        # Basic kinematics. They all change based on the acceleration from above.
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # FEATURE: Screen Warping. Player will wrap around screen borders. Can be removed with border acting as barrier.
        if self.pos.x > self.game.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.game.WIDTH

        # Update the player rectangle to be at the new position that was calculated above
        self.rect.midbottom = self.pos

        # Check for for player death if player falls off of screen
        if self.rect.bottom > self.game.HEIGHT:
            self.alive = False

    # Jump method first check if a player is on a platform before allowing player to jump
    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.gameplayscreen.platforms, False)
        if hits and not self.jumping:
            if self.boosted:
                self.jumping = True
                self.vel.y = -30
                self.boosted = False
            else:
                # Rhythm detection
                curr_time = time.time()
                if curr_time - self.start_time <= 0.15 or curr_time - self.start_time >= (1/83)*60-0.15:
                    self.jumping = True
                    self.vel.y = -20
                    self.vel.x *= 2
                    self.game.assets["sfx_blip"].play()
                else:
                    self.jumping = True
                    self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    # Player platform collision detection & rhythm restart
    def update(self):
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
        pows_hits = pygame.sprite.spritecollide(self, self.gameplayscreen.powerups, True)
        for pow in pows_hits:
            if pow.type == 'boost':
                self.boosted = True

        # Check if player hits enemy
        hit_enemy = pygame.sprite.spritecollide(self, self.gameplayscreen.enemies, True)
        if hit_enemy:
            self.alive = False

        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, self.gameplayscreen.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if lowest.rect.bottom < hit.rect.bottom:
                        lowest = hit
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1  # hits[0] returns the first collision in the list
                    self.vel.y = 0
                    self.jumping = False
                    self.game.player_jump = False
                    self.game.player_jump_c = False

        # Tracking player height for distance traveled
        delta_y = self.pos.y - self.last_y
        self.last_y = self.pos.y
        self.gameplayscreen.total_distance -= delta_y


# For now, platforms will be represented with gray rectangles.
class Platform(pygame.sprite.Sprite):
    def __init__(self, game, gameplayscreen, width, x, y):
        self.groups = gameplayscreen.all_sprites, gameplayscreen.platforms
        super().__init__(self.groups)
        self.game = game
        self.gameplayscreen = gameplayscreen
        self.surf = pygame.Surface((width, 20))
        self.surf.fill((211, 211, 211))
        self.rect = self.surf.get_rect(center=(x, y))    # center = spawn position
        if random.randrange(100) < 15:
            p = Powerups(self.game, self, self.gameplayscreen)
            self.gameplayscreen.powerups.add(p)
            self.gameplayscreen.all_sprites.add(p)


# Representing enemies with yellow squares
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, gameplayscreen, span, x):
        self.groups = gameplayscreen.all_sprites, gameplayscreen.enemies
        super().__init__(self.groups)
        self.game = game
        self.gameplayscreen = gameplayscreen
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((211, 211, 0))
        self.rect = self.surf.get_rect()

        # Vectors for simple enemy movement
        self.vec = pygame.math.Vector2
        self.pos = self.vec((x, 30))
        self.start = self.pos
        self.span = span

    def update(self):
        # Sine wave oscillation for basic enemies, could be improved
        self.pos.x = self.start.x + math.sin(time.time() * 83/120 * 2 * math.pi) * -self.span
        self.rect.midbottom = self.pos
        if self.rect.top >= self.game.HEIGHT:
            self.kill()


class Powerups(pygame.sprite.Sprite):
    def __init__(self, game, platform, gameplayscreen):
        self.groups = gameplayscreen.all_sprites, gameplayscreen.powerups
        super().__init__(self.groups)
        self.game = game
        self.plat = platform
        self.gameplayscreen = gameplayscreen
        self.type = random.choice(['boost'])
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((200, 100, 200))
        self.rect = self.surf.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.gameplayscreen.platforms.has(self.plat):
            self.kill()

