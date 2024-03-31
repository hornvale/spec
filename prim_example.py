from bridson import poisson_disc_sampler
from prim import prim_mst
import matplotlib.pyplot as plt

points = poisson_disc_sampler(100, 100, 20)
mst_edges = prim_mst(points)

# Plot points
x_coords, y_coords = zip(*points)
plt.scatter(x_coords, y_coords, s=1)

# Draw MST edges
for p1, p2 in mst_edges:
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='r')

plt.gca().set_aspect('equal', adjustable='box')
plt.show()
