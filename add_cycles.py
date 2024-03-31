from bridson import poisson_disc_sampler
from prim import prim_mst, calculate_distance
import matplotlib.pyplot as plt
import random
import heapq

def nearest_edges(points, num_edges=10):
    """Generate edges to nearest neighbors for each point."""
    edges = []
    for i, point in enumerate(points):
        distances = [(calculate_distance(point, other), i, j)
                     for j, other in enumerate(points) if i != j]
        nearest = heapq.nsmallest(num_edges, distances)
        edges.extend(nearest)
    return edges

def calculate_all_edges(points):
    """Generate all possible edges between points with their distances."""
    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = calculate_distance(points[i], points[j])
            edges.append((distance, points[i], points[j]))
    return edges

def add_cycles_to_mst(points, mst_edges, num_cycles=10):
    """Add additional edges to the MST to introduce cycles.

    Args:
        points (list of tuples): The original points.
        mst_edges (list of tuples): Edges in the MST.
        num_cycles (int): The number of additional cycles to add.

    Returns:
        list of tuples: The updated list of edges including added cycles.
    """
    # Convert mst_edges to a set for faster lookups
    mst_edges_set = set(tuple(sorted([p1, p2])) for p1, p2 in mst_edges)
    # Assuming nearest_edges() is used to get potential edges
    all_edges = nearest_edges(points, num_edges=5)  # or calculate_all_edges(points)
    # Filter out edges already in the MST using the set for efficient lookup
    non_mst_edges = [edge for edge in all_edges if tuple(sorted([edge[1], edge[2]])) not in mst_edges_set]
    # Randomly select edges to add as cycles, ensuring we don't exceed the available edges
    cycles_to_add = random.sample(non_mst_edges, min(num_cycles, len(non_mst_edges)))
    # Convert edge indices back to point tuples for the final edge list
    updated_edges = list(mst_edges) + [(points[edge[1]], points[edge[2]]) for edge in cycles_to_add]
    return updated_edges

points = poisson_disc_sampler(1000, 1000, 20)
mst_edges = prim_mst(points)
updated_edges = add_cycles_to_mst(points, mst_edges, num_cycles=500)

# Plot points
x_coords, y_coords = zip(*points)
plt.scatter(x_coords, y_coords, s=1)

# Draw MST edges
for p1, p2 in updated_edges:
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='r')

plt.gca().set_aspect('equal', adjustable='box')
plt.show()
