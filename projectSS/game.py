import pygame
import sys
from menu import *


class Game:
    def __init__(self):
        # starts up game
        pygame.init()
        self.playing = False
        self.set_pressed = False

        # width and height of the window
        self.WIDTH = 800
        self.HEIGHT = 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # loading assets
        # black-colored quit button (default look) (32x32)
        self.quit_img = pygame.image.load('assets/exit.png')
        # when hovered quit button lights up (32x32)
        self.quit_light_img = pygame.image.load('assets/exit_light.png')

        self.play_button = pygame.image.load('assets/play.png')
        self.play_light = pygame.image.load('assets/playlight.png')

        self.settings = pygame.image.load('assets/settings.png')

        # background 800 x 600 img
        self.gamebg = pygame.image.load('assets/gamebg.png')

        # load music, set volume, -1 = plays song infinitely, change it to 0 to play once only
        pygame.mixer.music.load('assets/8bitmusic.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.mouse = pygame.mouse.get_pos()

        # draws the background using the image
        self.screen.blit(self.gamebg, (0, 0))

        # menus
        self.main_menu = MainMenu(self)
        self.options_menu = SettingsMenu(self)
        self.menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.settings:
                self.playing = False
            # this is to update the game loop
            self.screen.fill((0, 0, 0))
            pygame.display.update()
            self.reset_state()

    def check_events(self):
        self.mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # if X button of window is clicked the game is exited
            if event.type == pygame.QUIT:
                sys.exit()

            # if quit button location is clicked the game is exited
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 800 >= self.mouse[0] >= 800 - 32 and 600 >= self.mouse[1] >= 600 - 32:
                    sys.exit()
                elif 0 <= self.mouse[0] <= 32 and 0 <= self.mouse[1] <= 32:
                    self.set_pressed = True

    def reset_state(self):
        self.set_pressed = False
