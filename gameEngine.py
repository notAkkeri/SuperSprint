<<<<<<< Updated upstream
=======
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

        # Forsaken heart
        self.forsaken_heart = ForsakenHeart(self.SCREEN.get_width(), self.SCREEN.get_height())
        self.forsaken_heart_value = 200
        self.forsaken_heart_restores_life = True
        self.heart_sprites = self.create_heart_sprites()


        # timer
        self.timer = 0
        self.previous_time = pygame.time.get_ticks() 

    def forsaken_heart_collected(self):
        # Check if the hero has 3 hearts
        if self.hero.health == 3:
            self.coin_spawner.score += 200
        else:
            # Otherwise, restore one heart to the hero
            if self.forsaken_heart_restores_life:
                if self.hero.health < 3:
                    self.hero.health += 1


    def format_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"Time: {minutes:02}:{seconds:02}"
    

    def create_heart_sprites(self):
        heart_sprites = []
        spacing = 10  
        heart_width = heart_frames[0].get_width() 
        num_hearts = self.hero.health
        y = -65

        initial_x = self.SCREEN.get_width() - (num_hearts * (heart_width + spacing))

        for i in range(num_hearts):
            x = initial_x + i * (heart_width + spacing)
            heart_sprite = HeartSprite(heart_frames, x, y, scale=0.5)  #
            heart_sprites.append(heart_sprite)

        return heart_sprites

    # Returns score value
    def get_current_score(self):
        return self.coin_spawner.score

    def update_heart_sprites(self):
        for i, heart_sprite in enumerate(self.heart_sprites):
            heart_sprite.update()
            x = 900 - (i * (heart_sprite.rect.width + 2))
            heart_sprite.rect.x = x

        while len(self.heart_sprites) > self.hero.health:
            heart_to_remove = self.heart_sprites.pop()
            # heart_to_remove.kill()
         
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

            # Timer
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.previous_time
            self.previous_time = current_time

            # FPS counter
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
            # hero state & jumping checks 
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

            # fHeart
            self.forsaken_heart.update(current_time)
            # fHeart collection
            if self.hero.rect.colliderect(self.forsaken_heart.rect):
                self.forsaken_heart_collected()
            # draw heart
            self.SCREEN.blit(self.forsaken_heart.image, self.forsaken_heart.rect)


            # spawns the coins 
            for x in range(3):
                self.coin_spawner.spawn_coins()
            
            # coin speed
            self.coin_spawner.update_coins()

            # displays boulder on screen
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
                    crashSFX.play()

            # display  & update scores
            score = self.coin_spawner.score  
            # draw timer
            self.timer += elapsed_time
            drawScore(self.SCREEN, score, self.format_time(self.timer))

            with open("Scores/currentScore.txt", "w") as file:
                file.write(str(score))

            # update sprites 
            self.hero.update(current_time) 
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
            
            # draws & updates hearts 
            for heart_sprite in self.heart_sprites:
                heart_sprite.update()
                self.SCREEN.blit(heart_sprite.image, heart_sprite.rect)

            # go to end screen
            if self.hero.health == 0:
                # stops music 
                if self.game_theme_playing:
                    self.game_Theme_Music.stop()
                    self.game_theme_playing = False
                
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
>>>>>>> Stashed changes
