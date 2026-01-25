import pygame
import math

def bounce(x, y):
    global vx, vy, robot_radius, WIDTH, HEIGHT
    if x <= robot_radius or x >= WIDTH - robot_radius:
        vx = -vx
    
    if y <= robot_radius or y >= HEIGHT - robot_radius:
        vy = -vy

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 1: Basic Robot Motion")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Robot state
robot_x = WIDTH // 2  # Start at center
robot_y = HEIGHT // 2
robot_radius = 10

# Velocity commands (pixels per second)
# THIS IS WHAT YOU'LL CHANGE TO EXPERIMENT
vx = 50.0  # pixels/sec to the right
vy = 30.0  # pixels/sec downward

# Simulation parameters
dt = 0.05  # time step in seconds (50ms)
clock = pygame.time.Clock()
FPS = 60

# Trail to visualize path
trail = []

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # UPDATE PHYSICS - This is the core!
    # New position = old position + velocity * time_step
    robot_x += vx * dt
    robot_y += vy * dt

    bounce(robot_x, robot_y)
        
    # Store position for trail
    trail.append((int(robot_x), int(robot_y)))
    
    # Keep only last 500 points to avoid memory issues
    if len(trail) > 500:
        trail.pop(0)
    
    # RENDERING
    screen.fill(WHITE)
    
    # Draw trail
    if len(trail) > 1:
        pygame.draw.lines(screen, BLUE, False, trail, 2)
    
    # Draw robot
    pygame.draw.circle(screen, RED, (int(robot_x), int(robot_y)), robot_radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()