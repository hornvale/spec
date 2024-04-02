import math
import numpy as np
from opensimplex import OpenSimplex

class TerrainGenerator:
    def __init__(self, seed):
        self.simplex = OpenSimplex(seed)

    def generate_elevation(self, x_start, y_start, width, height, scale, octaves, persistence, min_elevation=-1000, max_elevation=15000):
        """
        Generate an elevation map using Perlin noise.

        Args:
            x_start (int): The starting x-coordinate of the elevation map.
            y_start (int): The starting y-coordinate of the elevation map.
            width (int): The width of the elevation map.
            height (int): The height of the elevation map.
            scale (float): The scale of the Perlin noise.
            octaves (int): The number of octaves to generate.
            persistence (float): The persistence value for the Perlin noise.
            min_elevation (int): The minimum elevation value.
            max_elevation (int): The maximum elevation value.

        Returns:
            np.ndarray: The generated elevation map.
        """
        elevation_map = np.zeros((height, width))
        max_amplitude = 0
        amplitude = 1
        for _ in range(octaves):
            for i in range(height):
                for j in range(width):
                    x = x_start + i
                    y = y_start + j
                    elevation_map[i][j] += amplitude * self.simplex.noise2(x / scale, y / scale)
            max_amplitude += amplitude
            amplitude *= persistence
            scale /= 2
        elevation_map /= max_amplitude

        # Current values are in the range of about [-.5, .5], so we'll rescale
        # them to the desired range of elevation values.

        elevation_map = min_elevation + (elevation_map + 0.5) * (max_elevation - min_elevation)
        return elevation_map
