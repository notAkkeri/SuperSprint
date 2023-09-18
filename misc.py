import pygame
from pygame.locals import *
from pygame import mixer 
pygame.init()
pygame.mixer.init()

# SFX & Audio # 
coinSFX = pygame.mixer.Sound("assets/sfx/collect.mp3")
coinSFX.set_volume(0.35)
jumpSFX = pygame.mixer.Sound("assets/sfx/jump1.mp3")
jumpSFX.set_volume(0.45)

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

# gameOver background 
endBG = pygame.image.load("assets/backgroundx.png")

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

# score on screen (gameEngine)
def drawScore(SCREEN, score):
    score_text = get_font1(35).render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(SCREEN.get_width() // 2, 20))
    SCREEN.blit(score_text, score_rect)

# GAME OVER txt
def drawOver(SCREEN, x, y):
    over_text = get_font3(205).render("GAME OVER!!!", True, (132, 183, 15))
    over_rect = over_text.get_rect(topleft=(x, y))
    SCREEN.blit(over_text, over_rect)

# draw Hscore (End)
def drawHighscoreText(screen, text, x, y):
    font = get_font(35)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# draw score
def drawScore2(screen, score, x, y):
    font = get_font(35)
    score_text = f"Your Score: {score}"
    text_surface = font.render(score_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)






