import random
import pygame
from misc import Hero

# Point value for coins 
coin_values = {
    "gold": 55,
    "silver": 10,
    "bronze": 5
}

# Collection range 
COLLISION_MARGIN = 10

# Load images
def load_images():
    coin_images = {
        "gold": pygame.image.load("assets/goldCoin.png"),
        "silver": pygame.image.load("assets/silverCoin.png"),
        "bronze": pygame.image.load("assets/bronzeCoin.png"),
    }
    boulder_image = pygame.image.load("assets/boulder.png")
    return coin_images, boulder_image

coinImages, boulderImage = load_images()

# ITEMS #

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_type, value):
        super().__init__()
        self.image = coinImages[coin_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collected = False
        self.value = value

class CoinPool:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coins = []
        self.available_coins = []

    def create_coin(self, x, y, coin_type, value):
        if len(self.available_coins) > 0:
            coin = self.available_coins.pop()
            coin.rect.topleft = (x, y)
            coin.collected = False
            coin.value = value
        else:
            coin = Coin(x, y, coin_type, value)
            self.coins.append(coin)
        return coin

    def despawn_coin(self, coin):
        self.available_coins.append(coin)

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
        self.coin_pool = CoinPool(screen_width, screen_height)

    def spawn_coins(self):
        coin_probabilities = {
            "gold": 0.08,
            "silver": 0.20,
            "bronze": 0.72
        }
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        time_elapsed = current_time - self.last_spawn_time

        if time_elapsed >= 850:  # Spawn coins every 850 milliseconds
            for coin_type, probability in coin_probabilities.items():
                if random.random() < probability:
                    coin_x = self.screen_width
                    coin_y = random.randint(100, self.screen_height - coinImages[coin_type].get_height())
                    coin_value = coin_values.get(coin_type, 0)
                    coin = self.coin_pool.create_coin(coin_x, coin_y, coin_type, coin_value)
                    self.coins.append(coin)
            self.last_spawn_time = current_time

# Update coins (spawning)
    def update_coins(self):
        coins_to_remove = []

        for coin in self.coins:
            coin.rect.x -= 3  # coin movement speed
            if coin.rect.x + coin.rect.width < 0 or coin.collected:
                coins_to_remove.append(coin)
                self.coin_pool.despawn_coin(coin)
            else:
                coin_rect = pygame.Rect(
                    coin.rect.x - COLLISION_MARGIN, 
                    coin.rect.y - COLLISION_MARGIN, 
                    coin.rect.width + 2 * COLLISION_MARGIN, 
                    coin.rect.height + 2 * COLLISION_MARGIN
                )
                if not coin.collected and self.hero.rect.colliderect(coin_rect):
                    coin.collected = True
                    self.score += coin.value
                    print(f"Collected {coin.image} coin, It's worth {coin.value} points!")
                    
        for coin in coins_to_remove: 
            self.coins.remove(coin)

# Boulders #

class Boulder(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = boulderImage
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width, screen_height - self.rect.height)
        self.speed = 5  # movement speed of boulder
        self.collided = False

    def update(self):
        self.rect.x -= self.speed

    def check_collision(self, hero, hearts):
        if not self.collided and self.rect.colliderect(hero.rect):
            self.collided = True
            if hero.health > 0:  # Check if hero has health left
                hero.health -= 1  # Decrement hero's health
                hearts.pop()  # Remove one heart icon from the list

class BoulderSpawner(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boulders = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 5500  # spawn cooldown (1000 = 1 second)

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


