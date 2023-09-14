import pygame
from pygame.locals import *
from pygame import mixer 
import sys
from button import Button 
from credits import displayCredits  
from gameEngine import displayGame 
from help import displayHelp
from misc import get_font, title, click_sound, menu_Theme

pygame.init()
pygame.mixer.init()

SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load("assets/background.png")
pygame.display.set_caption("Menu")

# menu theme
menu_Theme_music = menu_Theme()

# The main menu
def mainMenu():
    # Playing menu theme
    menu_Theme_music.play(-1)
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Title (Super Sprint)
        title_height = title.get_height()
        screen_height = SCREEN.get_height()

        title_x = (SCREEN.get_width() - title.get_width()) // 2
        title_y = (screen_height - title_height) // 8
        SCREEN.blit(title, (title_x, title_y))
    
        # buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 300),
                             text_input="PLAY", font=get_font(75), base_color="#fbfdb7", hovering_color="#f8cd78",
                            click_sound=click_sound)
        
        HELP_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 425),
                             text_input="HELP", font=get_font(75), base_color="#fbfdb7", hovering_color="#f8cd78",
                             click_sound=click_sound)
                             
        EXIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#fbfdb7", hovering_color="#f8cd78",
                             click_sound=click_sound)
        
        CREDITS_BUTTON= Button(image=pygame.image.load("assets/rect1.png"), pos=(1180, 640),
                                text_input="CREDITS", font=get_font(30), base_color="#fbfdb7", hovering_color="#f8cd78",
                                click_sound=click_sound)

        # loops the buttons, changes the colour (based on which is hovered) & updates the display 
        for button in [PLAY_BUTTON, EXIT_BUTTON, CREDITS_BUTTON, HELP_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    menu_Theme_music.stop()
                    displayGame(SCREEN)        
                    pygame.display.set_caption("Menu")
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    displayHelp(SCREEN)
                    pygame.display.set_caption("Menu")
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    displayCredits(SCREEN) 
                    pygame.display.set_caption("Menu")
                
        pygame.display.update()

mainMenu()

