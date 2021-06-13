import pygame


# menu base class for handling multiple menus
class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.run_display = True


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Home'
        self.play_x, self.play_y = self.mid_w - 32, self.mid_h
        self.quit_x, self.quit_y = self.game.WIDTH - 32, self.game.HEIGHT - 32
        self.setting_x, self.setting_y = 0, 0

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # draws the background using the image
            self.game.screen.blit(self.game.gamebg, (0, 0))
            # the default quit button will be drawn and if hovered over the quit light up button is drawn instead
            if self.game.WIDTH >= self.game.mouse[0] >= self.quit_x and self.game.HEIGHT >= self.game.mouse[1] >= self.quit_y:
                self.game.screen.blit(self.game.quit_light_img, (self.quit_x, self.quit_y))
            else:
                self.game.screen.blit(self.game.quit_img, (self.quit_x, self.quit_y))

            # play button
            if self.mid_w + 32 >= self.game.mouse[0] >= self.play_x and self.mid_h+64 >= self.game.mouse[1] >= self.mid_h:
                self.game.screen.blit(self.game.play_light, (self.play_x, self.play_y))
            else:
                self.game.screen.blit(self.game.play_button, (self.play_x, self.play_y))

            # settings button
            self.game.screen.blit(self.game.settings, (self.setting_x, self.setting_y))

            pygame.display.update()

    def check_input(self):
        if self.game.set_pressed:
            self.game.menu = self.game.options_menu
            self.run_display = False


# TODO finish settings menu
class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((20, 20, 20))
            pygame.display.update()

    def check_input(self):
        pass
