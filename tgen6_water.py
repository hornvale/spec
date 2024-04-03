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

    def generate_temperature(self, x_start, y_start, width, height, scale, equator_position, max_latitude=100, min_temperature=-20, max_temperature=120, temperature_noise_scale=0.5):
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
            max_latitude (int): The maximum latitude value.
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
                latitudinal_factor = (1 - (distance_from_equator ** 2 / (max_latitude ** 2)))
                base_temp = min_temperature + (latitudinal_factor * (max_temperature - min_temperature))

                # Adjust temperature based on Perlin noise
                noise = self.simplex.noise2(x / scale, y / scale)
                temperature_variation_range = (max_temperature - min_temperature) * temperature_noise_scale
                noise_contribution = noise * temperature_variation_range

                # Set temperature, ensuring it stays within specified min and max bounds
                temperature = base_temp + noise_contribution
                temperature_map[i][j] = np.clip(temperature, min_temperature, max_temperature)

        return temperature_map

    def seasonal_temperature_modifier(self, day_of_year, amplitude=10, days_in_year=365):
        """
        Calculate a seasonal temperature modifier based on the day of the year.

        Args:
            day_of_year (int): The day of the year.
            amplitude (float): The amplitude of the temperature variation.
            days_in_year (int): The total number of days in a year.

        Returns:
            float: The seasonal temperature modifier.
        """
        radians = (2 * math.pi / days_in_year) * day_of_year
        return amplitude * math.sin(radians)

    def apply_seasonal_variation(self, temperature_map, day_of_year, amplitude=20, days_in_year=365):
        """
        Apply seasonal variation to the temperature map.

        Args:
            temperature_map (np.ndarray): The original temperature map.
            day_of_year (int): The day of the year.
            amplitude (float): The amplitude of the temperature variation.
            days_in_year (int): The total number of days in a year.

        Returns:
            np.ndarray: The temperature map with seasonal variation applied.
        """
        modified_map = temperature_map.copy()
        seasonal_shift = self.seasonal_temperature_modifier(day_of_year, amplitude, days_in_year)
        modified_map += seasonal_shift
        return modified_map

    def latitude_seasonal_scale(self, latitude, max_latitude, scaling_factor=0.5):
        """
        Calculate a seasonal scaling factor based on latitude.

        Args:
            latitude (float): The latitude of the location.
            max_latitude (float): The maximum latitude value.
            scaling_factor (float): The scaling factor for the effect.

        Returns:
            float: The seasonal scaling factor based on latitude.
        """
        return 1 - (abs(latitude) / max_latitude) ** scaling_factor

    def apply_seasonal_and_latitude_variation(self, temperature_map, day_of_year, max_latitude, equator_position, amplitude=20, days_in_year=365, scaling_factor=0.5):
        """
        Apply seasonal and latitude-based variation to the temperature map.

        equator_position ends up being effectively the distance in pixels from
        the top of the map to the equator.

        Args:
            temperature_map (np.ndarray): The original temperature map.
            day_of_year (int): The day of the year.
            max_latitude (float): The maximum latitude value.
            equator_position (int): The position of the equator (latitude).
            amplitude (float): The amplitude of the temperature variation.
            days_in_year (int): The total number of days in a year.
            scaling_factor (float): The scaling factor for the latitude effect.

        Returns:
            np.ndarray: The temperature map with seasonal and latitude-based variation applied.
        """
        modified_map = temperature_map.copy()
        for i in range(modified_map.shape[0]):
            latitude = (i - equator_position) / max_latitude
            seasonal_shift = self.seasonal_temperature_modifier(day_of_year, amplitude, days_in_year) * self.latitude_seasonal_scale(latitude, max_latitude, scaling_factor)
            modified_map[i, :] += seasonal_shift
        return modified_map

    def generate_moisture(self, x_start, y_start, width, height, scale, octaves=2, persistence=0.5):
        """
        Generate a moisture map based on Perlin noise.

        Args:
            x_start (int): The starting x-coordinate of the moisture map.
            y_start (int): The starting y-coordinate of the moisture map.
            width (int): The width of the moisture map.
            height (int): The height of the moisture map.
            scale (float): The scale of the Perlin noise.
            octaves (int): The number of octaves to generate.
            persistence (float): The persistence value for the Perlin noise.

        Returns:
            np.ndarray: The generated moisture map.
        """
        moisture_map = np.zeros((height, width))
        max_amplitude = 0
        amplitude = 1
        for _ in range(octaves):
            for i in range(height):
                for j in range(width):
                    x = x_start + i
                    y = y_start + j
                    moisture_map[i][j] += amplitude * self.simplex.noise2(x / scale, y / scale)
            max_amplitude += amplitude
            amplitude *= persistence
            scale /= 2
        moisture_map /= max_amplitude
        return moisture_map

    def generate_water(self, elevation_map, water_level):
        """
        Generate a water map based on an elevation map and a water level.

        Args:
            elevation_map (np.ndarray): The elevation map.
            water_level (float): The water level.

        Returns:
            np.ndarray: A binary water map.
        """
        water_map = np.zeros(elevation_map.shape)
        water_map[elevation_map <= water_level] = 1  # Water
        water_map[elevation_map > water_level] = 0  # Land
        return water_map

    def is_local_maximum(self, y, x, elevation_map):
        """
        Check if a point is a local maximum in its neighborhood.

        Args:
            y (int): The y-coordinate of the point.
            x (int): The x-coordinate of the point.
            elevation_map (np.ndarray): The elevation map.

        Returns:
            bool: True if the point is a local maximum, False otherwise.
        """
        max_elevation = elevation_map[y, x]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < elevation_map.shape[0] and 0 <= nx < elevation_map.shape[1]:
                    if elevation_map[ny, nx] > max_elevation:
                        return False
        return True

    def find_water_sources(self, elevation_map, percentile=95):
        """
        Find water sources based on the elevation map.

        Args:
            elevation_map (np.ndarray): The elevation map.
            percentile (int): The percentile threshold for identifying water sources.

        Returns:
            list: A list of water source coordinates.
        """
        threshold = np.percentile(elevation_map, percentile)
        sources = np.argwhere(elevation_map > threshold)
        sources = [(y, x) for y, x in sources if self.is_local_maximum(y, x, elevation_map)]
        return sources

    def generate_water_sources(self, elevation_map, percentile=95):
        """
        Generate a water source map based on the elevation map.

        Args:
            elevation_map (np.ndarray): The elevation map.
            percentile (int): The percentile threshold for identifying water sources.

        Returns:
            np.ndarray: A binary water source map.
        """
        water_sources = self.find_water_sources(elevation_map, percentile)
        water_source_map = np.zeros(elevation_map.shape)
        for y, x in water_sources:
            water_source_map[y, x] = 1
        return water_source_map

    def find_downhill_water_path(self, y, x, elevation_map):
        """
        Find a downhill path from a given point on the elevation map.

        Args:
            y (int): The y-coordinate of the starting point.
            x (int): The x-coordinate of the starting point.
            elevation_map (np.ndarray): The elevation map.

        Returns:
            list: A list of coordinates representing the downhill path.
        """
        path = []
        while True:
            path.append((y, x))
            next_y, next_x = None, None
            lowest = elevation_map[y, x]
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = y + dy, x + dx
                    if (0 <= ny < elevation_map.shape[0] and 0 <= nx < elevation_map.shape[1] and
                            (ny, nx) not in path and elevation_map[ny, nx] < lowest):
                        lowest = elevation_map[ny, nx]
                        next_y, next_x = ny, nx
            if next_y is None or elevation_map[next_y, next_x] >= elevation_map[y, x]:
                # No lower adjacent cell or we are at a local minimum (lake or ocean)
                break
            y, x = next_y, next_x
        return path

    def generate_rivers(self, elevation_map, water_map, water_sources):
        """
        Generate rivers based on the elevation map and water sources.

        Args:
            elevation_map (np.ndarray): The elevation map.
            water_map (np.ndarray): The water map.
            water_sources (list): A list of water source coordinates.

        Returns:
            np.ndarray: The generated river map.
        """
        river_map = np.zeros(elevation_map.shape)
        for y, x in water_sources:
            path = self.find_downhill_water_path(y, x, elevation_map)
            width = 1
            for y, x in path:
                if water_map[y, x] >= 1:
                    width += water_map[y, x]
                river_map[y, x] = width
            y, x = path[-1]
            self.expand_lake(y, x, elevation_map, river_map)
        return river_map

    def generate_lakes(self, elevation_map, river_map):
        """
        Form lakes based on the river map and elevation map.

        Args:
            elevation_map (np.ndarray): The elevation map.
            river_map (np.ndarray): The river map.

        Returns:
            np.ndarray: A new rivers map incorporating the lakes.
        """
        lakes_map = np.copy(river_map)
        for y in range(elevation_map.shape[0]):
            for x in range(elevation_map.shape[1]):
                if self.is_local_minimum(y, x, elevation_map):
                    self.expand_lake(y, x, elevation_map, lakes_map, lake_depth=50, max_gradient=50)
        return lakes_map

    def is_local_minimum(self, y, x, elevation_map):
        """
        Check if a point is a local minimum in its neighborhood.

        Args:
            y (int): The y-coordinate of the point.
            x (int): The x-coordinate of the point.
            elevation_map (np.ndarray): The elevation map.

        Returns:
            bool: True if the point is a local minimum, False otherwise.
        """
        min_elevation = elevation_map[y, x]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < elevation_map.shape[0] and 0 <= nx < elevation_map.shape[1]:
                    if elevation_map[ny, nx] < min_elevation:
                        return False
        return True

    def expand_lake(self, y, x, elevation_map, river_map, lake_depth=100, max_gradient=50):
        """
        Expand a lake from a starting point, allowing the lake to fill up to a certain depth.

        Args:
            y (int): The y-coordinate of the starting point.
            x (int): The x-coordinate of the starting point.
            elevation_map (np.ndarray): The elevation map.
            river_map (np.ndarray): The river map.
            lake_depth (float): The maximum depth a lake can fill up from its starting elevation.
            max_gradient (float): The maximum gradient allowed for expanding the lake.

        Returns:
            np.ndarray: The updated river map.
        """
        start_elevation = elevation_map[y, x]
        queue = [(y, x)]
        visited = set()
        while queue:
            cy, cx = queue.pop(0)
            if (cy, cx) in visited:
                continue
            visited.add((cy, cx))
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < elevation_map.shape[0] and 0 <= nx < elevation_map.shape[1]:
                        elevation_difference = elevation_map[ny, nx] - start_elevation
                        if elevation_difference <= lake_depth and elevation_difference >= -max_gradient:
                            if river_map[ny, nx] == 0:  # Ensure we're not overwriting rivers
                                river_map[ny, nx] = 2  # Mark as lake
                            queue.append((ny, nx))

    def generate_merged_elevation_and_river_map(self, elevation_map, river_map):
        """
        Generate a merged elevation and river map.

        This is not actually good. Don't use it. It's just a graphical demo.

        Args:
            elevation_map (np.ndarray): The elevation map.
            river_map (np.ndarray): The river map.

        Returns:
            np.ndarray: The merged elevation and river map.
        """
        merged_map = np.copy(elevation_map)
        for y in range(elevation_map.shape[0]):
            for x in range(elevation_map.shape[1]):
                if river_map[y, x] > 0:
                    merged_map[y, x] = river_map[y, x]
        return merged_map
