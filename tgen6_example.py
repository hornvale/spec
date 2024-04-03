from tgen6_water import TerrainGenerator
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Initialize the terrain generator with a seed for reproducibility
generator = TerrainGenerator(seed=42)
elevation_map = generator.generate_elevation(x_start=0, y_start=0, width=100, height=100, scale=50, octaves=4, persistence=0.5)
generator = TerrainGenerator(seed=43)
temperature_map = generator.generate_temperature(x_start=0, y_start=0, width=100, height=100, scale=50, equator_position=100, max_latitude=100)
temperature_summer_map = generator.apply_seasonal_variation(temperature_map, day_of_year=93, amplitude=20, days_in_year=365)
temperature_autumn_map = generator.apply_seasonal_variation(temperature_map, day_of_year=187, amplitude=20, days_in_year=365)
temperature_winter_map = generator.apply_seasonal_variation(temperature_map, day_of_year=280, amplitude=20, days_in_year=365)
temperature_spring2_map = generator.apply_seasonal_and_latitude_variation(temperature_map, max_latitude=100, equator_position=100, day_of_year=0, amplitude=20, days_in_year=365, scaling_factor=0.1)
temperature_summer2_map = generator.apply_seasonal_and_latitude_variation(temperature_map, max_latitude=100, equator_position=100, day_of_year=93, amplitude=20, days_in_year=365, scaling_factor=0.1)
temperature_autumn2_map = generator.apply_seasonal_and_latitude_variation(temperature_map, max_latitude=100, equator_position=100, day_of_year=187, amplitude=20, days_in_year=365, scaling_factor=0.1)
temperature_winter2_map = generator.apply_seasonal_and_latitude_variation(temperature_map, max_latitude=100, equator_position=100, day_of_year=280, amplitude=20, days_in_year=365, scaling_factor=0.1)
generator = TerrainGenerator(seed=44)
moisture = generator.generate_moisture(x_start=0, y_start=0, width=100, height=100, scale=50)
water_map = generator.generate_water(elevation_map, water_level=1000)
water_sources = generator.find_water_sources(elevation_map, percentile=95)
water_sources_map = generator.generate_water_sources(elevation_map, percentile=95)
river_map = generator.generate_rivers(elevation_map, water_map, water_sources)
lakes_map = generator.generate_lakes(elevation_map, river_map)
merged_map = generator.generate_merged_elevation_and_river_map(elevation_map, river_map)

# Create a figure with a specific gridspec for main plot and colorbar
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[20, 1], figure=fig)
ax = fig.add_subplot(gs[0])
cbar_ax = fig.add_subplot(gs[1])

def plot_data(data, title, cmap='terrain'):
    ax.clear()  # Clear the main plot's axes
    cbar_ax.clear()  # Clear the colorbar's axes
    im = ax.imshow(data, cmap=cmap)
    ax.set_title(title)
    plt.colorbar(im, cax=cbar_ax)  # Create a colorbar in the specified axes
    fig.canvas.draw()

def on_key(event):
    if event.key == 'e':
        plot_data(elevation_map, 'Elevation')
    elif event.key == 't':
        plot_data(temperature_map, 'Temperature', cmap='coolwarm')
    elif event.key == '2':
        plot_data(temperature_summer_map, 'Summer Temperature', cmap='coolwarm')
    elif event.key == '3':
        plot_data(temperature_autumn_map, 'Autumn Temperature', cmap='coolwarm')
    elif event.key == '4':
        plot_data(temperature_winter_map, 'Winter Temperature', cmap='coolwarm')
    elif event.key == '5':
        plot_data(temperature_spring2_map, 'Spring Latitudinal Temperature', cmap='coolwarm')
    elif event.key == '6':
        plot_data(temperature_summer2_map, 'Summer Latitudinal Temperature', cmap='coolwarm')
    elif event.key == '7':
        plot_data(temperature_autumn2_map, 'Autumn Latitudinal Temperature', cmap='coolwarm')
    elif event.key == '8':
        plot_data(temperature_winter2_map, 'Winter Latitudinal Temperature', cmap='coolwarm')
    elif event.key == 'w':
        plot_data(water_map, 'Ocean', cmap='Blues')
    elif event.key == 'r':
        plot_data(water_sources_map, 'Water sources', cmap='Blues')
    elif event.key == 'v':
        plot_data(river_map, 'Rivers', cmap='Blues')
    elif event.key == 'l':
        plot_data(lakes_map, 'Lakes', cmap='Blues')
    elif event.key == 'a':
        plot_data(merged_map, 'Elevation and Rivers', cmap='terrain')
    elif event.key == 'm':
        plot_data(moisture, 'Moisture', cmap='Blues')
    elif event.key == 'q':
        plt.close()

# Connect the keyboard event handler
fig.canvas.mpl_connect('key_press_event', on_key)

# Initial plot to show something on start
plot_data(elevation_map, 'Elevation')

plt.show()
