import os
import pygame
from projectSS.gamescreen import GameScreen


class Ring:
    def __init__(self, x, y, sprite, game):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.game = game

        self.width = sprite.get_width()
        self.height = sprite.get_height()

        self.mouse_hover = False

    def update(self):
        # Update mouse over
        self.mouse_hover = (self.x <= self.game.mouse_pos[0] < self.x + self.width and
                            self.y <= self.game.mouse_pos[1] < self.y + self.height)

        # Invoke on_click if clicked
        if self.mouse_hover and self.game.mouse_clicked:
            self.game.assets["sfx_blip"].play()
            return True
        else:
            return False

    def render(self):
        self.game.screen.blit(self.sprite, (self.x, self.y))


class MinigameScreen(GameScreen):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.counting_down = True
        self.start_ticks = None  # Start tick
        self.counter = 7
        self.counter_str = str(self.counter)
        self.circles = []

    def on_show(self):
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/minigame_bgm.mp3'))
        pygame.mixer.music.play(-1)
        self.counting_down = True
        self.start_ticks = pygame.time.get_ticks()
        self.circles = [
            Ring(self.game.WIDTH / 2 - 128, self.game.HEIGHT / 2 - 128, self.game.assets["circle"], self.game)]

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
            for circle in self.circles:
                clicked = circle.update()
                if clicked:
                    self.circles.remove(circle)
            if not self.circles:
                self.game.show_previous_game_screen()

    def render(self):
        self.game.screen.fill((251, 171, 52))
        if self.counting_down:
            self.game.draw_text('Boss battle! Get ready to click!', 40, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 80)
            self.game.draw_text(self.counter_str, 80, self.game.WIDTH / 2, self.game.HEIGHT / 2)
            return
        else:
            for circle in self.circles:
                circle.render()
