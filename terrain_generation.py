import math
import numpy as np
from opensimplex import OpenSimplex

class TerrainGenerator:
    def __init__(self, seed):
        self.simplex = OpenSimplex(seed)

    def calculate_distance(self, p1, p2):
        """
        Calculate the Euclidean distance between two points.
        """
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def generate_elevation(self, width, height, scale, octaves, persistence, min_elevation=-1000, max_elevation=15000):
        """
        Generate an elevation map using Perlin noise.

        Args:
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
                    elevation_map[i][j] += amplitude * self.simplex.noise2(i / scale, j / scale)
            max_amplitude += amplitude
            amplitude *= persistence
            scale /= 2
        elevation_map /= max_amplitude

        # Current values are in the range of about [-.5, .5], so we'll rescale
        # them to the desired range of elevation values.
        elevation_map = min_elevation + (elevation_map + 0.5) * (max_elevation - min_elevation)
        return elevation_map

    def generate_temperature(self, width, height, scale, equator_position, min_temperature=-20, max_temperature=120):
        """
        Generate a temperature map based on latitude and Perlin noise.

        equator_position ends up being effectively the distance in pixels from
        the top of the map to the equator.

        Args:
            width (int): The width of the temperature map.
            height (int): The height of the temperature map.
            scale (float): The scale of the Perlin noise.
            equator_position (int): The position of the equator (latitude).
            min_temperature (int): The minimum temperature value.
            max_temperature (int): The maximum temperature value.

        Returns:
            np.ndarray: The generated temperature map.
        """
        temperature_map = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                noise = self.simplex.noise2(i / scale, j / scale) / 2.0
                distance_from_equator = abs(i - equator_position)
                latitudinal_factor = (1 - (distance_from_equator ** 2 / height ** 2))
                base_temp = min_temperature + (latitudinal_factor * (max_temperature - min_temperature))
                temperature_map[i][j] = base_temp + noise * (max_temperature - min_temperature)

        # Rescale the temperature map to ensure it's within the min and max temperature range
        min_temp_map = np.min(temperature_map)
        max_temp_map = np.max(temperature_map)
        temperature_map = (temperature_map - min_temp_map) / (max_temp_map - min_temp_map)
        temperature_map = min_temperature + (temperature_map * (max_temperature - min_temperature))

        return temperature_map

    def generate_moisture(self, width, height, scale):
        """
        Generate a moisture map based on Perlin noise.

        Args:
            width (int): The width of the moisture map.
            height (int): The height of the moisture map.
            scale (float): The scale of the Perlin noise.

        Returns:
            np.ndarray: The generated moisture map.
        """
        moisture_map = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                moisture_map[i][j] = self.simplex.noise2(i / scale, j / scale)
        return moisture_map

    def generate_wind_map(self, width, height):
        """
        Generate a wind map based on latitude.

        Args:
            width (int): The width of the wind map.
            height (int): The height of the wind map.

        Returns:
            np.ndarray: The generated wind map.
        """
        wind_map = np.zeros((height, width, 2))
        for i in range(height):
            latitude = (i / height) * 180 - 90
            if -30 <= latitude <= 30:  # Trade Winds
                wind_direction = (-1, 0)  # East to West
            elif -60 <= latitude < -30 or 30 < latitude <= 60:  # Westerlies
                wind_direction = (1, 0)  # West to East
            else:  # Polar Easterlies
                wind_direction = (-1, 0)  # East to West
            for j in range(width):
                wind_map[i][j] = wind_direction
        return wind_map

    def adjust_wind_map_for_elevation(self, wind_map, elevation_map, threshold=0.5):
        """
        Adjust the wind direction based on elevation.

        Args:
            wind_map (np.ndarray): The original wind map.
            elevation_map (np.ndarray): The elevation map.
            threshold (float): The elevation threshold for considering high elevation.

        Returns:
            np.ndarray: The adjusted wind map based on elevation.
        """
        height, width, _ = wind_map.shape

        for i in range(height):
            for j in range(width):
                # Check if the current location is adjacent to a high elevation
                if self.is_adjacent_to_high_elevation(i, j, elevation_map, threshold):
                    # Adjust wind direction to flow around the high elevation
                    wind_direction = self.get_wind_diversion(i, j, elevation_map)
                    wind_map[i][j] = wind_direction
                else:
                    # Optionally, adjust wind direction slightly based on local terrain features
                    # This could be a more subtle adjustment for lower elevation changes
                    wind_map[i][j] += self.get_local_wind_adjustment(i, j, elevation_map)

        return wind_map

    def is_adjacent_to_high_elevation(self, i, j, elevation_map, threshold):
        """
        Check if the current cell is adjacent to high elevation.

        Args:
            i (int): The row index of the current cell.
            j (int): The column index of the current cell.
            elevation_map (np.ndarray): The elevation map.
            threshold (float): The elevation threshold for considering high elevation.

        Returns:
            bool: True if the cell is adjacent to high elevation, False otherwise.
        """
        # Simple check for adjacent cells exceeding the elevation threshold
        adjacent_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, E, W
        for dx, dy in adjacent_offsets:
            x, y = i + dx, j + dy
            if 0 <= x < elevation_map.shape[0] and 0 <= y < elevation_map.shape[1]:
                if elevation_map[x][y] > threshold:
                    return True
        return False

    def get_wind_diversion(self, i, j, elevation_map):
        """
        Determine the wind diversion based on the terrain elevation.

        Args:
            i (int): The row index of the current cell.
            j (int): The column index of the current cell.
            elevation_map (np.ndarray): The elevation map.

        Returns:
            tuple: The adjusted wind direction based on the terrain.
        """
        # Analyze Terrain Gradient: Determine the gradient of the terrain
        # around the current location (i, j). This can be done by comparing
        # the elevation of the current cell with the elevations of surrounding
        # cells to identify the general slope direction.

        # Determine Diversion Direction: Based on the gradient, decide how the
        # wind should be diverted. If the terrain rises sharply in the wind's
        # current direction, the wind should be diverted parallel to the slope
        # of the elevation increase, mimicking how wind flows around rather
        # than over a high obstacle.

        # Vector Adjustment: Adjust the wind direction vector to reflect this
        # diversion. The new vector should point in the direction of least
        # resistance, which could be determined by evaluating the terrain
        # gradient in adjacent cells.

        # Determine the indices of the 8 surrounding cells
        neighbors = [(i-1, j-1), (i-1, j), (i-1, j+1),
                     (i, j-1),             (i, j+1),
                     (i+1, j-1), (i+1, j), (i+1, j+1)]

        # Calculate the gradient vector as the weighted sum of the elevation differences
        gradient_x, gradient_y = 0, 0
        for dx, dy in neighbors:
            if 0 <= dx < elevation_map.shape[0] and 0 <= dy < elevation_map.shape[1]:
                weight = 1 / (1 + self.calculate_distance((i, j), (dx, dy)))
                gradient_x += weight * (elevation_map[dx][dy] - elevation_map[i][j])
                gradient_y += weight * (elevation_map[dx][dy] - elevation_map[i][j])

        # Normalize the gradient vector
        gradient_magnitude = math.sqrt(gradient_x**2 + gradient_y**2)
        if gradient_magnitude > 0:
            gradient_x /= gradient_magnitude
            gradient_y /= gradient_magnitude

        # The wind diversion is perpendicular to the gradient vector
        diversion_x = -gradient_y
        diversion_y = gradient_x

        # Return the diversion as a unit vector
        return (diversion_x, diversion_y)

    def get_local_wind_adjustment(self, i, j, elevation_map):
        """
        Determine a local wind adjustment based on the terrain features.

        Args:
            i (int): The row index of the current cell.
            j (int): The column index of the current cell.
            elevation_map (np.ndarray): The elevation map.

        Returns:
            tuple: The local wind adjustment based on the terrain.
        """

        # Local Terrain Variation: Examine the immediate surroundings of (i, j)
        # for minor elevation changes that could influence wind flow. This
        # could involve looking at a smaller neighborhood around the cell.

        # Adjustment Based on Features: Depending on the terrain features
        # detected (e.g., small hills, valleys), slightly adjust the wind
        # vector to reflect the influence of these features. This could mean
        # minor changes in direction or magnitude.

        # Smooth Transition: Ensure that adjustments are smooth and gradual to
        # avoid abrupt changes in wind direction that would not occur in
        # nature.

        # Determine the indices of the 8 surrounding cells
        neighbors = [(i-1, j-1), (i-1, j), (i-1, j+1),
                     (i, j-1),             (i, j+1),
                     (i+1, j-1), (i+1, j), (i+1, j+1)]

        # Calculate the gradient vector as the weighted sum of the elevation differences
        gradient_x, gradient_y = 0, 0
        for dx, dy in neighbors:
            if 0 <= dx < elevation_map.shape[0] and 0 <= dy < elevation_map.shape[1]:
                weight = 1 / (1 + self.calculate_distance((i, j), (dx, dy)))
                gradient_x += weight * (elevation_map[dx][dy] - elevation_map[i][j])
                gradient_y += weight * (elevation_map[dx][dy] - elevation_map[i][j])

        # Normalize the gradient vector
        gradient_magnitude = math.sqrt(gradient_x**2 + gradient_y**2)
        if gradient_magnitude > 0:
            gradient_x /= gradient_magnitude
            gradient_y /= gradient_magnitude

        # Determine Diversion Direction: Based on the gradient, decide how the
        # wind should be diverted. If the terrain rises sharply in the wind's
        # current direction, the wind should be diverted parallel to the slope
        # of the elevation increase, mimicking how wind flows around rather
        # than over a high obstacle.

        # The wind diversion is perpendicular to the gradient vector
        diversion_x = -gradient_y
        diversion_y = gradient_x

        # Return the diversion as a unit vector
        return (diversion_x, diversion_y)

    def adjust_moisture_for_orographic_effect(self, moisture_map, elevation_map, wind_map):
        """
        Calculate the orographic effect on moisture based on elevation and wind direction.

        Args:

            moisture_map (np.ndarray): The original moisture map.
            elevation_map (np.ndarray): The elevation map.
            wind_map (np.ndarray): The wind map.

        Returns:
            np.ndarray: The orographic moisture map based on elevation and wind direction.
        """
        orographic_moisture = np.copy(moisture_map)
        for i in range(orographic_moisture.shape[0]):
            for j in range(orographic_moisture.shape[1]):
                wind_direction = wind_map[i][j]
                x, y = int(wind_direction[0]), int(wind_direction[1])
                neighbor_i, neighbor_j = i + y, j + x
                if 0 <= neighbor_i < orographic_moisture.shape[0] and 0 <= neighbor_j < orographic_moisture.shape[1]:
                    orographic_moisture[i][j] = max(0, elevation_map[neighbor_i][neighbor_j] - elevation_map[i][j])
        return orographic_moisture

    def adjust_temperature_for_elevation(self, temperature_map, elevation_map, lapse_rate):
        """
        Adjust the temperature based on elevation using a lapse rate.

        Args:
            temperature_map (np.ndarray): The original temperature map.
            elevation_map (np.ndarray): The elevation map.
            lapse_rate (float): The temperature lapse rate.

        Returns:
            np.ndarray: The adjusted temperature map based on elevation.
        """
        adjusted_temperature_map = np.copy(temperature_map)
        for i in range(adjusted_temperature_map.shape[0]):
            for j in range(adjusted_temperature_map.shape[1]):
                adjusted_temperature_map[i][j] -= lapse_rate * elevation_map[i][j]
        return adjusted_temperature_map
