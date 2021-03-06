import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import pygame
import json
from projectSS.menus import MainMenu, SettingsMenu, GameOverMenu, LevelCompleteMenu
from projectSS.gameplayscreen import GameplayScreen
from projectSS.minigame import MinigameScreen


# --------------- In-code asset acknowledgement --------------- #
#
#   Icon made by Freepik from www.flaticon.com
#   Icon made by iconixor from www.flaticon.com
#   Boss encounter & minigame win SFX's made by Tony Parsons at dreamstime.com
#   Music in the background from https://www.FesliyanStudios.com

class Game:
    """
    Shooting For The Stars game class. This class handles the entire functioning of the game by just initializing it.
    """

    def __init__(self):
        # --------------- Pygame initialization --------------- #

        pygame.init()
        self.running = True     # Boolean that tells the game loop to continue.

        # Game window resolution.
        self.WIDTH = 800
        self.HEIGHT = 600

        # Creation of the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # --------------- Game assets --------------- #

        #   * PLEASE use the below line of code to import assets! Without it, user installation will break!
        #   * Most GUI images are 32x32.
        #   * GUI elements have a gradiant version named "light" that will replace it when the mouse hovers over it.
        #   * This dictionary of assets DOES NOT handle background music (but does handle SFX blip)!
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
                         "sfx_jump": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/jump.wav')),
                         "sfx_pushed": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/pushed.wav')),
                         "sfx_boostjump": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/boostjump.wav')),
                         "sfx_loseshield": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/loseshield.wav')),
                         "sfx_pickup": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/pickup.wav')),
                         "enemy_disc": pygame.image.load(os.path.join(abs_dir, 'assets/disc.png')),
                         "sfx_boss": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/boss_encounter.wav')),
                         "sfx_boss_win": pygame.mixer.Sound(os.path.join(abs_dir, 'assets/boss_win.wav'))}

        # SFX List.
        self.sfx = [self.assets["sfx_blip"], self.assets["sfx_hit"], self.assets["sfx_jump"], self.assets["sfx_pushed"],
                    self.assets["sfx_boostjump"], self.assets["sfx_loseshield"], self.assets["sfx_pickup"],
                    self.assets["sfx_boss"], self.assets["sfx_boss_win"]]

        # Window caption and icon.
        pygame.display.set_caption("Shooting For The Stars")
        pygame.display.set_icon(self.__assets["icon"])

        # Set default music and SFX volumes and update them through a dedicated helper function.
        self.setting_music_volume = 0.8
        self.setting_sfx_volume = 0.8
        self.update_settings()

        # Saving user data, level and high score
        self.user_data = [0, 0]
        if os.path.isfile(os.path.join(abs_dir, 'userData.json')) and os.access(os.path.join(abs_dir, 'userData.json'), os.R_OK):
            f = open(os.path.join(abs_dir, 'userData.json'), "r")
            self.user_data = json.load(f)
            f.close()
        else:
            f = open(os.path.join(abs_dir, 'userData.json'), "w")
            f.write(json.dumps(self.user_data))
            f.close()

        # --------------- Game Logic --------------- #

        # Stores the mouse position in a tuple. mouse_pos[0] accesses x, mouse_pos[1] accesses y.
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False

        # Initialize game screens/menus. Game.update() handles switching between screens/menus.
        self.scrn_main_menu = MainMenu(self)
        self.scrn_settings_menu = SettingsMenu(self)
        self.scrn_gameplay_screen = GameplayScreen(self)
        self.scrn_gameover_menu = GameOverMenu(self, self.scrn_gameplay_screen)
        self.scrn_level_complete_menu = LevelCompleteMenu(self, self.scrn_gameplay_screen)
        self.scrn_minigame_screen = MinigameScreen(self, self.scrn_gameplay_screen)

        # Stores the next game screen that will be switched to in the next iteration of Game.update().
        self.next_game_screen = None

        # Keeps track of the previous screen to know where to return on button clicks.
        self.prev_game_screen = None

        # Set MainMenu as default game screen. It will be the first screen to be seen by the user.
        self.game_screen = self.scrn_main_menu

        # Call upon the MainMenu's on_show() method to begin it's initialization.
        self.game_screen.on_show()

        # Fixed FPS timer to maintain a smooth gaming experience.
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()

        # Begin to run the game.
        self.game_loop()

    def game_loop(self):
        """
        As with any video game, Shooting For The Stars' loop is contained in a method. Each iteration of the loop is
        considered a "tick" in the game. Each tick controls game FPS, logic, and rendering.
        """

        while self.running:
            # Limit FPS to fixed value.
            self.FramePerSec.tick(self.FPS)
            self.update()
            self.render()

    def update(self):
        """
        This function, which is called in each iteration of Game.game_loop(), ensures that game logic progresses.
        """

        # Update mouse position. Reset mouse_clicked boolean from any previous mouse clicks.
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_clicked = False

        # Event handling
        for event in pygame.event.get():
            # If X button of window is clicked the game is exited
            if event.type == pygame.QUIT:
                sys.exit()

            # If user clicked the mouse, update the corresponding boolean.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_clicked = True

        # Change game screen if necessary.
        if self.next_game_screen is not None:
            self.prev_game_screen = self.game_screen
            self.game_screen = self.next_game_screen
            self.next_game_screen = None

            if self.prev_game_screen == self.scrn_minigame_screen:
                if not self.scrn_minigame_screen.minigame_mode:
                    # Reload music and reset rhythm mechanic timer.
                    pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), self.scrn_gameplay_screen.music_file))
                    pygame.mixer.music.play(-1)
                    self.scrn_gameplay_screen.rhy_start_time = time.time()
                else:
                    self.game_screen.on_show()
            elif self.prev_game_screen == self.scrn_settings_menu and self.game_screen == self.scrn_gameplay_screen:
                pass
            else:
                self.game_screen.on_show()  # Call on the new game_screen to initialize itself.

        # Call on the current game_screen's update() method to allow it to progress its game logic.
        self.game_screen.update()

    def render(self):
        """
        This method handles rendering to the screen by resetting it, calling on the current game_screen's respective
        render() method, and updating the screen. Called in each iteration of Game.game_loop().
        """

        self.screen.fill((0, 0, 0))
        self.game_screen.render()
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        """
        Helper function called in various game screens/menus to draw text to the screen.

        :param text: String containing desired message to user.
        :param size: The desired size of the text.
        :param x: The x position of the screen where text will be displayed.
        :param y: The y position of the screen where text will be displayed.
        """
        font = pygame.font.Font(self.__assets["font_loc"], size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # --------------- Methods used by the current game screen to change to a different game screen --------------- #

    def show_main_menu_screen(self):
        self.next_game_screen = self.scrn_main_menu
        self.save_user_data()

    def show_settings_screen(self):
        self.next_game_screen = self.scrn_settings_menu

    def show_gameplay_screen(self):
        if self.gameplay.level > self.gameplay.highest_level:
            self.__assets['sfx_pushed'].play()
        else:
            self.next_game_screen = self.scrn_gameplay_screen
            self.save_user_data()

    def show_previous_game_screen(self):
        self.next_game_screen = self.prev_game_screen

    def show_game_over_screen(self):
        self.scrn_gameover_menu.score = int(self.scrn_gameplay_screen.best_distance)
        self.scrn_gameover_menu.endless = self.scrn_gameplay_screen.endless
        self.scrn_gameover_menu.highscore = int(self.scrn_gameplay_screen.high_score)
        self.save_user_data()
        self.next_game_screen = self.scrn_gameover_menu
    
    def show_level_complete_screen(self):
        self.next_game_screen = self.scrn_level_complete_menu
        self.save_user_data()
    
    def show_minigame_screen(self):
        self.next_game_screen = self.scrn_minigame_screen

    def update_settings(self):
        """
        The game's dedicated function for setting the music and SFX volumes. Also takes care of edge cases.
        """

        # Set volumes min/max
        if self.setting_music_volume < 0:
            self.setting_music_volume = 0
        elif self.setting_music_volume > 1:
            self.setting_music_volume = 1

        if self.setting_sfx_volume < 0:
            self.setting_sfx_volume = 0
        elif self.setting_sfx_volume > 1:
            self.setting_sfx_volume = 1

        # Modify the music's volume. Pygame represents music volume with values between 0 - 1, hence the 0.1 value.
        pygame.mixer.music.set_volume(self.setting_music_volume * 0.1)

        # Modify all of the stored SFXs' volumes.
        for s in self.sfx:
            s.set_volume(self.setting_sfx_volume * 0.5)

    def save_user_data(self):
        abs_dir = os.path.dirname(__file__)
        self.user_data[0] = self.gameplay.highest_level
        self.user_data[1] = self.gameplay.high_score
        f = open(os.path.join(abs_dir, 'userData.json'), "w")
        f.write(json.dumps(self.user_data))
        f.close()

    @property
    def assets(self):
        return self.__assets

    @property
    def gameplay(self):
        return self.scrn_gameplay_screen
