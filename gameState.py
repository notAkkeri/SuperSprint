from gameEngine import GameEngine
from credits import Credits
from help import HelpScreen
from endScreen import EndScreen
import pygame 

class GameStateManager:
    def __init__(self):
        self.current_state = None
        self.args = None
        self.menu_Theme_music = None  
        self.game_Theme_music = None

    def set_menu_theme(self):
        if self.menu_Theme_music is None:
            from misc import menu_Theme
            self.menu_Theme_music = menu_Theme()
            self.menu_Theme_music.play(-1)

    def set_game_theme(self):
        if self.game_Theme_music is None:
            from misc import gameTheme
            self.game_Theme_music = gameTheme()
            self.game_Theme_music.play(loops=-1)

    def set_state(self, state_name, SCREEN, game_state_manager, *args, current_score=0):
        if state_name == "main_menu":
            from main import MainMenu 
            self.set_menu_theme()
            main_menu = MainMenu(SCREEN, game_state_manager)

            self.current_state = main_menu

        elif state_name == "game":
            # Stop the menu theme if it's playing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.set_game_theme()
            self.current_state = GameEngine(SCREEN, game_state_manager, *args)

        elif state_name == "credits":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.current_state = Credits(SCREEN, game_state_manager, menu_Theme_music=self.menu_Theme_music, *args)
        elif state_name == "help":
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            self.current_state = HelpScreen(SCREEN, game_state_manager, menu_Theme_music=self.menu_Theme_music, *args)
        elif state_name == "end":
            if self.game_Theme_music is not None:
                self.game_Theme_music.stop()  
            self.current_state = EndScreen(SCREEN, game_state_manager, *args)

    def run(self):
        if self.current_state:
            self.current_state.run()


def start_main_menu(self, SCREEN, game_state_manager):
    main_menu = MainMenu(SCREEN, game_state_manager)
    main_menu.run()

# start game 
def startGameEngine(SCREEN, next_state_callback=None):
    game_engine = GameEngine(SCREEN, next_state_callback)
    game_engine.run()

# start credits
def displayCredits(SCREEN, next_state_callback=None):
    credits_state = Credits(SCREEN, next_state_callback)
    credits_state.run()

# start help
def displayHelp(SCREEN, next_state_callback=None):
    help_screen = HelpScreen(SCREEN, next_state_callback)
    help_screen.run()

def displayEnd(SCREEN, game_state_manager):
    end_screen = EndScreen(SCREEN, game_state_manager)
    end_screen.run()
   


