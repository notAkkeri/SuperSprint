import pygame
import sys
from button import Button 

def displayCredits(SCREEN):
    credits_screen = True  # Initialize the credits_screen variable

    def get_font(size):
        return pygame.font.Font("assets/font1.ttf", size)

    while credits_screen:
        # Fill the screen with black
        SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Load and display the background image on top of the black screen
        background_image = pygame.image.load("assets/background.png")
        SCREEN.blit(background_image, (0, 0))

        # Display credits information
        programmers_text = get_font(45).render("Programmers:", True, "#0c0c0c")
        programmer1_text = get_font(30).render("notAkkeri", True, "#f2faca")
        programmer2_text = get_font(30).render("daScuderiaSha", True, "#f2faca")

        music_text = get_font(45).render("Music:", True, "#0c0c0c")
        music1_text = get_font(30).render("N/A", True, "#f2faca")
        music2_text = get_font(30).render("N/A", True, "#f2faca")

        assets_text = get_font(45).render("Assets:", True, "#0c0c0c")
        assets1_text = get_font(30).render("N/A", True, "#f2faca")
        assets2_text = get_font(30).render("N/A", True, "#f2faca")

        open_source_text = get_font(35).render("Open Source project!", True, "#0c0c0c")
        use_text = get_font(30).render("Feel free to use (just leave credit)", True, "#f2faca")

        back_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(80, 640),
                             text_input="BACK", font=get_font(30), base_color="#f2faca", hovering_color="White")

        # Display the text on the credits screen
        SCREEN.blit(programmers_text, (540, 20))
        SCREEN.blit(programmer1_text, (540, 60))
        SCREEN.blit(programmer2_text, (540, 90))

        SCREEN.blit(music_text, (540, 160))
        SCREEN.blit(music1_text, (540, 200))
        SCREEN.blit(music2_text, (540, 230))

        SCREEN.blit(assets_text, (540, 300))
        SCREEN.blit(assets1_text, (540, 340))
        SCREEN.blit(assets2_text, (540, 370))

        SCREEN.blit(open_source_text, (540, 450))
        SCREEN.blit(use_text, (540, 480))

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

