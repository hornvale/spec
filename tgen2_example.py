from tgen2_temperature import TerrainGenerator
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Initialize the terrain generator with a seed for reproducibility
generator = TerrainGenerator(seed=42)
elevation = generator.generate_elevation(x_start=0, y_start=0, width=100, height=100, scale=50, octaves=4, persistence=0.5)
temperature = generator.generate_temperature(x_start=0, y_start=0, width=100, height=100, scale=50, equator_position=80)

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
        plot_data(elevation, 'Elevation')
    elif event.key == 't':
        plot_data(temperature, 'Temperature', cmap='coolwarm')
    elif event.key == 'q':
        plt.close()

# Connect the keyboard event handler
fig.canvas.mpl_connect('key_press_event', on_key)

# Initial plot to show something on start
plot_data(elevation, 'Elevation')

plt.show()
