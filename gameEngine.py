import pygame
import sys
import random
from button import Button
from itemSpawner import spawn_coins, Coin, coinTime, despawn_coins

pygame.init()

def get_font(size):
    return pygame.font.Font("assets/font1.ttf", size)

def get_heart_icon():
    return pygame.image.load("assets/heartIcon.png")

def get_gold_icon():
    return pygame.image.load("assets/goldCoin.png")

def get_silver_icon():
    return pygame.image.load("assets/silverCoin.png")

def get_bronze_icon():
    return pygame.image.load("assets/bronzeCoin.png")


last_coin_spawn_time = pygame.time.get_ticks()

# Function to display the game screen
def displayGame(SCREEN):
    global last_coin_spawn_time
    game_screen = True 

    # coins
    coins = []

    #scores 
    score = 0

    # healthy (lives)
    heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))     
    lives = 3

    #background 
    gameBG = pygame.image.load("assets/gameBG.png")
    bg_x = 0  # Initial x-position of the background

   # button variables 
    back_to_menu_button = Button(image=pygame.image.load("assets/rect.png"), pos=(80, 640),
                                 text_input="BACK", font=get_font(30), base_color="#fbfdb7", hovering_color="#f8cd78")
    
    # main loop 
    while game_screen:
        SCREEN.fill((0, 0, 0))
        pygame.display.set_caption("Super Sprint")

        # draws & generates background  
            # works by constantly updating position of the background with each frame in the loop (gives the appearence of consitently moving)
        bg_x -= 1  # Speed of background moving 
        if bg_x < -gameBG.get_width():
            bg_x = 0  
        SCREEN.blit(gameBG, (bg_x, 0))
        SCREEN.blit(gameBG, (bg_x + gameBG.get_width(), 0))
        
        # Hearts display 
        for i in range(lives):
            x = SCREEN.get_width() - 50 - (i * (heart_icon.get_width() + 5))  
            SCREEN.blit(heart_icon, (x, 10))  

        # Display the score at the top-middle of the screen
        score_text = get_font(24).render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN.get_width() // 2, 20))
        SCREEN.blit(score_text, score_rect)


        # Coin spawning 
        if random.random() < 0.01:  
            spawn_coins(coins, SCREEN.get_width(), SCREEN.get_height(), get_gold_icon(), get_silver_icon(), get_bronze_icon())
        # coin draw 
        for coin in coins:
            coin.draw(SCREEN)
        
        # Despawn check 
        despawn_coins(coins, SCREEN.get_width(), SCREEN.get_height())
        last_coin_spawn_time = coinTime(coins, last_coin_spawn_time, SCREEN, get_gold_icon, get_silver_icon, get_bronze_icon)


        # menu button 
        back_to_menu_button.changeColor(pygame.mouse.get_pos())
        back_to_menu_button.update(SCREEN)

        # button activation check then goes back to menu 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen = False
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_menu_button.checkForInput(pygame.mouse.get_pos()):
                    game_screen = False  

        pygame.display.update()

