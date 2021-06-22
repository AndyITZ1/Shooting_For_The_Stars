import random

import pygame
from pygame.locals import *


# For now, player will be represented with red squares.
class Player(pygame.sprite.Sprite):
    def __init__(self, game, gameplayscreen):
        super().__init__()
        self.game = game
        self.gameplayscreen = gameplayscreen
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((237, 55, 55))
        self.rect = self.surf.get_rect()
        self.alive = True

        # Kinematics: Governs the physics of player movement. vec allows us to make 2D vector variables.
        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12     # TODO: Change friction value to suit game needs.
        self.pos = self.vec((20, 565))
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)

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
        if pressed_keys[K_SPACE]:
            self.jump()

        # Basic kinematics. They all change based on the acceleration from above.
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # FEATURE: Screen Warping. Player will wrap around screen borders. Can be removed with border acting as barrier.
        if self.pos.x > self.game.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.game.WIDTH

        # Check for for player death if player falls off of screen
        if self.pos.y > self.game.HEIGHT:
            self.alive = False

        # Update the player rectangle to be at the new position that was calculated above
        self.rect.midbottom = self.pos

    # Jump method first check if a player is on a platform before allowing player to jump
    def jump(self):
        hits = pygame.sprite.spritecollide(self, self.gameplayscreen.platforms, False)
        if hits:
            self.vel.y = -15    # TODO: Change jump value to suit game needs.

    # Player platform collision detection. Check if velocity is greater than 0 to prevent jump cancellation
    def update(self):
        hits = pygame.sprite.spritecollide(self, self.gameplayscreen.platforms, False)
        if self.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1   # hits[0] returns the first collision in the list


# For now, platforms will be represented with gray rectangles.
class Platform(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((211, 211, 211))
        self.rect = self.surf.get_rect(center=(random.randint(0, game.WIDTH - 10),
                                               random.randint(0, game.HEIGHT - 30)))    # center = spawn position
