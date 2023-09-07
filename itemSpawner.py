import random
import pygame
from misc import Hero

# Point value for coins 
coin_values = {
    "gold": 15,
    "silver": 5,
    "bronze": 1
}

# Collection range 
COLLISION_MARGIN = 10

# Load images
coinImages = {
    "gold": pygame.image.load("assets/goldCoin.png"),
    "silver": pygame.image.load("assets/silverCoin.png"),
    "bronze": pygame.image.load("assets/bronzeCoin.png")
}

# ITEMS #

# Coin spawning logic 
class CoinSpawner:
    def __init__(self, screen_width, screen_height, hero):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coin_values = coin_values
        self.coin_images = coinImages  
        self.coins = []
        self.last_spawn_time = pygame.time.get_ticks()  # Initialize with current time
        self.hero = hero
        self.score = 0 

    def spawn_coins(self):
        coin_probabilities = {
            "gold": 0.08,
            "silver": 0.20,
            "bronze": 0.72
        }
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        time_elapsed = current_time - self.last_spawn_time

        if time_elapsed >= 500:  # Spawn coins every 1000 milliseconds (1 second)
            for coin_type, probability in coin_probabilities.items():
                if random.random() < probability:
                    coin_image = self.coin_images.get(coin_type)  
                    if coin_image:
                        coin_x = self.screen_width
                        coin_y = random.randint(100, self.screen_height - coin_image.get_height())
                        coin = {
                            "x": coin_x,
                            "y": coin_y,
                            "type": coin_type,
                            "image": coin_image,
                            "value": coin_values.get(coin_type, 0),
                            "collected": False
                        }
                        self.coins.append(coin)
            self.last_spawn_time = current_time

# Update coins (spawning)
    def update_coins(self):
        coins_to_remove = []

        for coin in self.coins:
            coin["x"] -= 2.5  # coin movement speed
            if coin["x"] + coin["image"].get_width() < 0 or coin["collected"]:
                coins_to_remove.append(coin)
            else:
                coin_rect = pygame.Rect(coin["x"] - COLLISION_MARGIN, coin["y"] - COLLISION_MARGIN, coin["image"].get_width() + 2 * COLLISION_MARGIN, coin["image"].get_height() + 2 * COLLISION_MARGIN)
                if not coin["collected"] and self.hero.rect.colliderect(coin_rect):
                    coin["collected"] = True
                    self.score += coin["value"]
                    print(f"Collected {coin['type']} coin, It's worth {coin['value']} points!")
                    
        for coin in coins_to_remove:
            self.coins.remove(coin)

# Boulders #

class Boulder(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("assets/boulder.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width, screen_height - self.rect.height)
        self.speed = 7 # movement speed of boulder
        self.collided = False

    def update(self):
        self.rect.x -= self.speed

    def check_collision(self, hero):
       if not self.collided and self.rect.colliderect(hero.rect):
            self.collided = True

class BoulderSpawner(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boulders = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 10000  # spawn cooldown

    def spawn_boulders(self):
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_spawn_time

        if time_elapsed >= self.spawn_interval:
            boulder = Boulder(self.screen_width, self.screen_height)
            self.boulders.append(boulder)
            self.last_spawn_time = current_time

    def update(self):
        for boulder in self.boulders:
            boulder.update()
        self.boulders = [boulder for boulder in self.boulders if boulder.rect.right > -100]

    def draw(self, SCREEN):
        for boulder in self.boulders:
            SCREEN.blit(boulder.image, boulder.rect)


