import math
import numpy as np
import sys

# Parameters
grid_size = 8 # Size of the grid
distance_decay_constant = 0.5 # Decay constant for distance
decay_constant = 0.1 # Decay constant for juice
accumulation_rate = 1 # Juice accumulation rate
max_juice = 100 # Maximum juice level in a region
juice_threshold = 25  # Below this, regions are considered for unloading
juice_at_p0 = 100 # Juice level at player's position
weight_p = 0.70 # Weight of player's proximity effect for juice
weight_l = 0.30 # Weight of player's lingering effect for juice
linger_decay = 0.1 # Fall off rate for lingering juice

# Initialize the grid and player position
grid = np.zeros((grid_size, grid_size))
player_pos = [0, 0]  # Starting at the top-left corner
turns_since_visited = np.full((grid_size, grid_size), np.inf)

def update_juice(pos, elapsed_time=1):
    """Update the juice levels based on player position and interaction."""
    global grid, turns_since_visited
    x, y = pos
    manhattan_distance = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)
    turns_since_visited += 1  # Increment for all regions
    turns_since_visited[x][y] = 0  # Reset for the current position

    # Apply decay to all other regions
    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate manhattan distance to player
            manhattan_dist = manhattan_distance(x, y, i, j)
            proximity_juice = juice_at_p0 * math.exp(- distance_decay_constant * manhattan_dist)
            # Calculate whether player has been in this region before
            if turns_since_visited[i][j] != np.inf:
                elapsed_time = turns_since_visited[i][j]
                exponent = -decay_constant * elapsed_time
                lingering_juice = max_juice * math.exp(exponent)
            else:
                lingering_juice = 0
            total_juice = weight_p * proximity_juice + weight_l * lingering_juice
            grid[i][j] = total_juice
            # print(f"Region ({i}, {j}) juice {grid[i][j]} (distance {manhattan_dist}, proximity_juice {proximity_juice}, lingering_juice {lingering_juice})")
            if grid[i][j] < juice_threshold:
                pass
                # print(f"Region ({i}, {j}) juice {grid[i][j]} below threshold {juice_threshold}, consider unloading")

def print_grid():
    """Print the grid with the player position and juice levels."""
    for i in range(grid_size):
        for j in range(grid_size):
            juice_level = grid[i][j]
            character = "#" if [i, j] != player_pos else "@"
            if juice_level < juice_threshold:
                sys.stdout.write(f"\x1B[38;5;0m{character}\033[0m ")
            elif juice_level > 95:
                sys.stdout.write(f"\033[92m{character}\033[0m ")  # Green
            elif juice_level > 90:
                sys.stdout.write(f"\033[93m{character}\033[0m ")  # Yellow
            elif juice_level > 88:
                sys.stdout.write(f"\x1B[38;5;219m{character}\033[0m ")
            elif juice_level > 86:
                sys.stdout.write(f"\x1B[38;5;218m{character}\033[0m ")
            elif juice_level > 84:
                sys.stdout.write(f"\x1B[38;5;217m{character}\033[0m ")
            elif juice_level > 82:
                sys.stdout.write(f"\x1B[38;5;216m{character}\033[0m ")
            elif juice_level > 80:
                sys.stdout.write(f"\x1B[38;5;215m{character}\033[0m ")
            elif juice_level > 78:
                sys.stdout.write(f"\x1B[38;5;214m{character}\033[0m ")
            elif juice_level > 76:
                sys.stdout.write(f"\x1B[38;5;213m{character}\033[0m ")
            elif juice_level > 74:
                sys.stdout.write(f"\x1B[38;5;212m{character}\033[0m ")
            elif juice_level > 72:
                sys.stdout.write(f"\x1B[38;5;211m{character}\033[0m ")
            elif juice_level > 70:
                sys.stdout.write(f"\x1B[38;5;210m{character}\033[0m ")
            elif juice_level > 68:
                sys.stdout.write(f"\x1B[38;5;209m{character}\033[0m ")
            elif juice_level > 66:
                sys.stdout.write(f"\x1B[38;5;208m{character}\033[0m ")
            elif juice_level > 64:
                sys.stdout.write(f"\x1B[38;5;207m{character}\033[0m ")
            elif juice_level > 62:
                sys.stdout.write(f"\x1B[38;5;206m{character}\033[0m ")
            elif juice_level > 60:
                sys.stdout.write(f"\x1B[38;5;205m{character}\033[0m ")
            elif juice_level > 58:
                sys.stdout.write(f"\x1B[38;5;204m{character}\033[0m ")
            elif juice_level > 56:
                sys.stdout.write(f"\x1B[38;5;203m{character}\033[0m ")
            elif juice_level > 54:
                sys.stdout.write(f"\x1B[38;5;202m{character}\033[0m ")
            elif juice_level > 52:
                sys.stdout.write(f"\x1B[38;5;201m{character}\033[0m ")
            elif juice_level > 50:
                sys.stdout.write(f"\x1B[38;5;200m{character}\033[0m ")
            elif juice_level > 48:
                sys.stdout.write(f"\x1B[38;5;199m{character}\033[0m ")
            elif juice_level > 46:
                sys.stdout.write(f"\x1B[38;5;198m{character}\033[0m ")
            elif juice_level > 44:
                sys.stdout.write(f"\x1B[38;5;197m{character}\033[0m ")
            elif juice_level > 42:
                sys.stdout.write(f"\x1B[38;5;196m{character}\033[0m ")
            elif juice_level > 40:
                sys.stdout.write(f"\x1B[38;5;251m{character}\033[0m ")
            elif juice_level > 38:
                sys.stdout.write(f"\x1B[38;5;250m{character}\033[0m ")
            elif juice_level > 36:
                sys.stdout.write(f"\x1B[38;5;249m{character}\033[0m ")
            elif juice_level > 34:
                sys.stdout.write(f"\x1B[38;5;248m{character}\033[0m ")
            elif juice_level > 32:
                sys.stdout.write(f"\x1B[38;5;247m{character}\033[0m ")
            elif juice_level > 30:
                sys.stdout.write(f"\x1B[38;5;246m{character}\033[0m ")
            elif juice_level > 27:
                sys.stdout.write(f"\x1B[38;5;245m{character}\033[0m ")
            elif juice_level > 24:
                sys.stdout.write(f"\x1B[38;5;244m{character}\033[0m ")
            elif juice_level > 21:
                sys.stdout.write(f"\x1B[38;5;243m{character}\033[0m ")
            elif juice_level > 18:
                sys.stdout.write(f"\x1B[38;5;242m{character}\033[0m ")
            elif juice_level > 15:
                sys.stdout.write(f"\x1B[38;5;241m{character}\033[0m ")
            elif juice_level > 12:
                sys.stdout.write(f"\x1B[38;5;240m{character}\033[0m ")
            elif juice_level > 9:
                sys.stdout.write(f"\x1B[38;5;239m{character}\033[0m ")
            elif juice_level > 6:
                sys.stdout.write(f"\x1B[38;5;238m{character}\033[0m ")
            elif juice_level > 3:
                sys.stdout.write(f"\x1B[38;5;237m{character}\033[0m ")
            else:
                sys.stdout.write(f"\x1B[38;5;236m{character}\033[0m ")
        print()

def move_player(direction):
    """Move the player in the specified direction, if possible."""
    global player_pos, player_history
    new_position = player_pos[:]
    if direction == 'w' and player_pos[0] > 0:
        new_position[0] -= 1
    elif direction == 's' and player_pos[0] < grid_size - 1:
        new_position[0] += 1
    elif direction == 'a' and player_pos[1] > 0:
        new_position[1] -= 1
    elif direction == 'd' and player_pos[1] < grid_size - 1:
        new_position[1] += 1
    elif direction == '.':
        pass
    else:
        print("Cannot move in that direction")
    if new_position != player_pos:
        player_pos = new_position

# Main simulation loop
print("Use 'w', 'a', 's', 'd' to move, '.' to wait, 'q' to quit")
while True:
    update_juice(player_pos)
    print_grid()
    direction = input("Direction: ")
    if direction == 'q':
        break
    move_player(direction)
