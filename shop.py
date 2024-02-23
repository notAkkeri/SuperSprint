import pygame
import sys
from button import Button
from misc import get_font,playClickSound


class ShopScreen:
    def __init__(self, SCREEN, game_state_manager, menu_Theme_music):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.menu_Theme_music = menu_Theme_music
        self.back_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(120, 60),
                                text_input="BACK", font=get_font(30), base_color="#f1e8ef", hovering_color="#1b1018",
                                click_sound=playClickSound)
        
    def run(self):
        while True:  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(pygame.mouse.get_pos()):
                        pygame.display.set_caption("Menu")
                        playClickSound() 
                        self.game_state_manager.set_state("main_menu", self.SCREEN, self.game_state_manager) 
                        return



            self.SCREEN.fill((0, 0, 0))
            pygame.display.set_caption("Shop")

            # displays background image
            background_image = pygame.image.load("assets/background.png")
            self.SCREEN.blit(background_image, (0, 0))


            self.back_button.changeColor(pygame.mouse.get_pos())
            self.back_button.update(self.SCREEN)

            pygame.display.update()

