import pygame
from pygame.locals import *
import sys
from button import Button
from misc import title, playClickSound
from gameState import GameStateManager

pygame.init()
pygame.mixer.init()

SCREEN_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Menu")

game_state_manager = GameStateManager()

# Constants for button properties
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
BUTTON_Y_OFFSET = 125

class MainMenu:
    def __init__(self, SCREEN, game_state_manager):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.font = pygame.font.Font("assets/font.ttf", 55)
        self.background_image = pygame.image.load("assets/background.png")

    def create_buttons(self):
        #positions of each button placement
        button_data = [
            {"pos": (640, 250), "text": "PLAY", "font": self.font},
            {"pos": (640, 350), "text": "HELP", "font": self.font},
            {"pos": (640, 450), "text": "SHOP", "font": self.font},
             {"pos": (640, 550), "text": "CREDITS", "font": self.font},
            {"pos": (640, 650), "text": "QUIT", "font": self.font},
        ]

        buttons = []
        for data in button_data:
            button = Button(
                image=pygame.image.load("assets/rect.png"),
                pos=data["pos"],
                text_input=data["text"],
                font=data["font"],
                base_color="#511c57",
                hovering_color="#FBF9FB",
                click_sound=playClickSound,
            )
            buttons.append(button)
        return buttons

    def run(self):
        running = True
        buttons = self.create_buttons()
        
        while running:
            self.SCREEN.blit(self.background_image, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            title_height = title.get_height()
            screen_height = self.SCREEN.get_height()
            title_x = (self.SCREEN.get_width() - title.get_width()) // 2
            title_y = (screen_height - title_height) // 8
            self.SCREEN.blit(title, (title_x, title_y))

            for button in buttons:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.checkForInput(MENU_MOUSE_POS):
                            playClickSound()
                            if button.text_input == "PLAY":
                                self.game_state_manager.set_state("game", self.SCREEN, game_state_manager=self.game_state_manager)
                                return
                            elif button.text_input == "HELP":
                                self.game_state_manager.set_state("help", self.SCREEN, game_state_manager=self.game_state_manager)
                                return
                            elif button.text_input == "CREDITS":
                                self.game_state_manager.set_state("credits", self.SCREEN, game_state_manager=self.game_state_manager)
                                return
                            
                            elif button.text_input == "SHOP":
                                self.game_state_manager.set_state("shop", self.SCREEN, game_state_manager=self.game_state_manager)
                                return
                            
                            elif button.text_input == "QUIT":
                                pygame.quit()
                                sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    game_state_manager.set_menu_theme()  
    game_state_manager.set_state("main_menu", SCREEN, game_state_manager=game_state_manager)

    while True:
        game_state_manager.run()
