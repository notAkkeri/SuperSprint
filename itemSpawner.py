import random
import pygame

# Settings #
coin_values = {
    "gold": 3,
    "silver": 2,
    "bronze": 1
}

# Load images
coinImages = {
    "gold": pygame.image.load("assets/goldCoin.png"),
    "silver": pygame.image.load("assets/silverCoin.png"),
    "bronze": pygame.image.load("assets/bronzeCoin.png")
}

class CoinSpawner:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.coin_values = coin_values
        self.coin_images = coinImages  # Removed the parentheses here
        self.coins = []
        self.last_spawn_time = pygame.time.get_ticks()  # Initialize with current time

    def spawn_coins(self):
        coin_probabilities = {
            "gold": 0.05,
            "silver": 0.15,
            "bronze": 0.80
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

    def update_coins(self):
        coins_to_remove = []

        for coin in self.coins:
            coin["x"] -= 3  # Adjust the speed if needed
            if coin["x"] + coin["image"].get_width() < 0 or coin["collected"]:
                coins_to_remove.append(coin)

        for coin in coins_to_remove:
            self.coins.remove(coin)
