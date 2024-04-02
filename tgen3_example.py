from tgen3_seasonal_temperature_variation import TerrainGenerator
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Initialize the terrain generator with a seed for reproducibility
generator = TerrainGenerator(seed=42)
elevation_map = generator.generate_elevation(x_start=0, y_start=0, width=100, height=100, scale=50, octaves=4, persistence=0.5)
temperature_map = generator.generate_temperature(x_start=0, y_start=0, width=100, height=100, scale=50, equator_position=100, max_latitude=100)
temperature_summer_map = generator.apply_seasonal_variation(temperature_map, day_of_year=93, amplitude=20, days_in_year=365)
temperature_autumn_map = generator.apply_seasonal_variation(temperature_map, day_of_year=187, amplitude=20, days_in_year=365)
temperature_winter_map = generator.apply_seasonal_variation(temperature_map, day_of_year=280, amplitude=20, days_in_year=365)

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
    elif event.key == 'q':
        plt.close()

# Connect the keyboard event handler
fig.canvas.mpl_connect('key_press_event', on_key)

# Initial plot to show something on start
plot_data(elevation_map, 'Elevation')

plt.show()
