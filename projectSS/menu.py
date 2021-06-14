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
        self.setting_x, self.setting_y = 3, 3

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            # draws the background using the image
            self.game.screen.blit(self.game.gamebg, (0, 0))

            self.game.draw_text('Shooting for the Stars', 40, self.mid_w, self.mid_h-40)
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
            self.game.reset_state()

    def check_input(self):
        if self.game.set_pressed:
            self.game.menu = self.game.options_menu
            self.run_display = False


class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.music_level = 5
        self.sfx_level = 5

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.screen.fill((255, 140, 105))
            # back to main menu
            self.game.screen.blit(self.game.quit_img, (3, 3))

            self.game.draw_text('Options', 50, self.mid_w, self.mid_h*0.4)
            self.game.draw_text('Music Volume', 30, self.mid_w, self.mid_h*0.6)
            self.game.draw_text('-', 30, self.mid_w*0.6, self.mid_w*0.6)
            for i in range(0, self.music_level):
                pygame.draw.rect(self.game.screen, (0, 0, 0), pygame.Rect(self.mid_w*(0.63+i*0.08), self.mid_h*0.75, 12, 20))
            self.game.draw_text('+', 30, self.mid_w*1.4, self.mid_h*0.8)
            self.game.draw_text('SFX Volume', 30, self.mid_w, self.mid_h)
            self.game.draw_text('-', 30, self.mid_w*0.6, self.mid_h*1.2)
            for i in range(0, self.sfx_level):
                pygame.draw.rect(self.game.screen, (0, 0, 0), pygame.Rect(self.mid_w*(0.63+i*0.08), self.mid_h*1.15, 12, 20))
            self.game.draw_text('+', 30, self.mid_w*1.4, self.mid_h*1.2)
            pygame.display.update()
            self.game.reset_state()

    def check_input(self):
        blip_flag = False
        if self.game.LEFT_CLICK:
            blip_flag = True
            if self.mid_w*0.58 <= self.game.mouse[0] <= self.mid_w*0.62 and self.mid_h*0.78 <= self.game.mouse[1] <= self.mid_w*0.82:
                if self.music_level > 0:
                    self.music_level -= 1
                    pygame.mixer.music.set_volume(self.music_level*0.02)
            elif self.mid_w*1.38 <= self.game.mouse[0] <= self.mid_w*1.42 and self.mid_h*0.78 <= self.game.mouse[1] <= self.mid_w*0.82:
                if self.music_level < 10:
                    self.music_level += 1
                    pygame.mixer.music.set_volume(self.music_level*0.02)
            elif self.mid_w*0.58 <= self.game.mouse[0] <= self.mid_w*0.62 and self.mid_h*1.18 <= self.game.mouse[1] <= self.mid_w*1.22:
                if self.music_level > 0:
                    self.sfx_level -= 1
                    self.game.sfx_blip.set_volume(self.sfx_level*0.08)
            elif self.mid_w*1.38 <= self.game.mouse[0] <= self.mid_w*1.42 and self.mid_h*1.18 <= self.game.mouse[1] <= self.mid_w*1.22:
                if self.music_level < 10:
                    self.sfx_level += 1
                    self.game.sfx_blip.set_volume(self.sfx_level*0.08)
            else:
                blip_flag = False
        if self.game.set_pressed:
            blip_flag = True
            self.game.menu = self.game.main_menu
            self.run_display = False

        if blip_flag:
            self.game.sfx_blip.play()

