import pygame
import sys
from misc import *
from itemSpawner import *
from endScreen import *
clock = pygame.time.Clock()

pygame.init()

#global variables 
SCREEN_HEIGHT = 720

# Themes

# game_Theme_Music =  game_theme()
menu_Theme_music = menu_Theme()

# Function to display the game screen
def displayGame(SCREEN):
    print("entering game")
    game_screen = True

    # scores 
    score = 0

    # healthy (lives)
    heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))     
    lives = 3
    hearts = [heart_icon] * lives

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

        # Frame rate
        clock.tick(4500)

        # background 
        backgroundScroll(gameBG, bg_x, SCREEN)
        bg_x = backgroundScroll(gameBG, bg_x, SCREEN)

        # heart display
        for i in range(hero.health):
            x = SCREEN.get_width() - 50 - (i * (heart_icon.get_width() + 5))
            SCREEN.blit(heart_icon, (x, 10))

        # Update the CoinSpawner
        coin_spawner.spawn_coins()
        coin_spawner.update_coins()
        hero.update()

        # Boulder
        boulder_spawner.spawn_boulders()
        boulder_spawner.update()
        for boulder in boulder_spawner.boulders:
            SCREEN.blit(boulder.image, boulder.rect)

        # boulder collision
        for i, boulder in enumerate(boulder_spawner.boulders):
            if not boulder.collided and boulder.rect.colliderect(hero.rect):
                boulder.collided = True
                boulder_spawner.boulders.remove(boulder)
                if hero.health > 0:  
                    hero.health -= 1  
                    hearts.pop()

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
            SCREEN.blit(coin.image, (coin.rect.x, coin.rect.y))

            coin_rect = pygame.Rect(coin.rect.x, coin.rect.y, coin.image.get_width(), coin.image.get_height())
            if not coin.collected:
                if coin_rect.colliderect(hero.rect):
                    coin.collected = True
                    coin_spawner.score += coin.value
                    print(f"Collected {coin.image} coin, It's worth {coin.value} points!")

    
            # Display score
        score = coin_spawner.score
        drawScore(SCREEN, score)

        # Check if the game is over
        if len(hearts) == 0:
            print("Game Over")
            # displayEnd(SCREEN)
            menu_Theme_music.play()
            game_screen = False

        # event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
                
        pygame.display.update()

