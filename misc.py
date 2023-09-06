import pygame

# MISC # 

def get_heart_icon():
    return pygame.image.load("assets/heartIcon.png")

def get_gold_icon():
    return pygame.image.load("assets/goldCoin.png")

def get_silver_icon():
    return pygame.image.load("assets/silverCoin.png")

def get_bronze_icon():
    return pygame.image.load("assets/bronzeCoin.png")

def get_font(size):
    return pygame.font.Font("assets/font1.ttf", size)

def backgroundScroll(bg_image, bg_x, screen):
    bg_x -= 1 
    if bg_x < -bg_image.get_width():
        bg_x = 0
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + bg_image.get_width(), 0))
    return bg_x 

def drawScore(SCREEN, score):
    score_text = get_font(24).render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN.get_width() // 2, 20))
    SCREEN.blit(score_text, score_rect)

# CHARACTER # 
SCREEN_HEIGHT = 720
JUMP_STRENGTH = -11
GRAVITY = 0.1
class Hero(pygame.sprite.Sprite):
    def __init__(self, screen_height):
        super().__init__()
        self.image = pygame.image.load("assets/hero.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, screen_height - self.rect.height - 250)
        self.velocity_y = 0
        self.is_jumping = False
        self.coins_collected = 0

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Keep the character on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True

    def collect_coin(self):
        self.coins_collected += 1


