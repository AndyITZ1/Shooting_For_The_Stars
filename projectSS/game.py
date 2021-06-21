import sys
import os
from projectSS.menus import *

# Icon made by Freepik from www.flaticon.com


class Game:
    # Initialization of the game. This includes starting up pygame, creating the screen, loading assets,
    # and creating menus.
    def __init__(self):
        # starts up pygame
        pygame.init()
        self.playing = False        # TODO: What are these three variables for?
        self.set_pressed = False
        self.LEFT_CLICK = False

        # width and height of the game window (resolution)
        self.WIDTH = 800
        self.HEIGHT = 600

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # loading assets. PLEASE use the below line of code to import assets! Without it, the installation will break!
        # Most GUI images are 32x32. Main menu background is 800x600, to match resolution.
        # GUI elements have a gradiant version named "light" that will replace it when the mouse hovers over it.
        # This dictionary of assets DOES NOT handle background music (but does handle SFX blip)!
        abs_dir = os.path.dirname(__file__)
        self.__assets = {"icon": pygame.image.load(os.path.join(abs_dir, 'assets/musical_notes.png')),
                         "quit_img": pygame.image.load(os.path.join(abs_dir, 'assets/exit.png')),
                         "quit_light": pygame.image.load(os.path.join(abs_dir, 'assets/exit_light.png')),
                         "play_button": pygame.image.load(os.path.join(abs_dir, 'assets/play.png')),
                         "play_light": pygame.image.load(os.path.join(abs_dir, 'assets/play_light.png')),
                         "settings": pygame.image.load(os.path.join(abs_dir, 'assets/settings.png')),
                         "settings_light": pygame.image.load(os.path.join(abs_dir, "assets/settings_light.png")),
                         "main_menu_bg": pygame.image.load(os.path.join(abs_dir, 'assets/gamebg.png')),
                         "font_loc": os.path.join(abs_dir, 'assets/playmegames.ttf'),
                         "sfx_blip": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/blip.wav'))}

        # Window caption and icon
        pygame.display.set_caption("Shooting For The Stars")
        pygame.display.set_icon(self.__assets["icon"])

        # draws the background using the image
        self.screen.blit(self.__assets["main_menu_bg"], (0, 0))

        # load music, set volume, -1 = plays song infinitely, change it to 0 to play once only
        pygame.mixer.music.load(os.path.join(abs_dir, 'assets/8bitmusic.mp3'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        # GUI click sound volume (SFX blip)
        self.__assets["sfx_blip"].set_volume(0.4)

        # Stores the mouse position in a tuple. [0] accesses x, [1] accesses y.
        self.mouse = pygame.mouse.get_pos()

        # Menus. Each screen is handled by a Menu class. TODO: store these menus in a dictionary.
        self.main_menu = MainMenu(self)
        self.options_menu = SettingsMenu(self)

        # When the game initializes, we want the first game menu to be the main menu.
        self.menu = self.main_menu


    def game_loop(self):
        while self.playing:
            # Begin game loop (ticK) by checking for events.
            self.check_events()

            # TODO: what is this if statement supposed to do/represent?
            if self.__assets["settings"]:
                self.playing = False

            # this is to update the game loop.
            # TODO: What is this fill() function's purpose in the loop?
            self.screen.fill((0, 0, 0))

            # Update any screen drawings.
            pygame.display.update()

            # TODO: What is this state reset supposed to mean?
            self.reset_state()

    def check_events(self):
        # Update mouse position.
        self.mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # if X button of window is clicked the game is exited
            if event.type == pygame.QUIT:
                sys.exit()

            # if quit button location is clicked the game is exited
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 800 >= self.mouse[0] >= 800 - 32 and 600 >= self.mouse[1] >= 600 - 32:
                    sys.exit()
                # Else if we click on the settings icon
                elif 0 <= self.mouse[0] <= 35 and 0 <= self.mouse[1] <= 35:
                    self.set_pressed = True
                    self.__assets["sfx_blip"].play()
                self.LEFT_CLICK = True

    def reset_state(self):
        self.set_pressed = False
        self.LEFT_CLICK = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.__assets["font_loc"], size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    @property
    def assets(self):
        return self.__assets
