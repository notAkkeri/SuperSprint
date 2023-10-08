import random
import pygame
from sprite import *
from misc import coinSFX, crashSFX, get_forsaken_icon
from math import radians

# Point value for coins 
coin_values = {
    "gold": 55,
    "silver": 25,
    "bronze": 5
}

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

# Mask for boulder
boulder_mask = pygame.mask.from_surface(boulderImage)

# ITEMS #

# Coin sprites
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_type, hero):
        super().__init__()
        self.image = coinImages[coin_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collected = False
        self.mask = pygame.mask.from_surface(self.image)
        self.hero = hero
        self.coin_type = coin_type  

    def collect(self):
        coinSFX.play()
        self.collected = True
        self.hero.score += coin_values[self.coin_type]



# coins spawn method and creation
class CoinPool:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coins = []
        self.available_coins = []

    def create_coin(self, x, y, coin_type, hero):
        if len(self.available_coins) > 0:
            coin = self.available_coins.pop()
            coin.rect.topleft = (x, y)
            coin.collected = False
        else:
            coin = Coin(x, y, coin_type, hero)
            self.coins.append(coin)
        return coin

    def despawn_coin(self, coin):
        self.available_coins.append(coin)

# --> New coin spawner <--- #
class CoinSpawner:
    def __init__(self, screen_width, screen_height, hero):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coin_values = coin_values
        self.coin_images = coinImages
        self.coins = []
        self.hero = hero
        self.coin_pool = CoinPool(screen_width, screen_height)
        self.coin_group = pygame.sprite.Group()
        self.last_spawn_time = 0
        self.spawn_interval = 2250 
        self.spawn_pattern = 0

        # Preload 20 coins w/ coin type
        self.preloaded_coins = []
        for _ in range(20):
            coin_type = random.choices(
                ["gold", "silver", "bronze"],
                # rarity
                weights=[0.5, 0.35, 0.6],
                k=1
            )[0]
            coin = self.coin_pool.create_coin(-100, -100, coin_type, hero)
            self.preloaded_coins.append(coin)

    def update_coins(self):
        coins_to_remove = []

        for coin in self.coins:
            coin.rect.x -= 10  # Coin speed

            # Check for collisions with the hero using masks
            if not coin.collected and pygame.sprite.collide_mask(coin, self.hero):
                coin.collect()
                coins_to_remove.append(coin)

            # Remove coin if it goes off-screen
            if coin.rect.x + coin.rect.width < 0 or coin.collected:
                coins_to_remove.append(coin)

        # Remove the coins from the main list
        for coin in coins_to_remove:
            if coin in self.coins:
                self.coins.remove(coin)

    # coin spawner
    def spawn_coins(self):
        coin_probabilities = {
            "gold": 0.1,
            "silver": 0.22,
            "bronze": 0.68
        }
        current_time = pygame.time.get_ticks()  # tracks spawntime
        time_elapsed = current_time - self.last_spawn_time

        # coin spawn choice (single or rows)
        if time_elapsed >= self.spawn_interval:
            self.last_spawn_time = current_time

            if self.spawn_pattern == 0:
                # spawn mixture of coins in a row
                coin_x = self.screen_width
                coin_y = random.randint(100, self.screen_height - coinImages["gold"].get_height())
                num_coins = random.randint(2, 6)  # coin row randomize
                coin_types = random.choices(
                    ["gold", "silver", "bronze"],
                    k=num_coins,
                    weights=[coin_probabilities["gold"], coin_probabilities["silver"], coin_probabilities["bronze"]]
                )
                for coin_type in coin_types:
                    coin = self.coin_pool.create_coin(coin_x, coin_y, coin_type, self.hero)
                    self.coins.append(coin)
                    coin_x += coinImages[coin_type].get_width() + 10
                print(f"Spawned a row of {num_coins} coins with types: {', '.join(coin_types)}.")
                self.spawn_pattern = 1
            else:
                # single coin spawning
                coin_type = random.choices(
                    ["gold", "silver", "bronze"],
                    weights=[coin_probabilities["gold"], coin_probabilities["silver"], coin_probabilities["bronze"]],
                    k=1
                )[0]
                coin_x = self.screen_width
                coin_y = random.randint(100, self.screen_height - coinImages[coin_type].get_height())
                coin = self.coin_pool.create_coin(coin_x, coin_y, coin_type, self.hero)
                self.coins.append(coin)
                print(f"Spawned a {coin_type} coin at ({coin_x}, {coin_y}).")
                self.spawn_pattern = 0
                
    # coin activation 
    def activate_coin(self):
        coin_type = random.choices(
            ["gold", "silver", "bronze"],
            weights=[0.1, 0.22, 0.68],
            k=1
        )[0]

        # coin spawns from the right side of the screen
        coin_x = self.screen_width
        coin_y = random.randint(100, self.screen_height - coinImages[coin_type].get_height())
        coin = self.coin_pool.create_coin(coin_x, coin_y, coin_type, self.hero)
        self.coins.append(coin)
        print(f"Spawned a {coin_type} coin at ({coin_x}, {coin_y})")

# Boulders #

class Boulder(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = boulderImage
        self.collided = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width, screen_height - self.rect.height)
        self.speed = 12  # boulder speed 
        self.collided = False
        self.angle = 0  
        self.rotation_speed = self.speed  
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect.x -= self.speed
        self.rotation_speed = self.speed

        # rotation illusion 
        self.angle += self.rotation_speed
        self.angle %= 360  # Wrap angle within 360 degrees
        self.image = pygame.transform.rotate(boulderImage, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_collision(self, hero, hearts):
        if not self.collided and pygame.sprite.collide_mask(self, hero):
            self.collided = True
            crashSFX.play()
            if pygame.sprite.collide_mask(self, hero):
                self.collided = True
                if hero.health > 0:
                    hero.health -= 1
                    hearts.pop()
                    print(f"Hero has been hit by a boulder !")

    def handle_boulder_collisions(self, hero):
        for boulder in self.boulders:
            boulder.check_collision(hero)

class BoulderSpawner(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boulders = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 8500  # (Spawn CD)
        self.boulder_speed = 12  # starting speed 
        self.speed_increase_timer = 0
        self.speed_increase_interval = 20000 # Increase speed every 25 seconds

    def spawn_boulders(self):
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - self.last_spawn_time

        if time_elapsed >= self.spawn_interval:

            # speed increase every 25 seconds
            self.speed_increase_timer += time_elapsed
            if self.speed_increase_timer >= self.speed_increase_interval:
                self.boulder_speed += 2
                self.speed_increase_timer = 0

            boulder = Boulder(self.screen_width, self.screen_height)
            boulder.speed = self.boulder_speed
            self.boulders.append(boulder)
            self.last_spawn_time = current_time

    def update(self):
        for boulder in self.boulders:
            boulder.update()
        self.boulders = [boulder for boulder in self.boulders if not boulder.collided]


    def draw(self, SCREEN):
        for boulder in self.boulders:
            SCREEN.blit(boulder.image, boulder.rect)

# Forsaken  Heart 
class ForsakenHeart(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, hero, active_forsaken_hearts=None, spawn_interval=None):
        super().__init__()
        self.image = get_forsaken_icon()
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_timer = pygame.time.get_ticks()
        self.collected = False
        self.value = 200
        self.hero = hero
        self.active_forsaken_hearts = active_forsaken_hearts
        self.spawn_interval = spawn_interval  
        self.rect.x = self.screen_width
        self.rect.y = random.randint(50, self.screen_height - self.rect.height - 50)

    def update(self, current_time):
        self.rect.x -= 10  # Movement speed
        if self.rect.right < 0:
            self.rect.x = self.screen_width
            self.rect.y = random.randint(50, self.screen_height - self.rect.height - 50)

    def check_collision(self, hero):
        if not self.collected and pygame.sprite.collide_rect(self, hero):
            self.collect()

    def collect(self):
        if not self.collected:
            self.collected = True
            self.hero.score += self.value  
            if self.hero.health < 3:
                self.hero.health += 1
                if self.hero.health <= 3:
                    lost_heart = self.hero.heart_sprites[-1]
                    x = lost_heart.rect.x
                    new_heart_sprite = HeartSprite(heart_frames, x, lost_heart.rect.y, scale=0.5)
                    self.hero.heart_sprites.insert(-1, new_heart_sprite)

    def forsaken_heart_collected(self):
        if self.hero.health == 3:
            self.hero.score += 200
        else:
            if self.forsaken_heart_restores_life:
                if self.hero.health < 3:
                    self.hero.health += 1
                    # Recovers 1 health if health is less than 3
                    if self.hero.health <= 3:
                        lost_heart = self.hero.heart_sprites[-1] 
                        x = lost_heart.rect.x
                        new_heart_sprite = HeartSprite(heart_frames, x, lost_heart.rect.y, scale=0.5)
                        self.hero.heart_sprites.insert(-1, new_heart_sprite)


    def spawn_forsaken_heart(self):
        y = self.screen_height - self.rect.height
        x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.topleft = (x, y)
        print(f"ForsakenHeart spawned at ({x}, {y})")

