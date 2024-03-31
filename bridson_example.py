
from bridson import poisson_disc_sampler
import matplotlib.pyplot as plt

width, height, radius = 1000, 1000, 20
samples = poisson_disc_sampler(width, height, radius)

print(samples)

x_coords, y_coords = zip(*samples)
plt.scatter(x_coords, y_coords, s=1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
