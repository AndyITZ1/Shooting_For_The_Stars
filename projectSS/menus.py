import pygame
import os.path
import sys
from abc import ABC

from projectSS.gamescreen import GameScreen


class Button:
    def __init__(self, x, y, sprite, sprite_hover, on_click, game):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sprite_hover = sprite_hover
        self.on_click = on_click
        self.game = game

        # Set button hitbox dimensions
        self.width = sprite.get_width()
        self.height = sprite.get_height()

        # True if mouse is hovering over button
        self.mouse_hover = False

    def update(self):
        # Update mouse over
        self.mouse_hover = (self.x <= self.game.mouse_pos[0] < self.x + self.width and
                            self.y <= self.game.mouse_pos[1] < self.y + self.height)

        # Invoke on_click if clicked
        if self.mouse_hover and self.game.mouse_clicked:
            self.game.assets["sfx_blip"].play()
            self.on_click()

    def render(self):
        self.game.screen.blit(self.sprite_hover if self.mouse_hover else self.sprite, (self.x, self.y))


# menu base class for handling multiple menus
class Menu(GameScreen, ABC):
    def __init__(self, game):
        super().__init__(game)
        self.center_x, self.center_y = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.buttons = []

    def update_buttons(self):
        for btn in self.buttons:
            btn.update()

    def render_buttons(self):
        for btn in self.buttons:
            btn.render()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        # Add buttons
        self.btn_play = Button(self.center_x - 32, self.center_y,
                               self.game.assets["btn_play"], self.game.assets["btn_play_light"],
                               self.game.show_main_game_screen, self.game)

        self.btn_quit = Button(self.game.WIDTH - 40, self.game.HEIGHT - 40,
                               self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                               sys.exit, self.game)

        self.btn_settings = Button(8, 8,
                                   self.game.assets["btn_settings"], self.game.assets["btn_settings_light"],
                                   self.game.show_settings_screen, self.game)

        # TODO: Delete btn_minigame and its location in buttons when done with minigame testing
        self.btn_minigame = Button(self.center_x - 32, 8,
                                   self.game.assets["minigame"], self.game.assets["minigame_light"],
                                   self.game.show_minigame_screen, self.game)

        self.buttons.append(self.btn_play)
        self.buttons.append(self.btn_quit)
        self.buttons.append(self.btn_settings)
        self.buttons.append(self.btn_minigame)

    def on_show(self):
        if self.game.prev_game_screen != self.game.scrn_settings_menu:
            pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/8bitmusic.mp3'))
            pygame.mixer.music.play(-1)

    def update(self):
        self.update_buttons()

    def render(self):
        # Draws the background using the image
        self.game.screen.blit(self.game.assets["bg_main_menu"], (0, 0))

        # Title text
        self.game.draw_text('Shooting for the Stars', 40, self.center_x, self.center_y - 40)

        self.render_buttons()


class SettingsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.btn_exit = Button(8, 8,
                               self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                               self.game.show_previous_game_screen, self.game)

        self.btn_music_minus = Button(self.center_x - 64, self.center_y - 64,
                                      self.game.assets["btn_minus"], self.game.assets["btn_minus_light"],
                                      self.music_minus, self.game)

        self.btn_music_plus = Button(self.center_x + 32, self.center_y - 64,
                                     self.game.assets["btn_plus"], self.game.assets["btn_plus_light"],
                                     self.music_plus, self.game)

        self.btn_sfx_minus = Button(self.center_x - 64, self.center_y + 64,
                                    self.game.assets["btn_minus"], self.game.assets["btn_minus_light"],
                                    self.sfx_minus, self.game)

        self.btn_sfx_plus = Button(self.center_x + 32, self.center_y + 64,
                                   self.game.assets["btn_plus"], self.game.assets["btn_plus_light"],
                                   self.sfx_plus, self.game)

        self.buttons.append(self.btn_exit)
        self.buttons.append(self.btn_music_minus)
        self.buttons.append(self.btn_music_plus)
        self.buttons.append(self.btn_sfx_minus)
        self.buttons.append(self.btn_sfx_plus)

    def update(self):
        self.update_buttons()

    def render(self):
        # TODO: Why is this a solid color? Shouldn't it just be the same as the main menu bg?
        # Background color
        self.game.screen.fill((255, 140, 105))

        self.game.draw_text('Options', 50, self.center_x, self.center_y - 192)

        self.game.draw_text('Music Volume', 30, self.center_x, self.center_y - 96)
        self.game.draw_text(str(int(self.game.setting_music_volume * 10)), 30, self.center_x, self.center_y - 48)

        self.game.draw_text('SFX Volume', 30, self.center_x, self.center_y + 32)
        self.game.draw_text(str(int(self.game.setting_sfx_volume * 10)), 30, self.center_x, self.center_y + 80)

        self.render_buttons()

    def music_minus(self):
        self.game.setting_music_volume -= 0.1
        self.game.update_settings()

    def music_plus(self):
        self.game.setting_music_volume += 0.1
        self.game.update_settings()

    def sfx_minus(self):
        self.game.setting_sfx_volume -= 0.1
        self.game.update_settings()

    def sfx_plus(self):
        self.game.setting_sfx_volume += 0.1
        self.game.update_settings()


class GameOverMenu(Menu):
    def __init__(self, game, score=0):
        super().__init__(game)
        self.score = score
        self.btn_retry = Button(self.center_x - 48, self.center_y + 30,
                                self.game.assets["btn_retry"], self.game.assets["btn_retry_light"],
                                self.game.show_main_game_screen, self.game)

        self.btn_quit = Button(self.center_x + 32, self.center_y + 30,
                               self.game.assets["btn_quit"], self.game.assets["btn_quit_light"],
                               self.game.show_main_menu_screen, self.game)

        self.buttons.append(self.btn_retry)
        self.buttons.append(self.btn_quit)

    def on_show(self):
        # bgm source: https://thewhitepianokey.bandcamp.com/track/leaving-yoshi-slow-loopable
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'assets/gameover_bgm.mp3'))
        pygame.mixer.music.play(-1)

    def update(self):
        self.update_buttons()

    def render(self):
        # Draws the background using the image
        self.game.screen.blit(self.game.assets["bg_game"], (0, 0))

        # Text
        self.game.draw_text('Game Over', 40, self.center_x, self.center_y - 40)
        self.game.draw_text('Score: ' + str(self.score), 30, self.center_x, self.center_y - 80)

        self.render_buttons()
