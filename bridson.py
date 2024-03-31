import math
import random

def poisson_disc_sampler(width, height, radius, k=30):
    """
    Generate points using Bridson's algorithm for Poisson Disk Sampling.

    Parameters:
    width (int): The width of the area.
    height (int): The height of the area.
    radius (float): The minimum distance between points.
    k (int): The number of samples to consider before rejection.

    Returns:
    Generator yielding points (x, y).
    """
    # Cell side length
    cell_size = radius / math.sqrt(2)
    grid_width = math.ceil(width / cell_size)
    grid_height = math.ceil(height / cell_size)

    # Grid initialization
    grid = [None for _ in range(grid_width * grid_height)]
    queue = []
    samples = []

    # Helper function to get grid index
    def get_grid_index(x, y):
        return int(x / cell_size) + int(y / cell_size) * grid_width

    # Helper function to check if a point is far enough from others
    def far(x, y):
        grid_x, grid_y = int(x / cell_size), int(y / cell_size)
        for i in range(max(grid_x - 2, 0), min(grid_x + 3, grid_width)):
            for j in range(max(grid_y - 2, 0), min(grid_y + 3, grid_height)):
                s = grid[i + j * grid_width]
                if s:
                    dx, dy = s[0] - x, s[1] - y
                    if dx * dx + dy * dy < radius * radius:
                        return False
        return True

    # First sample
    x, y = int(width / 2), int(height / 2)
    queue.append((x, y))
    samples.append((x, y))
    grid[get_grid_index(x, y)] = (x, y)

    # Generate other samples
    while queue:
        i = random.randint(0, len(queue) - 1)
        parent_x, parent_y = queue[i]

        for _ in range(k):
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(radius, 2 * radius)
            x = parent_x + r * math.cos(angle)
            y = parent_y + r * math.sin(angle)

            x = round(x)
            y = round(y)

            if 0 <= x < width and 0 <= y < height and far(x, y):
                queue.append((x, y))
                samples.append((x, y))
                grid[get_grid_index(x, y)] = (x, y)
                break
        else:
            # If no point was added, remove the parent from the queue
            queue.pop(i)

    return samples
