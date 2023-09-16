import pygame
from pygame.locals import *
import sys
from button import Button
from misc import get_font, title, click_sound, menu_Theme
from gameState import GameStateManager
pygame.init()
pygame.mixer.init()

SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load("assets/background.png")
pygame.display.set_caption("Menu")

# menu theme
menu_Theme_music = menu_Theme()

game_state_manager = GameStateManager()

# The main menu
class MainMenu:
    def __init__(self, SCREEN, game_state_manager):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.menu_Theme_music = menu_Theme()

    def run(self):
        # Play menu theme
        self.menu_Theme_music.play(-1)
        running = True
        while running:
            self.SCREEN.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Title (Super Sprint)
            title_height = title.get_height()
            screen_height = self.SCREEN.get_height()

            title_x = (self.SCREEN.get_width() - title.get_width()) // 2
            title_y = (screen_height - title_height) // 8
            self.SCREEN.blit(title, (title_x, title_y))

            # Buttons
            PLAY_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 300),
                                 text_input="PLAY", font=get_font(75), base_color="#f1e8ef", hovering_color="#1b1018",
                                 click_sound=click_sound)

            HELP_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 425),
                                 text_input="HELP", font=get_font(75), base_color="#f1e8ef", hovering_color="#1b1018",
                                 click_sound=click_sound)

            EXIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=get_font(75), base_color="#f1e8ef", hovering_color="#1b1018",
                                 click_sound=click_sound)

            CREDITS_BUTTON = Button(image=pygame.image.load("assets/rect1.png"), pos=(1180, 640),
                                    text_input="CREDITS", font=get_font(25), base_color="#f1e8ef", hovering_color="#1b1018",
                                    click_sound=click_sound)

            # Loop through the buttons, change colors based on hover, and update the display
            for button in [PLAY_BUTTON, EXIT_BUTTON, CREDITS_BUTTON, HELP_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click_sound.play()
                        self.menu_Theme_music.stop()
                        self.game_state_manager.set_state("game", self.SCREEN, self.game_state_manager)
                        return  # Return to exit the MainMenu run loop

                    if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click_sound.play()
                        self.game_state_manager.set_state("help", self.SCREEN, self.game_state_manager)
                        return

                    if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

                    if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click_sound.play()
                        self.game_state_manager.set_state("credits", self.SCREEN, self.game_state_manager)
                        return

            pygame.display.update()

if __name__ == "__main__":
    game_state_manager = GameStateManager()
    game_state_manager.set_state("main_menu", SCREEN, game_state_manager)  

    while True:
        game_state_manager.run()


