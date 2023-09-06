import random
import pygame

#Coin class
class Coin:
    def __init__(self, x, y, coin_type):
        self.x = x
        self.y = y
        self.coin_type = coin_type
        self.creation_time = pygame.time.get_ticks()

    def draw(self, SCREEN):
        SCREEN.blit(self.coin_type, (self.x, self.y))

#Coin spawner  & rarity 
def spawn_coins(coins, width, height, goldCoin, silverCoin, bronzeCoin):
    coin_probabilities = {
        "gold": 0.1, # 10% 
        "silver": 0.25, # 25% 
        "bronze": 0.50 # 50%
    }

    if random.random() < coin_probabilities["gold"]:
        coins.append(Coin(random.randint(0, width - goldCoin.get_width()), random.randint(100, height - goldCoin.get_height()), goldCoin))
    elif random.random() < coin_probabilities["silver"]:
        coins.append(Coin(random.randint(0, width - silverCoin.get_width()), random.randint(100, height - silverCoin.get_height()), silverCoin))
    elif random.random() < coin_probabilities["bronze"]:
        coins.append(Coin(random.randint(0, width - bronzeCoin.get_width()), random.randint(100, height - bronzeCoin.get_height()), bronzeCoin))

#Tracks the global time of the game & how long coin has spawned for 
def coinTime(coins, last_coin_spawn_time, SCREEN, get_gold_icon, get_silver_icon, get_bronze_icon):
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - last_coin_spawn_time

    if time_elapsed >= 50000: 
        spawn_coins(coins, SCREEN.get_width(), SCREEN.get_height(), get_gold_icon(), get_silver_icon(), get_bronze_icon())
        last_coin_spawn_time = current_time

    return last_coin_spawn_time  # Return the updated last_coin_spawn_time

#Despawn coin function 
def despawn_coins(coins, screen_width, screen_height):
    coins_to_remove = []
    current_time = pygame.time.get_ticks()

    for coin in coins:
        # check if coin has been drawn for > 4 seconds 
        if coin.x < 0 or coin.x > screen_width or coin.y < 0 or coin.y > screen_height or (current_time - coin.creation_time) >= 4000:
            coins_to_remove.append(coin)

    # Remove coins that past their spawn counter (later, when character picks them up)
    for coin in coins_to_remove:
        coins.remove(coin)

