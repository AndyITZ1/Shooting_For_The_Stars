import os
import pygame
from projectSS.gamescreen import GameScreen


class MinigameScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.counting_down = True
        self.start_ticks = None   # Start tick
        self.counter = 7
        self.counter_str = str(self.counter)

    def on_show(self):
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/minigame_bgm.mp3'))
        pygame.mixer.music.play(-1)
        self.counting_down = True
        self.start_ticks = pygame.time.get_ticks()  # Start tick

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

    def render(self):
        self.game.screen.fill((251, 171, 52))
        if self.counting_down:
            self.game.draw_text('Boss battle! Get ready to click!', 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 80)
            self.game.draw_text(self.counter_str, 80, self.game.WIDTH / 2, self.game.HEIGHT / 2)
