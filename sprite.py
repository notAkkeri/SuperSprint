import pygame
from pygame.locals import *
from misc import jumpSFX 
pygame.init()

# Global constants
SCREEN_HEIGHT = 720
JUMP_STRENGTH = -12.25
GRAVITY = 0.135
JUMP_COOLDOWN_DURATION = 850

# Load sprite sheets
spriteHurt = pygame.image.load("assets/spriteHurt.png")
spriteJump = pygame.image.load("assets/spriteJump.png")
spriteRun = pygame.image.load("assets/spriteRun.png")

# Define frame dimensions
frame_width_hurt = 128  
frame_height_hurt = 128  
frame_width_jump = 128  
frame_height_jump = 128  
frame_width_run = 128  
frame_height_run = 128  

# animation frames 
hurt_frames = [pygame.Rect(i * frame_width_hurt, 0, frame_width_hurt, frame_height_hurt) for i in range(3)]
jump_frames = [pygame.Rect(i * frame_width_jump, 0, frame_width_jump, frame_height_jump) for i in range(6)]
run_frames = [pygame.Rect(i * frame_width_run, 0, frame_width_run, frame_height_run) for i in range(6)]
class Hero(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, running_frames, jumping_frames, hurt_frames):
        super().__init__()

        # sprite sheet
        self.sprite_sheet = sprite_sheet
        self.running_frames = running_frames
        self.jumping_frames = jumping_frames
        self.hurt_frames = hurt_frames

        # current frame index and animation speed
        self.current_frame = 0

        # hurt variables anis
        self.hurt_frames = hurt_frames
        self.hurt_current_frame = 0

        # animation control states
        self.is_running = False
        self.is_jumping = False
        self.is_hurt = False

        # animation timers and speeds (seconds)
        self.running_animation_speed = 7  # RUNNING
        self.jumping_animation_speed = 20  # JUMPING
        self.hurt_animation_speed = 1  # HIT
        
        # Set the initial image and rect
        self.image = self.sprite_sheet.subsurface(self.running_frames[0])
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, SCREEN_HEIGHT - frame_height_run - 250)

        # Hero values
        self.velocity_y = 0
        self.coins_collected = 0
        self.radius = self.rect.width // 2
        self.health = 3
        self.jumpCD = 0

        self.clock = pygame.time.Clock()

        # jump availability
        self.jump_available = True

        # Additional hurt animation frames and state
        self.hurt_current_frame = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_hurt = True  # Set the hurt animation flag
            self.hurt_current_frame = 0  # Reset the hurt animation frame

    def jump(self, current_time):
        if not self.is_jumping and self.jump_available:  # Check if jump is available
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.is_running = False 
            self.jump_available = False  # Jump is not available during cooldown
            self.jump_start_time = pygame.time.get_ticks()  # Record jump start time
            jumpSFX.play()

    def update(self, current_time):
        elapsed_time = self.clock.tick(240) / 1000.0  

        if self.is_hurt:
            self.current_frame += self.hurt_animation_speed * elapsed_time
            if self.current_frame >= len(self.hurt_frames):
                self.is_hurt = False  # trigger ani off after duration
                self.current_frame = 0
            else:
                self.image = self.sprite_sheet.subsurface(self.hurt_frames[int(self.current_frame)])

        elif self.is_jumping:
            self.current_frame += self.jumping_animation_speed * elapsed_time
            if self.current_frame >= len(self.jumping_frames):
                self.current_frame = len(self.jumping_frames) - 1
            self.image = self.sprite_sheet.subsurface(self.jumping_frames[int(self.current_frame)])
        elif self.is_running:
            self.current_frame += self.running_animation_speed * elapsed_time
            if self.current_frame >= len(self.running_frames):
                self.current_frame = 0
            self.image = self.sprite_sheet.subsurface(self.running_frames[int(self.current_frame)])
        else:
            self.image = self.sprite_sheet.subsurface(self.running_frames[0])

        # cd check
        if not self.jump_available:
            if current_time - self.jump_start_time >= JUMP_COOLDOWN_DURATION:
                self.jump_available = True        

        # game phys
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        #  stay on floor lil bro
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0

        # jump cd
        if current_time - self.jumpCD >= JUMP_COOLDOWN_DURATION:
            self.is_jumping = False

    # Collect coin function
    def collect_coin(self, value):
        self.coins_collected += value


# Define what the Hero class is
hero = Hero(spriteRun, run_frames, jump_frames, hurt_frames)
