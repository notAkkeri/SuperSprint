import pygame
import sys
import random
from misc import *
from itemSpawner import *

pygame.init()

#global variables 
SCREEN_HEIGHT = 720

# Function to display the game screen
def displayGame(SCREEN):
    print("entering game")
    game_screen = True

    # scores 
    score = 0

    # healthy (lives)
    heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))     
    lives = 3

    # background 
    gameBG = pygame.image.load("assets/gameBG.png")
    bg_x = 0  # Initial x-position of the background
    
    # coin spawn instance
    coin_spawner = CoinSpawner(SCREEN.get_width(), SCREEN.get_height())

    hero = Hero(SCREEN_HEIGHT)
    
    # main loop 
    while game_screen:
        SCREEN.fill((0, 0, 0))
        pygame.display.set_caption("Super Sprint")

        # background 
        backgroundScroll(gameBG, bg_x, SCREEN)
        bg_x = backgroundScroll(gameBG, bg_x, SCREEN)

        # Hearts display 
        for i in range(lives):
            x = SCREEN.get_width() - 50 - (i * (heart_icon.get_width() + 5))  
            SCREEN.blit(heart_icon, (x, 10))  

        # Display the score at the top-middle of the screen
        drawScore(SCREEN, score)

        # Update the CoinSpawner
        coin_spawner.spawn_coins()
        coin_spawner.update_coins()

        hero.update()

        # MOVEMENT #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print("jump success")  # Add this line to check if the spacebar is detected
            hero.jump()

        # Draw the hero character
        SCREEN.blit(hero.image, hero.rect)

        for coin in coin_spawner.coins:
            SCREEN.blit(coin["image"], (coin["x"], coin["y"]))

        # button activation check then goes back to menu (temp) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen = False
                sys.exit()  

        pygame.display.update()

