import pygame
from pygame.locals import *
from pygame import mixer 
pygame.init()
pygame.mixer.init()

# Audio Channels
sfxChannel0 = pygame.mixer.Channel(0) # multi use channel
sfxChannel1 = pygame.mixer.Channel(1) # unique channel
sfxChannel2 = pygame.mixer.Channel(2) # unique channel
sfxChannel3 = pygame.mixer.Channel(3) # unique channel
themesChannel1 = pygame.mixer.Channel(4) 
themesChannel2 = pygame.mixer.Channel(5)
themesChannel3 = pygame.mixer.Channel(6) 
# SFX #

# Sound Effects

 # Coin Collect
# Coin Collect
coinSFX = pygame.mixer.Sound("assets/sfx/collect.mp3")
coinSFX.set_volume(0.4)
def playCoinSFX():
    pygame.mixer.Channel(1).stop()
    pygame.mixer.Channel(1).play(coinSFX)
    return coinSFX

# Jumping
jumpSFX = pygame.mixer.Sound("assets/sfx/jump1.mp3")
jumpSFX.set_volume(0.25)
def playJumpSFX():
    pygame.mixer.Channel(2).stop()
    pygame.mixer.Channel(2).play(jumpSFX)
    return jumpSFX

# Boulder collide
crashSFX = pygame.mixer.Sound("assets/sfx/crash.mp3")
crashSFX.set_volume(0.1)
def playCrashSFX():
    pygame.mixer.Channel(3).stop()
    pygame.mixer.Channel(3).play(crashSFX)
    return crashSFX

# Forsaken heart (when max lives)
heal1SFX = pygame.mixer.Sound("assets/sfx/heal1.mp3")
heal1SFX.set_volume(0.5)
def playHeal1SFX():
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(0).play(heal1SFX)
    return heal1SFX

# Forsaken heart (when health restored)
heal2SFX = pygame.mixer.Sound("assets/sfx/heal2.mp3")
heal2SFX.set_volume(0.5)
def playHeal2SFX():
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(0).play(heal2SFX)
    return heal2SFX

# Buttons SFX
click_sound = pygame.mixer.Sound("assets/sfx/click1.mp3")
click_sound.set_volume(0.3)
def playClickSound():
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(0).play(click_sound)
    return click_sound

# Themes #

# Menu theme
menu_theme_sound = pygame.mixer.Sound("assets/sfx/menu.mp3")
menu_theme_sound.set_volume(0.4)
def menu_Theme():
    themesChannel1.play(menu_theme_sound)
    return menu_theme_sound

# Game Theme
game_theme_sound = pygame.mixer.Sound("assets/sfx/theme.mp3")
game_theme_sound.set_volume(0.4)
def gameTheme():
    themesChannel2.play(game_theme_sound)
    return game_theme_sound

# Gameover theme
gameOver = pygame.mixer.Sound("assets/sfx/gameOverTheme.mp3")
gameOver.set_volume(0.25)
def gameOverTheme():
    themesChannel3.play(gameOver)
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




