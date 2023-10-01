import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Continuous Parallax Scrolling')

# Load the background images
bg_images = [pygame.image.load(f'path_to_bg{i}.png') for i in range(1, 6)]  # Replace with actual file paths
bg_width, bg_height = bg_images[0].get_rect().size

# Set initial positions for each background
bg_x = [0, bg_width, bg_width * 2, bg_width * 3, bg_width * 4]

# Set the scrolling speeds for each background
bg_scroll_speeds = [1, 2, 3, 4, 5]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update background positions based on scrolling speeds
    for i in range(len(bg_images)):
        bg_x[i] -= bg_scroll_speeds[i]

        # Check if the image has moved completely off-screen
        if bg_x[i] < -bg_width:
            # Reset the image's position to create a continuous loop
            bg_x[i] += bg_width * len(bg_images)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit the background images
    for i in range(len(bg_images)):
        screen.blit(bg_images[i], (bg_x[i], 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
