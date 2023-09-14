import pygame
import sys
from button import Button
from misc import get_font, get_font1, click_sound

SCREEN_HEIGHT = 720

def displayCredits(SCREEN):
    credits_screen = True

    while credits_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    click_sound.play()
                    credits_screen = False
                    break  # Back to menu if button press

        SCREEN.fill((0, 0, 0))
        pygame.display.set_caption("Credits")

        # displays background image
        background_image = pygame.image.load("assets/background.png")
        SCREEN.blit(background_image, (0, 0))

        # Text dict
        categories = [
            ("Programmers:", ["notAkkeri", "daScuderiaSha"]),
            ("Contributors:", ["A", "B", "C"]),
            ("Open Source project!", ["Feel free to use, all relevant credit is shown here."])
        ]

        y_position = 20  

        for category, subheadings in categories:
            # headings
            heading_text = get_font1(65).render(category, True, "#0c0c0c")
            SCREEN.blit(heading_text, (440, y_position))
            y_position += 65 

            # subheadings
            for subheading in subheadings:
                subheading_text = get_font1(50).render(subheading, True, "#fbfdb7")
                SCREEN.blit(subheading_text, (440, y_position))
                y_position += 55  

        back_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(80, 640),
                            text_input="BACK", font=get_font(30), base_color="#fbfdb7", hovering_color="#f8cd78",
                            click_sound=click_sound)

        back_button.changeColor(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        pygame.display.update()
