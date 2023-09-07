import pygame
import sys
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
    
    #Instances
    hero = Hero(SCREEN_HEIGHT)
    coin_spawner = CoinSpawner(SCREEN.get_width(), SCREEN.get_height(), hero)
    boulder_spawner = BoulderSpawner(SCREEN.get_width(), SCREEN.get_height())
  
    
    # game loop 
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

        # Update the CoinSpawner
        coin_spawner.spawn_coins()
        coin_spawner.update_coins()
        hero.update()

        # Boulder
        boulder_spawner.spawn_boulders()
        boulder_spawner.update()

        #collisions
        for boulder in boulder_spawner.boulders:
            boulder.check_collision(hero)
            if boulder.collided:
                boulder_spawner.boulders.remove(boulder)

        # display score 
        score = coin_spawner.score
        drawScore(SCREEN, score)

        # MOVEMENT #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #print("jump success")  
            hero.jump()

        # Draw the hero character
        SCREEN.blit(hero.image, hero.rect)

        # Draw coins & collection handler 
        for coin in coin_spawner.coins:
            SCREEN.blit(coin["image"], (coin["x"], coin["y"]))
            if not coin["collected"]:
                coin_rect = pygame.Rect(coin["x"], coin["y"], coin["image"].get_width(), coin["image"].get_height())
                if hero.rect.colliderect(coin_rect):
                    coin["collected"] = True
                    score += coin["value"]

       
        # Boulder object (spawning)
        for boulder in boulder_spawner.boulders:
            SCREEN.blit(boulder.image, boulder.rect)

        if hero.health == 0:
            print("you have died")

        # event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

    
        # event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
        pygame.display.update()

