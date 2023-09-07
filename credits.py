import pygame
import sys
from button import Button 
from misc import get_font1
SCREEN_HEIGHT = 720

def displayCredits(SCREEN):
    credits_screen = True 

    while credits_screen:
        SCREEN.fill((0, 0, 0))
        pygame.display.set_caption("Credits")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # displays background image 
        background_image = pygame.image.load("assets/background.png")
        SCREEN.blit(background_image, (0, 0))

        # Display credits information
        programmers_text = get_font1(45).render("Programmers:", True, "#0c0c0c")
        programmer1_text = get_font1(30).render("notAkkeri", True, "#fbfdb7")
        programmer2_text = get_font1(30).render("daScuderiaSha", True, "#fbfdb7")

        music_text = get_font1(45).render("Music:", True, "#0c0c0c")
        music1_text = get_font1(30).render("N/A", True, "#fbfdb7")
        music2_text = get_font1(30).render("N/A", True, "#fbfdb7")

        assets_text = get_font1(45).render("Assets:", True, "#0c0c0c")
        assets1_text = get_font1(30).render("N/A", True, "#fbfdb7")
        assets2_text = get_font1(30).render("N/A", True, "#fbfdb7")

        open_source_text = get_font1(35).render("Open Source project!", True, "#0c0c0c")
        use_text = get_font1(30).render("Feel free to use (just leave credit)", True, "#fbfdb7")

        back_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(80, 640),
                             text_input="BACK", font=get_font1(30), base_color="#fbfdb7", hovering_color="#f8cd78")

        # Display the text on the credits screen
        SCREEN.blit(programmers_text, (440, 20))
        SCREEN.blit(programmer1_text, (440, 60))
        SCREEN.blit(programmer2_text, (440, 90))

        SCREEN.blit(music_text, (440, 160))
        SCREEN.blit(music1_text, (440, 200))
        SCREEN.blit(music2_text, (440, 230))

        SCREEN.blit(assets_text, (440, 300))
        SCREEN.blit(assets1_text, (440, 340))
        SCREEN.blit(assets2_text, (440, 370))

        SCREEN.blit(open_source_text, (440, 450))
        SCREEN.blit(use_text, (440, 480))

        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    credits_screen = False
                    exit  

        pygame.display.update()

