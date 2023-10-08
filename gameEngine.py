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

        # time
        self.timer = 0
        self.previous_time = pygame.time.get_ticks()

        #bg 
        self.scroll_speed = 4  #base bg speed 
        self.scroll_speed_increase_interval = 12500 # increase after 12.5 seconds
        self.scroll_speed_increase_timer = pygame.time.get_ticks()

        # forsaken heart
        self.forsaken_heart = ForsakenHeart(self.SCREEN.get_width(), self.SCREEN.get_height(), self.hero)        

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
            heart_sprite = HeartSprite(heart_frames, x, y, scale=0.5)
            heart_sprites.append(heart_sprite)

        return heart_sprites

    def update_heart_sprites(self):
        for i, heart_sprite in enumerate(self.heart_sprites):
            heart_sprite.update()
            x = 900 - (i * (heart_sprite.rect.width + 2))
            heart_sprite.rect.x = x

        while len(self.heart_sprites) > self.hero.health:
            heart_to_remove = self.heart_sprites.pop()

        # Returns score value
    def get_current_score(self):
        return self.hero.score
    
         
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
        boulder_spawner = BoulderSpawner(self.SCREEN.get_width(), self.SCREEN.get_height())



        # game loop 
        while self.game_screen:
            self.SCREEN.fill((0, 0, 0))
            pygame.display.set_caption("Super Sprint")

            # Timer
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.previous_time
            self.previous_time = current_time


            # background 
            bg_x = backgroundScroll(gameBG, bg_x, self.SCREEN, elapsed_time, self.scroll_speed)
            
            # current game time
            current_time = pygame.time.get_ticks() 
            self.hero.update(current_time)

            if elapsed_time >= self.scroll_speed_increase_interval:
                self.scroll_speed += 2  # increase the background speed by 2
                self.scroll_speed_increase_timer = current_time  # reset timer

            # keys
            keys = pygame.key.get_pressed()

            # hero state & jumping checks 
            is_running = True
            is_jumping = False
            is_jumping = self.hero.is_jumping
            is_running = not is_jumping  
            is_hurt = False  
            self.hero.is_running = is_running
            self.hero.is_jumping = is_jumping
            self.hero.is_hurt = is_hurt

                
            # spawns the coins & update
            self.coin_spawner.spawn_coins()
            self.coin_spawner.update_coins()

            for coin in self.coin_spawner.coins:
                if not coin.collected:
                    self.SCREEN.blit(coin.image, coin.rect)
                    
            # boulder collison check
            for boulder in boulder_spawner.boulders:
                boulder.check_collision(self.hero, self.heart_sprites)
            
            # blit boulders on screen
            for boulder in boulder_spawner.boulders:
                self.SCREEN.blit(boulder.image, boulder.rect)

            # display & update boulders
            boulder_spawner.spawn_boulders()
            boulder_spawner.update()

            # display  & update scores
            score = self.hero.score
            # draw timer
            self.timer += elapsed_time
            drawScore(self.SCREEN, score, self.format_time(self.timer))

            # Dispaly, update & draw forsaken hearts
            if self.forsaken_heart:
                self.forsaken_heart.update(current_time)
                if self.hero.rect.colliderect(self.forsaken_heart.rect):
                    self.forsaken_heart.forsaken_heart_collected()  
                    self.forsaken_heart = None
            if self.forsaken_heart:
                self.SCREEN.blit(self.forsaken_heart.image, self.forsaken_heart.rect)

            # open current score file & updates score inside the file
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
            pygame.display.update()
