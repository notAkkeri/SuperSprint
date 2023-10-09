import pygame
import sys
from button import Button
from misc import get_font, get_font1, playClickSound

class HelpScreen:
    def __init__(self, SCREEN, game_state_manager, menu_Theme_music):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.menu_Theme_music = menu_Theme_music
        self.back_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(80, 640),
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
            pygame.display.set_caption("Help")

            # displays background image
            background_image = pygame.image.load("assets/background.png")
            self.SCREEN.blit(background_image, (0, 0))
            # Text dict
            categories = [
                ("How To Play:", ["Avoid obstacles and collect coins!", "Beat previously set scores", "Challenge your friends!"]),
                ("Coin Values:", ["Gold: 55", "Silver: 25", "Bronze: 5"]),
                ("Obstacles:", ["Boulders: 1Heart", "Birbs: 1Heart"])
            ]
            
            y_position = 20  

            for category, subheadings in categories:
                # headings
                heading_text = get_font1(65).render(category, True, "#FFF1FD")
                self.SCREEN.blit(heading_text, (440, y_position))
                y_position += 65 

                # subheadings
                for subheading in subheadings:
                    subheading_text = get_font1(50).render(subheading, True, "#B668AA")
                    self.SCREEN.blit(subheading_text, (440, y_position))
                    y_position += 55  

            # Update the back button
            self.back_button.changeColor(pygame.mouse.get_pos())
            self.back_button.update(self.SCREEN)

            pygame.display.update()

