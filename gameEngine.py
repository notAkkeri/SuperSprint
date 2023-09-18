import pygame
import sys
from misc import *
from itemSpawner import *
from pygame.locals import *
from sprite import *

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
        self.hero = Hero(spriteRun, run_frames, jump_frames, hurt_frames)
        pygame.init() 

        # Coin spawner ()
        self.coin_spawner = CoinSpawner(self.SCREEN.get_width(), self.SCREEN.get_height(), self.hero)
        #returns score value
    def get_current_score(self):
        return self.coin_spawner.score

    def run(self):
        #print("entering game")
        self.menu_Theme_music.stop()
        # scores 
        score = 0
        existing_high_score = 0
        current_score = score

        # ct
        current_time = pygame.time.get_ticks()

        # healthy (lives)
        heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))     
        lives = 3
        hearts = [heart_icon] * lives

        # background 
        gameBG = pygame.image.load("assets/gameBG.png")
        bg_x = 0  # Initial x-position of the background
       
        # defining coin  & boulder spawner
        #coin_spawner = CoinSpawner(self.SCREEN.get_width(), self.SCREEN.get_height(), self.hero)
        boulder_spawner = BoulderSpawner(self.SCREEN.get_width(), self.SCREEN.get_height())

        # game loop 
        while self.game_screen:
            self.SCREEN.fill((0, 0, 0))
            pygame.display.set_caption("Super Sprint")

            # background 
            backgroundScroll(gameBG, bg_x, self.SCREEN)
            bg_x = backgroundScroll(gameBG, bg_x, self.SCREEN)
            
            # current game time
            current_time = pygame.time.get_ticks() 
            self.hero.update(current_time)

            # keys
            keys = pygame.key.get_pressed()

            # hero jump cd duration check
            if keys[pygame.K_SPACE]:
                self.hero.jump(current_time)
            # hero state
            is_running = True
            is_jumping = False  
            if keys[pygame.K_SPACE]:
                is_jumping = True
            is_jumping = self.hero.is_jumping
            is_running = not is_jumping  
            is_hurt = False  
            self.hero.is_running = is_running
            self.hero.is_jumping = is_jumping
            self.hero.is_hurt = is_hurt

            # Spawn coins
            for x in range(3):
                self.coin_spawner.spawn_coins()
            
            # coin speed
            self.coin_spawner.update_coins()

            #self.coin_spawner.activate_coin() 
            #Update the CoinSpawner
            #coin_spawner.spawn_coins()
            #coin_spawner.update_coins()

            # Boulder
            boulder_spawner.spawn_boulders()
            boulder_spawner.update()
            for boulder in boulder_spawner.boulders:
                self.SCREEN.blit(boulder.image, boulder.rect)

                # boulder collision
            for i, boulder in enumerate(boulder_spawner.boulders):
                if not boulder.collided and boulder.rect.colliderect(self.hero.rect):
                    boulder.collided = True
                    boulder_spawner.boulders.remove(boulder)
                    if self.hero.health > 0:
                        self.hero.take_damage(1)  
                        hearts.pop()
                        print("Hero collided with a boulder. Health:", self.hero.health)

            # display score 
            score = self.coin_spawner.score  
            drawScore(self.SCREEN, score)
            
            # update hero
            self.hero.update(current_time)

            # Draw the hero character
            self.SCREEN.blit(self.hero.image, self.hero.rect)

            # Draw coins & collection handler
            for coin in self.coin_spawner.coins:
                self.SCREEN.blit(coin.image, coin.rect)
                coin_rect = pygame.Rect(coin.rect.x, coin.rect.y, coin.image.get_width(), coin.image.get_height())
                if coin and not coin.collected:
                    if coin_rect.colliderect(self.hero.rect):
                        coin.collected = True
                        self.coin_spawner.score += coin.value
                        coin.collect()
            
            # heart display
            for i in range(self.hero.health):
                x = self.SCREEN.get_width() - 50 - (i * (heart_icon.get_width() + 5))
                self.SCREEN.blit(heart_icon, (x, 10))

            # go to end screen
            if len(hearts) == 3:
                #print("Game Over")  #  debugging
                self.menu_Theme_music.play()
                current_score = self.get_current_score()
                self.game_state_manager.set_state("end", self.SCREEN, self.game_state_manager, current_score=current_score)
                existing_high_score = 0
                try:
                    with open("Scores/scores.txt", "r") as file:
                        existing_high_score = int(file.readline())
                except FileNotFoundError:
                    pass

                if score > existing_high_score:
                    with open("Scores/scores.txt", "w") as file:
                        file.write(str(score))
                    print("New high score:", score)  # Add this line for debugging
                    current_score = score  
                else:
                    print("Your score:", score)  # Add this line for debugging
                    current_score = score
                    return

            # event handler 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.hero.jump(current_time)
            
                    
            pygame.display.update()
