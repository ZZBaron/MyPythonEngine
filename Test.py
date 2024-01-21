import pygame
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPHERE_RADIUS = 100
WHITE = (255, 255, 255)

# Create the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sphere in 3D Engine")

# Function to project 3D coordinates to 2D screen space
def project(point):
    distance = 200  # Arbitrary distance from the camera
    x, y, z = point
    scale = distance / (distance - z)
    x = int(x * scale + SCREEN_WIDTH / 2)
    y = int(-y * scale + SCREEN_HEIGHT / 2)
    return x, y

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Generate and draw the sphere
    for phi in range(0, 180, 1):
        for theta in range(0, 360, 1):
            x = SPHERE_RADIUS * math.sin(math.radians(phi)) * math.cos(math.radians(theta))
            y = SPHERE_RADIUS * math.sin(math.radians(phi)) * math.sin(math.radians(theta))
            z = SPHERE_RADIUS * math.cos(math.radians(phi))
            point = (x, y, z)
            projected_point = project(point)
            pygame.draw.circle(screen, WHITE, projected_point, 2)

    pygame.display.flip()

# Clean up
pygame.quit()