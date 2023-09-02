import pygame
import sys
from button import Button  # Assuming you have a Button class in a separate file

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/background.png")
title = pygame.image.load("assets/logo.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Define a function to display credits screen
def displayCredits():
    credits_screen = True

    while credits_screen:
        SCREEN.fill((0, 0, 0))  # Fill the screen with black

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display credits information
        programmers_text = get_font(30).render("Programmers:", True, "#f2faca")
        programmer1_text = get_font(30).render("notAkkeri", True, "#f2faca")
        programmer2_text = get_font(30).render("daScuderiaSha", True, "#f2faca")

        music_text = get_font(30).render("Music:", True, "#f2faca")
        music1_text = get_font(30).render("N/A", True, "#f2faca")
        music2_text = get_font(30).render("N/A", True, "#f2faca")

        assets_text = get_font(30).render("Assets:", True, "#f2faca")
        assets1_text = get_font(30).render("N/A", True, "#f2faca")
        assets2_text = get_font(30).render("N/A", True, "#f2faca")

        open_source_text = get_font(30).render("Open Source project!", True, "#f2faca")
        use_text = get_font(30).render("Feel free to use (just leave credit)", True, "#f2faca")

        back_button = Button(image=pygame.image.load("assets/rect.png"), pos=(20, 640),
                             text_input="BACK", font=get_font(30), base_color="#f2faca", hovering_color="White")

        # Display the text on the credits screen
        SCREEN.blit(programmers_text, (20, 20))
        SCREEN.blit(programmer1_text, (40, 60))
        SCREEN.blit(programmer2_text, (40, 90))

        SCREEN.blit(music_text, (20, 160))
        SCREEN.blit(music1_text, (40, 200))
        SCREEN.blit(music2_text, (40, 230))

        SCREEN.blit(assets_text, (20, 300))
        SCREEN.blit(assets1_text, (40, 340))
        SCREEN.blit(assets2_text, (40, 370))

        SCREEN.blit(open_source_text, (20, 450))
        SCREEN.blit(use_text, (20, 480))

        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    credits_screen = False

        pygame.display.update()

# The main menu
def mainMenu():
    creditsOpen = False

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Title
        title_height = title.get_height()
        screen_height = SCREEN.get_height()

        title_x = (SCREEN.get_width() - title.get_width()) // 2
        title_y = (screen_height - title_height) // 8
        SCREEN.blit(title, (title_x, title_y))

        # Create the "PLAY" and "QUIT" buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 300),
                             text_input="PLAY", font=get_font(75), base_color="#f2faca", hovering_color="White")
        EXIT_BUTTON = Button(image=pygame.image.load("assets/rect.png"), pos=(640, 450),
                             text_input="QUIT", font=get_font(75), base_color="#f2faca", hovering_color="White")

        credits_button = Button(image=pygame.image.load("assets/rectOptions.png"), pos=(1180, 640),
                                text_input="CREDITS", font=get_font(30), base_color="#f2faca", hovering_color="White")

        # Check if the button is clicked
        if credits_button.checkForInput(MENU_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
            displayCredits()  # Show the credits screen

        credits_button.changeColor(MENU_MOUSE_POS)
        credits_button.update(SCREEN)

        # Update and draw the "PLAY" and "QUIT" buttons
        for button in [PLAY_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Calls the play function
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

mainMenu()
