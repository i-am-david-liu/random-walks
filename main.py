from datetime import datetime
import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define grid dimensions
grid_width, grid_height = 1000, 1000

# Define pixel size 
pixel_size = 2 

# Set up the window
window_width = grid_width * pixel_size
window_height = grid_height * pixel_size
window = pygame.display.set_mode((window_width, window_height))

surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
surface.fill((255, 255, 255))

# Define cell positions
# ! pixel positions are located in (left, top)
cells = []
cell_x = window_width // 2 - pixel_size
cell_y = window_height // 2 - pixel_size

cells.append([cell_x, cell_y, (250, 250, 250)])

#cells.append([cell_x - (pixel_size*200), cell_y + (pixel_size*200), (5, 1, 0)])
#cells.append([cell_x + (pixel_size*200), cell_y + (pixel_size*200), (0, 2, 5)])
#cells.append([cell_x - (pixel_size*200), cell_y - (pixel_size*200), (5, 3, 2)])
#cells.append([cell_x, cell_y, (5, 0, 3)])
#cells.append([cell_x + (pixel_size*200), cell_y - (pixel_size*200), (3, 5, 2)])
#cells.append([cell_x - (pixel_size*50), cell_y + (pixel_size*50), (0, 5, 3)])
#cells.append([cell_x - (pixel_size*50), cell_y + (pixel_size*50), (3, 2, 5)])
#cells.append([cell_x - (pixel_size*50), cell_y - (pixel_size*50), (10, 5, 0)])
#cells.append([cell_x + (pixel_size*50), cell_y + (pixel_size*50), (0, 5, 10)])

# Define movement dictionary
directions = {
        0: (pixel_size, 0),     # right
        1: (0, pixel_size),     # down
        2: (-pixel_size, 0),    # left
        3: (0, -pixel_size)     # up
}

steps = steps_left = 5000000
moving_avg_length = 500
print("Press SPACE to pause, 'q' to quit.")
print("Running {} steps...".format(steps))

running = True
paused = False 
quitting = False
#total_pos = [cell_x, cell_y]
#pos_tracker = []
# animation loop
start_time = time.time()
while running and steps_left > 0:
    # event handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quitting = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused 
                if paused:
                    print("Animation PAUSED.")
                else:
                    print("Animation unpaused.")
            elif event.key == pygame.K_q:
                running = False 
                quitting = True

    if not paused: 
        for i in range(len(cells)):
            cell_x, cell_y, cell_color = cells[i]

            # Draw cell position 
            next_cell_color = surface.get_at((cell_x, cell_y))
            if next_cell_color != pygame.Color(255, 255, 255):
                next_cell_color.r = max(next_cell_color.r - (255 - cell_color[0]), 0)
                next_cell_color.g = max(next_cell_color.g - (255 - cell_color[1]), 0)
                next_cell_color.b = max(next_cell_color.b - (255 - cell_color[2]), 0)
                pygame.draw.rect(
                    surface,
                    next_cell_color,
                    (cell_x, cell_y, pixel_size, pixel_size),
                )
            else:
                pygame.draw.rect(
                    surface,
                    cell_color,
                    (cell_x, cell_y, pixel_size, pixel_size),
                )
            # Draw average position
            """
            if steps - steps_left > moving_avg_length:
                avg_pos_x = total_pos[0] // moving_avg_length
                avg_pos_y = total_pos[1] // moving_avg_length
                pygame.draw.rect(window, (255, 200, 200), (avg_pos_x, avg_pos_y, 2, 2))
                
                total_pos[0] -= pos_tracker[0][0]
                total_pos[1] -= pos_tracker[0][1]
                pos_tracker.pop(0)
            """

            # Update the display
            window.blit(surface, (0, 0))
            pygame.display.flip()

            #time.sleep(0.01)

            # Update cell position
            cell_direction = random.choice( list(directions) )
            cells[i][0] = max(min(cell_x + directions[cell_direction][0], window_width - pixel_size), 0)
            cells[i][1] = max(min(cell_y + directions[cell_direction][1], window_height - pixel_size), 0)

            #total_pos[0] += cell_x
            #total_pos[1] += cell_y
            #pos_tracker.append([cell_x, cell_y])
        
        steps_left -= 1
        if steps_left % (steps // 8) == 0:
            execution_time = time.time() - start_time
            print("{}/{} steps performed. ({:.3f} s)".format(steps - steps_left, steps, execution_time))


if not quitting:
    print("Done! Capturing window as image to current directory...")

    time_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pygame.image.save(window, "imgs/{}.png".format(time_string))

    print("Saved image. Press 'q' to quit.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False 

print("Ending animation...")
pygame.quit()
