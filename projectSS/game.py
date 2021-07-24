import pygame
import sys
import os
from projectSS.menus import MainMenu, SettingsMenu, GameOverMenu
from projectSS.gameplayscreen import GameplayScreen
from projectSS.minigame import MinigameScreen


# Icon made by Freepik from www.flaticon.com
# Icon made by Kiranshastry from www.flaticon.com   # TODO: Delete once minigame testing is complete
# Icon made by iconixor from www.flaticon.com
# Music in the background from https://www.FesliyanStudios.com

class Game:
    # Initialization of the game. This includes starting up pygame, creating the screen, loading assets,
    # and creating menus.
    def __init__(self):
        # starts up pygame
        pygame.init()
        self.running = True

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
                         "btn_quit": pygame.image.load(os.path.join(abs_dir, 'assets/exit.png')),
                         "btn_quit_light": pygame.image.load(os.path.join(abs_dir, 'assets/exit_light.png')),
                         "btn_play": pygame.image.load(os.path.join(abs_dir, 'assets/play.png')),
                         "btn_play_light": pygame.image.load(os.path.join(abs_dir, 'assets/play_light.png')),
                         "btn_settings": pygame.image.load(os.path.join(abs_dir, 'assets/settings.png')),
                         "btn_settings_light": pygame.image.load(os.path.join(abs_dir, "assets/settings_light.png")),
                         "btn_minus": pygame.image.load(os.path.join(abs_dir, "assets/minus.png")),
                         "btn_minus_light": pygame.image.load(os.path.join(abs_dir, "assets/minus-light.png")),
                         "btn_plus": pygame.image.load(os.path.join(abs_dir, "assets/plus.png")),
                         "btn_plus_light": pygame.image.load(os.path.join(abs_dir, "assets/plus_light.png")),
                         "btn_retry": pygame.image.load(os.path.join(abs_dir, 'assets/retry.png')),
                         "btn_retry_light": pygame.image.load(os.path.join(abs_dir, 'assets/retry_light.png')),
                         "bg_main_menu": pygame.image.load(os.path.join(abs_dir, 'assets/mainbg.png')),
                         "bg_game": pygame.image.load(os.path.join(abs_dir, 'assets/gamebg.png')),
                         "font_loc": os.path.join(abs_dir, 'assets/playmegames.ttf'),
                         "sfx_blip": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/blip.wav')),
                         "minigame": pygame.image.load(os.path.join(abs_dir, 'assets/minigame.png')),
                         "minigame_light": pygame.image.load(os.path.join(abs_dir, 'assets/minigame_light.png')),
                         "bg_minigame": pygame.image.load(os.path.join(abs_dir, 'assets/minigame_bg.png')),
                         "circle": pygame.image.load(os.path.join(abs_dir, 'assets/circle.png')),
                         "sfx_hit": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/hit.wav')),
                         "enemy_disc": pygame.image.load(os.path.join(abs_dir, 'assets/disc.png'))}

        # setup sfx list
        self.sfx = [self.assets["sfx_blip"], self.assets["sfx_hit"]]

        # Window caption and icon
        pygame.display.set_caption("Shooting For The Stars")
        pygame.display.set_icon(self.__assets["icon"])

        # Game settings
        self.setting_music_volume = 0.8
        self.setting_sfx_volume = 0.8
        self.update_settings()

        # Stores the mouse position in a tuple. [0] accesses x, [1] accesses y.
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False

        # Initialize game screens
        self.scrn_main_menu = MainMenu(self)
        self.scrn_settings_menu = SettingsMenu(self)
        self.scrn_gameplay_screen = GameplayScreen(self)
        self.scrn_gameover_menu = GameOverMenu(self, self.scrn_gameplay_screen)
        self.scrn_minigame_screen = MinigameScreen(self)

        # Set MainMenu as default game screen
        self.game_screen = self.scrn_main_menu

        # Game screen to change to on the next update
        self.next_game_screen = None

        # Keep track of previous screen to know where to return on button clicks.
        self.prev_game_screen = None

        self.game_screen.on_show()

        # Fixed FPS timer
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()

        # Run game
        self.game_loop()

    def game_loop(self):
        while self.running:
            # Limit FPS to fixed value
            self.FramePerSec.tick(self.FPS)
            self.update()
            self.render()

    # Main update function. Updates user I/O and game logic
    def update(self):
        # Update mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False

        # Handle events
        for event in pygame.event.get():
            # if X button of window is clicked the game is exited
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_clicked = True

        # Change game screen if necessary
        if self.next_game_screen is not None:
            self.prev_game_screen = self.game_screen
            self.game_screen = self.next_game_screen
            self.game_screen.on_show()

            self.next_game_screen = None

        # Update current game screen
        self.game_screen.update()

    # Main render function
    def render(self):

        # Clear screen
        self.screen.fill((0, 0, 0))

        # Render current game screen
        self.game_screen.render()

        # Tell PyGame to update screen with everything drawn
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.__assets["font_loc"], size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Methods used by the current game screen to change to a different game screen
    def show_main_menu_screen(self):
        self.next_game_screen = self.scrn_main_menu

    def show_settings_screen(self):
        self.next_game_screen = self.scrn_settings_menu

    def show_main_game_screen(self):
        self.next_game_screen = self.scrn_gameplay_screen

    def show_previous_game_screen(self):
        self.next_game_screen = self.prev_game_screen

    def show_game_over_screen(self):
        self.scrn_gameover_menu.score = int(self.scrn_gameplay_screen.best_distance)
        self.next_game_screen = self.scrn_gameover_menu

    def show_minigame_screen(self):
        self.next_game_screen = self.scrn_minigame_screen

    # Apply settings updates
    def update_settings(self):

        # Set volumes min/max
        if self.setting_music_volume < 0:
            self.setting_music_volume = 0
        elif self.setting_music_volume > 1:
            self.setting_music_volume = 1

        if self.setting_sfx_volume < 0:
            self.setting_sfx_volume = 0
        elif self.setting_sfx_volume > 1:
            self.setting_sfx_volume = 1

        # Apply volumes
        pygame.mixer.music.set_volume(self.setting_music_volume * 0.1)

        # TODO: All sfx should be in a list so they can be updated here, don't hard code
        for s in self.sfx:
            s.set_volume(self.setting_sfx_volume * 0.5)

    @property
    def assets(self):
        return self.__assets

