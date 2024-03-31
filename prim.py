import math
import random
import heapq

from bridson import poisson_disc_sampler

def calculate_distance(p1, p2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def prim_mst(points):
    if not points:
        return []

    # Initialize structures
    mst_edges = []  # To store the edges of the MST
    connected_points = set([points[0]])  # Use a set for O(1) lookups
    candidate_edges = []  # Use a priority queue for candidate edges
    point_to_edges = {point: [] for point in points}  # Maps points to their edges

    # Initialize priority queue with edges from the first point
    def add_edges_for_point(point):
        for other_point in points:
            if other_point != point:
                distance = calculate_distance(point, other_point)
                edge = (distance, point, other_point)
                heapq.heappush(candidate_edges, edge)
                point_to_edges[point].append(edge)

    add_edges_for_point(points[0])

    # Generate the MST
    while len(connected_points) < len(points):
        # Get the shortest edge where one endpoint is in the tree
        while True:
            distance, p1, p2 = heapq.heappop(candidate_edges)
            if p2 not in connected_points:
                break

        # Add the new point and edge to the MST
        connected_points.add(p2)
        mst_edges.append((p1, p2))

        # Add new candidate edges for the newly connected point
        add_edges_for_point(p2)

    return mst_edges
