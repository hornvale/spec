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

    def generate_temperature(self, x_start, y_start, width, height, scale, equator_position, min_temperature=-20, max_temperature=120, temperature_noise_scale=0.5):
        """
        Generate a temperature map based on latitude and Perlin noise.

        equator_position ends up being effectively the distance in pixels from
        the top of the map to the equator.

        Args:
            x_start (int): The starting x-coordinate of the temperature map.
            y_start (int): The starting y-coordinate of the temperature map.
            width (int): The width of the temperature map.
            height (int): The height of the temperature map.
            scale (float): The scale of the Perlin noise.
            equator_position (int): The position of the equator (latitude).
            min_temperature (int): The minimum temperature value.
            max_temperature (int): The maximum temperature value.
            temperature_noise_scale (float): The scale of the temperature noise.

        Returns:
            np.ndarray: The generated temperature map.
        """
        temperature_map = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                # Calculate current coordinates within the map
                x = x_start + i
                y = y_start + j

                # Compute distance from the equator and its influence on base temperature
                distance_from_equator = abs((y_start + i) - equator_position)
                latitudinal_factor = (1 - (distance_from_equator ** 2 / ((height / 2) ** 2)))
                base_temp = min_temperature + (latitudinal_factor * (max_temperature - min_temperature))

                # Adjust temperature based on Perlin noise
                noise = self.simplex.noise2(x / scale, y / scale)
                temperature_variation_range = (max_temperature - min_temperature) * temperature_noise_scale
                noise_contribution = noise * temperature_variation_range

                # Set temperature, ensuring it stays within specified min and max bounds
                temperature = base_temp + noise_contribution
                temperature_map[i][j] = np.clip(temperature, min_temperature, max_temperature)

        return temperature_map