import pygame
import sys
import random
from misc import *
from button import Button
from itemSpawner import spawn_coins, Coin, coinTime, despawn_coins

pygame.init()

#global variables 
SCREEN_HEIGHT = 720
last_coin_spawn_time = pygame.time.get_ticks()

# Function to display the game screen
def displayGame(SCREEN):
    global last_coin_spawn_time
    game_screen = True

    # coins
    coins = []
    coinsDelete = []

    # scores 
    score = 0

    # healthy (lives)
    heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))     
    lives = 3

    # background 
    gameBG = pygame.image.load("assets/gameBG.png")
    bg_x = 0  # Initial x-position of the background
    
    # button variables 
    back_to_menu_button = Button(image=pygame.image.load("assets/rect1.png"), pos=(80, 80),
                                 text_input="BACK", font=get_font(30), base_color="#fbfdb7", hovering_color="#f8cd78")
    

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

        # Coin spawning 
        if random.random() < 0.01:
            spawn_coins(coins, SCREEN.get_width(), SCREEN.get_height(), get_gold_icon(), get_silver_icon(), get_bronze_icon())

        # despawn if coin touches void 
        for coin in coins:
            coin.x -= 1  
            if coin.x + coin.coin_type.get_width() < 0:
                coinsDelete.append(coin) 

        # deletes every coin in the delete list 
        for coin in coinsDelete:
            coins.remove(coin)

        # prints coin on the screen 
        for coin in coins:
            coin.draw(SCREEN)
        
        # Despawn check 
        despawn_coins(coins, SCREEN.get_width(), SCREEN.get_height())
        last_coin_spawn_time = coinTime(coins, last_coin_spawn_time, SCREEN, get_gold_icon, get_silver_icon, get_bronze_icon)


        hero.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print("Spacebar pressed")  # Add this line to check if the spacebar is detected
            hero.jump()

        # Draw the hero character
        SCREEN.blit(hero.image, hero.rect)

        # button activation check then goes back to menu (temp) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen = False
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu_button.checkForInput(pygame.mouse.get_pos()):
                    game_screen = False  

        pygame.display.update()

