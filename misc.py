import pygame
from pygame.locals import *
from pygame import mixer 
pygame.init()
pygame.mixer.init()

# SFX & Audio # 
coinSFX = pygame.mixer.Sound("assets/sfx/collect.mp3")
coinSFX.set_volume(0.3)
jumpSFX = pygame.mixer.Sound("assets/sfx/jump1.mp3")
jumpSFX.set_volume(0.05)
crashSFX = pygame.mixer.Sound("assets/sfx/crash.mp3")
jumpSFX.set_volume(0.3)
heal1SFX = pygame.mixer.Sound("assets/sfx/heal1.mp3")
heal1SFX.set_volume(0.5)
heal2SFX = pygame.mixer.Sound("assets/sfx/heal2.mp3")
heal2SFX.set_volume(0.5)

# Button/sound  
sound_path = "assets/sfx/click1.mp3"
click_sound = pygame.mixer.Sound(sound_path)
click_sound.set_volume(0.4)

# Menu Theme
menu_theme_sound = None  
def menu_Theme():
    global menu_theme_sound

    if menu_theme_sound is None:
        menu_theme_sound = pygame.mixer.Sound("assets/sfx/menu.mp3")
        menu_theme_sound.set_volume(0.3)
        menu_theme_sound.play()
    
    return menu_theme_sound
# Game Theme
def gameTheme():
    game_theme_sound =  pygame.mixer.Sound("assets/sfx/theme.mp3")
    game_theme_sound.set_volume(0.65)
    game_theme_sound.play()
    return game_theme_sound

# Gameover theme
def gameOverTheme():
    gameOver = pygame.mixer.Sound("assets/sfx/gameOverTheme.mp3")
    gameOver.set_volume(0.2)
    gameOver.play()
    return gameOver


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
def get_font4(size):
    return pygame.font.Font("assets/font4.ttf", size)



# Icons
def get_boulder_icon():
    return pygame.image.load("assets/boulder.png")
def get_forsaken_icon():
    return pygame.image.load("assets/forsakenHeart.png")


# Moving background
def backgroundScroll(bg_image, bg_x, screen, elapsed_time, scroll_speed):
    bg_x -= scroll_speed  
    if bg_x < -bg_image.get_width():
        bg_x = 0
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + bg_image.get_width(), 0))
    return bg_x

# ON SCREEN TEXT #

# score on screen & timer (gameEngine)
def drawScore(SCREEN, score, timer):
    score_text = get_font4(25).render(f"Score: {score}", True, (0, 0, 0))
    timer_text = get_font4(20).render(timer[6:], True, (0, 0, 0)) 
    timer_rect = timer_text.get_rect(topleft=(45, 20))

    SCREEN.blit(score_text, (SCREEN.get_width() // 2 - score_text.get_width() // 2, 20))
    SCREEN.blit(timer_text, timer_rect)

# GAME OVER txt
def drawOver(SCREEN, x, y):
    over_text = get_font3(205).render("GAME OVER!!!", True, (132, 183, 15))
    over_rect = over_text.get_rect(topleft=(x, y))
    SCREEN.blit(over_text, over_rect)

# highscore txt
def drawHighscoreText(screen, text, x, y):
    font = get_font4(45)
    text_surface = font.render(text, True, (240,230,140))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# current score txt
def drawScore2(screen, score, x, y):
    font = get_font4(35)
    score_text = f"Your Score: {score}"
    text_surface = font.render(score_text, True, (250,250,210))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# new HS txt 
def drawNewHS(screen, text, x, y):
    font = get_font4(45)
    text_surface = font.render(text, True, (240,230,140))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)




