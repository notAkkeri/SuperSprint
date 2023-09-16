import pygame
from pygame.locals import *
from pygame import mixer 
pygame.init()
pygame.mixer.init()

# SFX & Audio # 

# Button/sound  
sound_path = "assets/sfx/click1.mp3"
click_sound = pygame.mixer.Sound(sound_path)
click_sound.set_volume(0.45)

# Menu Theme
def menu_Theme():
    mixer.init()
    mixer.music.load("assets/sfx/menu.mp3")
    mixer.music.play()
    pygame.mixer.music.set_volume(0.3)
    return mixer.music

def stop_menu_music(self):
    self.menu_Theme_music.stop()


# MISC # 

# game logo
title = pygame.image.load("assets/logo.png")

# Fonts 
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
def get_font1(size):
    return pygame.font.Font("assets/font1.ttf", size)
def get_font2(size):
    return pygame.font.Font("assets/font2.ttf", size)
def get_font3(size):
    return pygame.font.Font("assets/font3.ttf", size)


# Icons
def get_heart_icon():
    return pygame.image.load("assets/heartIcon.png")
def get_boulder_icon():
    return pygame.image.load("assets/boulder.png")

# Moving background
def backgroundScroll(bg_image, bg_x, screen):
    bg_x -= 1 
    if bg_x < -bg_image.get_width():
        bg_x = 0
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + bg_image.get_width(), 0))
    return bg_x 

# Score on screen
def drawScore(SCREEN, score):
    score_text = get_font1(35).render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(SCREEN.get_width() // 2, 20))
    SCREEN.blit(score_text, score_rect)

def drawOver(SCREEN, x, y):
    over_text = get_font3(205).render("GAME OVER!!!", True, (132, 183, 15))
    over_rect = over_text.get_rect(topleft=(x, y))
    SCREEN.blit(over_text, over_rect)


# CHARACTER # 

#Goobal variables 
SCREEN_HEIGHT = 720
JUMP_STRENGTH = -11
GRAVITY = 0.1

# hero class
class Hero(pygame.sprite.Sprite):
    def __init__(self, screen_height):
        super().__init__()
        self.image = pygame.image.load("assets/hero.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, screen_height - self.rect.height - 250)
        self.velocity_y = 0
        self.is_jumping = False
        self.coins_collected = 0
        self.radius = self.rect.width // 2
        self.health = 3

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def update(self):
        # gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Keep the character on the ground 
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0

    # jump function 
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

   # increases number of coins collected by char then updates 
    def collect_coin(self, value):
        self.coins_collected += value






