import pygame
from pygame.locals import *
from misc import jumpSFX 
pygame.init()

# Global constants
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
JUMP_STRENGTH = -7
GRAVITY = 0.075
JUMP_COOLDOWN_DURATION = 850

# sprite sheets
spriteHurt = pygame.image.load("assets/spriteHurt.png")
spriteJump = pygame.image.load("assets/spriteJump.png")
spriteRun = pygame.image.load("assets/spriteRun.png")

# frame dimensions
frame_width_hurt = 200 
frame_height_hurt = 200  
frame_width_jump = 200 
frame_height_jump = 200  
frame_width_run = 200  
frame_height_run = 200 

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
        
        # initial image and rect
        self.image = self.sprite_sheet.subsurface(self.running_frames[0])
        self.rect = self.image.get_rect()
        self.rect.topleft = (150, SCREEN_HEIGHT - frame_height_run)


        # Hero values
        self.velocity_y = 0
        self.coins_collected = 0
        self.radius = self.rect.width // 2
        self.health = 3
        self.score = 0 
        self.heart_sprites = [] 

        self.clock = pygame.time.Clock()

        # jump availability
        self.max_jumps = 1  # max jumps while airborn 
        self.jump_count = 0
        self.can_double_jump = True


        # Create surfaces for each frame
        self.running_surfaces = [self.sprite_sheet.subsurface(frame) for frame in self.running_frames]
        self.jumping_surfaces = [self.sprite_sheet.subsurface(frame) for frame in self.jumping_frames]
        self.hurt_surfaces = [self.sprite_sheet.subsurface(frame) for frame in self.hurt_frames]

        # Create masks for each surface
        self.running_masks = [pygame.mask.from_surface(surface) for surface in self.running_surfaces]
        self.jumping_masks = [pygame.mask.from_surface(surface) for surface in self.jumping_surfaces]
        self.hurt_masks = [pygame.mask.from_surface(surface) for surface in self.hurt_surfaces]

        # initial masks
        self.mask = self.running_masks[0]
        self.hurt_current_frame = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_hurt = True 
            self.hurt_current_frame = 0  

    def jump(self, current_time):
        if self.jump_count < self.max_jumps:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.is_running = False
            self.jump_count += 1
            jumpSFX.play()
        elif self.jump_count == self.max_jumps and self.can_double_jump:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            self.is_running = False
            self.jump_count += 1
            self.can_double_jump = False
            jumpSFX.play()



    def update(self, current_time):
        elapsed_time = self.clock.tick(240) / 1000.0  

        if self.is_hurt:
            self.current_frame += self.hurt_animation_speed * elapsed_time
            if self.current_frame >= len(self.hurt_frames):
                self.is_hurt = False  # trigger ani off after duration
                self.current_frame = 0
            else:
                self.image = self.hurt_surfaces[int(self.current_frame)]
                self.mask = self.hurt_masks[int(self.current_frame)]

        elif self.is_jumping:
            self.current_frame += self.jumping_animation_speed * elapsed_time
            if self.current_frame >= len(self.jumping_frames):
                self.current_frame = len(self.jumping_frames) - 1
            self.image = self.jumping_surfaces[int(self.current_frame)]
            self.mask = self.jumping_masks[int(self.current_frame)]
        elif self.is_running:
            self.current_frame += self.running_animation_speed * elapsed_time
            if self.current_frame >= len(self.running_frames):
                self.current_frame = 0
            self.image = self.running_surfaces[int(self.current_frame)]
            self.mask = self.running_masks[int(self.current_frame)]
        else:
            self.image = self.running_surfaces[0]
            self.mask = self.running_masks[0]

        # gravity 
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # stay on da floor lil bro
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.is_jumping = False
            self.velocity_y = 0
            self.jump_count = 0
            self.can_double_jump = True

    # Collect coin function
    def collect_coin(self, value):
        self.coins_collected += value

heart_frames = [
    pygame.image.load("assets/Hearts/heartSprite_0.png"),
    pygame.image.load("assets/Hearts/heartSprite_1.png"),
    pygame.image.load("assets/Hearts/heartSprite_2.png"),
    pygame.image.load("assets/Hearts/heartSprite_3.png"),
    pygame.image.load("assets/Hearts/heartSprite_4.png"),
    pygame.image.load("assets/Hearts/heartSprite_5.png"),
    pygame.image.load("assets/Hearts/heartSprite_6.png"),
    pygame.image.load("assets/Hearts/heartSprite_7.png"),
    pygame.image.load("assets/Hearts/heartSprite_8.png"),
    pygame.image.load("assets/Hearts/heartSprite_9.png")
]

class HeartSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, scale=3.0):  
        super().__init__()
        self.frames = frames
        self.heart_sprites = []
        self.current_frame = 0
        self.scale = scale  
        self.image = pygame.transform.scale(frames[self.current_frame], (int(frames[self.current_frame].get_width() * scale), int(frames[self.current_frame].get_height() * scale)))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_count = 0
        self.animation_speed = 65
        self.forward = True

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.animation_speed == 0:
            if self.forward:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                if self.current_frame == len(self.frames) - 1:
                    self.forward = False
            else:
                self.current_frame = (self.current_frame - 1) % len(self.frames)
                if self.current_frame == 0:
                    self.forward = True
            self.image = self.frames[self.current_frame]


# init hero sprite (alongside animation & mask)
hero = Hero(spriteRun, run_frames, jump_frames, hurt_frames)
