import pygame
import sys
from button import Button 
from credits import displayCredits  # imports credits 
#from gameEngine import displayGame # imports game 
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load("assets/background.png")
title = pygame.image.load("assets/logo.png")
pygame.display.set_caption("Menu")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
# The main menu
def mainMenu():
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
                             text_input="PLAY", font=get_font(75), base_color="#fbfdb7", hovering_color="#f8cd78")
        EXIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 450),
                             text_input="QUIT", font=get_font(75), base_color="#fbfdb7", hovering_color="#f8cd78")

        credits_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(1180, 640),
                                text_input="CREDITS", font=get_font(30), base_color="#fbfdb7", hovering_color="#f8cd78")
    
        # changes colour if hover & updates
        credits_button.changeColor(MENU_MOUSE_POS)
        credits_button.update(SCREEN)

        # loops the buttons, changes the colour (based on which is hovered) & updates the display 
        for button in [PLAY_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                 #   displayGameEngine(SCREEN)
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if credits_button.checkForInput(MENU_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                    displayCredits(SCREEN) 
                    pygame.display.set_caption("Menu")


        pygame.display.update()

mainMenu()
