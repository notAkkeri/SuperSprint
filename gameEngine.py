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
        self.game_Theme_Music = gameTheme() 
        self.menu_Theme_music = menu_Theme()
        self.menu_theme_playing = True  
        self.game_theme_playing = False  
        
        pygame.init() 
        pygame.mixer.init()
        mixer.init()

        # hero init
        self.hero = Hero(spriteRun, run_frames, jump_frames, hurt_frames)
        self.heart_sprites = self.create_heart_sprites()

        # Coin spawner ()
        self.coin_spawner = CoinSpawner(self.SCREEN.get_width(), self.SCREEN.get_height(), self.hero)

    def create_heart_sprites(self):
        heart_sprites = []
        spacing = 2
        heart_width = heart_frames[0].get_width()
        num_hearts = self.hero.health
        initial_x = 900
        y = 10  # Adjust the y-coordinate to align with the score

        for i in range(num_hearts):
            x = initial_x + (i * (heart_width + spacing))
            heart_sprite = HeartSprite(heart_frames, x, y)  
            heart_sprites.append(heart_sprite)

        return heart_sprites

    # Returns score value
    def get_current_score(self):
        return self.coin_spawner.score

    def update_heart_sprites(self):
        for i, heart_sprite in enumerate(self.heart_sprites):
            heart_sprite.update()
            x = 900 + (i * (heart_sprite.rect.width + 2))
            heart_sprite.rect.x = x
            
    def run(self):
        #print("entering game")
        if self.menu_theme_playing:
            self.menu_Theme_music.stop()
            self.menu_theme_playing = False
            print("Menu theme stopped!")

        # Check if the game theme is not playing and start it
        if not self.game_theme_playing:
            self.game_Theme_Music.play()
            self.game_theme_playing = True
            print("Game theme playing")
        # scores 
        score = 0
        existing_high_score = 0
        current_score = score

        # ct
        current_time = pygame.time.get_ticks()

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

            # display score 
            score = self.coin_spawner.score  
            drawScore(self.SCREEN, score)

            # update current scores
            with open("Scores/currentScore.txt", "w") as file:
                file.write(str(score))
            
            # update hero
            self.hero.update(current_time)

            # Update health 
            self.update_heart_sprites() 
            for heart_sprite in self.heart_sprites:
                heart_sprite.update()
                self.SCREEN.blit(heart_sprite.image, heart_sprite.rect)

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
            
            # Update and draw heart sprites
            for heart_sprite in self.heart_sprites:
                heart_sprite.update()
                self.SCREEN.blit(heart_sprite.image, heart_sprite.rect)

            # go to end screen
            if self.hero.health == 0:
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
                    print("New high score:", score)  
                    current_score = score  
                else:
                    print("Your score:", score)  
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
