import pygame
from pygame.locals import *
from misc import *
from itemSpawner import *
from sprite import *

class SecondStage:
    def __init__(self, SCREEN, game_state_manager, current_score=0, lives=3):
        self.SCREEN = SCREEN
        self.game_state_manager = game_state_manager
        self.clock = pygame.time.Clock()
        self.SCREEN_HEIGHT = 720
        self.current_score = current_score  
        self.existing_high_score = 0  

        self.lives = lives

        self.heart_icon = pygame.transform.scale(get_heart_icon(), (45, 45))
        self.hearts = [self.heart_icon] * self.lives

    
    #def run(self):