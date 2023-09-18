from gameEngine import GameEngine
from credits import Credits
from help import HelpScreen
from endScreen import EndScreen

class GameStateManager:
    def __init__(self):
        self.current_state = None
        self.args = None

    def set_state(self, state_name, *args, current_score=0):
        if state_name == "main_menu":
            from main import MainMenu 
            self.current_state = MainMenu(*args)
        elif state_name == "game":
            self.current_state = GameEngine(*args)
        elif state_name == "credits":
            self.current_state = Credits(*args)
        elif state_name == "help":
            self.current_state = HelpScreen(*args)
        elif state_name == "end":
                    self.current_state = EndScreen(*args)

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
   


