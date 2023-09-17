import pygame
import sys
from misc import *
from itemSpawner import *
from pygame.locals import *
#constants

FRAMERATE = 9999

class GameEngine:
    def __init__(self, SCREEN, game_state_manager):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.game_screen = True
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT = 720
        # Themes
        # game_Theme_Music =  game_theme()
        self.menu_Theme_music = menu_Theme()
        pygame.init() 
    def transition_to_end_screen(self):
        self.game_state_manager.set_state(self.game_state_manager.displayEnd, self.SCREEN, self.game_state_manager)
        
    def run(self):
        #print("entering game")
        self.menu_Theme_music.stop()
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
        hero = Hero(self.SCREEN_HEIGHT)
        coin_spawner = CoinSpawner(self.SCREEN.get_width(), self.SCREEN.get_height(), hero)
        boulder_spawner = BoulderSpawner(self.SCREEN.get_width(), self.SCREEN.get_height())
    
        # game loop 
        while self.game_screen:
            self.SCREEN.fill((0, 0, 0))
            pygame.display.set_caption("Super Sprint")

            # Frame rate
            self.clock.tick(FRAMERATE)

            # background 
            backgroundScroll(gameBG, bg_x, self.SCREEN)
            bg_x = backgroundScroll(gameBG, bg_x, self.SCREEN)

            # heart display
            for i in range(hero.health):
                x = self.SCREEN.get_width() - 50 - (i * (heart_icon.get_width() + 5))
                self.SCREEN.blit(heart_icon, (x, 10))

            # Update the CoinSpawner
            coin_spawner.spawn_coins()
            coin_spawner.update_coins()
            hero.update()

            # Boulder
            boulder_spawner.spawn_boulders()
            boulder_spawner.update()
            for boulder in boulder_spawner.boulders:
                self.SCREEN.blit(boulder.image, boulder.rect)

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
            drawScore(self.SCREEN, score)

            # MOVEMENT #
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                #print("jump success")  
                hero.jump()

            # Draw the hero character
            self.SCREEN.blit(hero.image, hero.rect)

            # Draw coins & collection handler 
            for coin in coin_spawner.coins:
                self.SCREEN.blit(coin.image, (coin.rect.x, coin.rect.y))
                coin_rect = pygame.Rect(coin.rect.x, coin.rect.y, coin.image.get_width(), coin.image.get_height())
                if not coin.collected:
                    if coin_rect.colliderect(hero.rect):
                        coin.collected = True
                        coin_spawner.score += coin.value
                        #print(f"Collected {coin.image} coin, It's worth {coin.value} points!")
            # Display score
            score = coin_spawner.score
            drawScore(self.SCREEN, score)
            
  
            if len(hearts) == 0:
                #print("Game Over")
                self.menu_Theme_music.play()
                self.game_state_manager.set_state("end", self.SCREEN, self.game_state_manager)
                return



            # event handler 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                    
            pygame.display.update()
