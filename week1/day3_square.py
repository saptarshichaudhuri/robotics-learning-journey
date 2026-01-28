import pygame
import math
import time

start_time = time.time()
current_phase = "straight"  # or "turning"
phase_start_time = time.time()

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
v_left = 50.0  # pixels/sec to the right
v_right = 50.0  # pixels/sec downward
wheelbase = 20.0 # distance between wheels

v = (v_right + v_left) / 2.0 # linear velocity (forward speed)
omega = (v_right - v_left) / wheelbase # angular velocity (turning rate)
TURN_TIME = (math.pi / 2) / (100 / wheelbase)
theta = 0.0 # initial orientation

# Simulation parameters
dt = 0.05  # time step in seconds (50ms)
clock = pygame.time.Clock()
FPS = 60

# Trail to visualize path
trail = []

# Main loop
running = True
sides_completed = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # UPDATE PHYSICS - This is the core!
    # Update pose
    current_time = time.time()
    elapsed_in_phase = current_time - phase_start_time
    
    # Switch behavior based on elapsed time
    if current_phase == "straight" and elapsed_in_phase >= 1:
        # Been going straight for 1 second, now turn
        current_phase = "turning"
        phase_start_time = current_time  
    elif current_phase == "turning" and elapsed_in_phase >= TURN_TIME:
        # Been turning for TURN_TIME seconds, now go straight
        current_phase = "straight"
        phase_start_time = current_time
        sides_completed += 1
        
        if sides_completed >= 40:
            running = False
        
    # Set wheel speeds based on phase
    if current_phase == "straight":
        v_left = 50
        v_right = 50
    elif current_phase == "turning":
        v_left = 50
        v_right = -50
    
    v = (v_right + v_left) / 2.0 # linear velocity (forward speed)
    omega = (v_right - v_left) / wheelbase # angular velocity (turning rate)
    
    robot_x += v * math.cos(theta) * dt
    robot_y += v * math.sin(theta) * dt
    
    theta += omega * dt
    # TURN_TIME = (math.pi / 2) / omega
    
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
    
    # Draw orientation line
    line_length = robot_radius * 2
    end_x = robot_x + line_length * math.cos(theta)
    end_y = robot_y + line_length * math.sin(theta)
    pygame.draw.line(screen, BLACK, (int(robot_x), int(robot_y)), (int(end_x), int(end_y)), 3)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()