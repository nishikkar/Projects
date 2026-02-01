import math
import random

# ---------- Utility Functions ----------

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(p1, p2)]))


def get_neighbors(data, point_idx, eps):
    """Return indices of all points within eps distance of given point."""
    neighbors = []
    for i, point in enumerate(data):
        if euclidean_distance(data[point_idx], point) <= eps:
            neighbors.append(i)
    return neighbors


# ---------- DBSCAN Implementation ----------

def dbscan(data, eps, min_pts):
    """
    Perform DBSCAN clustering from scratch.
    data : list of lists (each sublist is a data point)
    eps : neighborhood radius
    min_pts : minimum number of points to form a dense region
    """
    labels = [0] * len(data)   # 0 = unvisited, -1 = noise, 1..k = cluster ids
    cluster_id = 0

    for i in range(len(data)):
        if labels[i] != 0:  # already processed
            continue

        # Find neighbors of point i
        neighbors = get_neighbors(data, i, eps)

        # Not enough neighbors → mark as noise
        if len(neighbors) < min_pts:
            labels[i] = -1
        else:
            # Start a new cluster
            cluster_id += 1
            expand_cluster(data, labels, i, neighbors, cluster_id, eps, min_pts)

    return labels


def expand_cluster(data, labels, point_idx, neighbors, cluster_id, eps, min_pts):
    """Expand the new cluster from the seed point."""
    labels[point_idx] = cluster_id

    i = 0
    while i < len(neighbors):
        neighbor_idx = neighbors[i]

        if labels[neighbor_idx] == -1:
            labels[neighbor_idx] = cluster_id  # change noise to border point

        elif labels[neighbor_idx] == 0:
            labels[neighbor_idx] = cluster_id
            neighbor_neighbors = get_neighbors(data, neighbor_idx, eps)
            if len(neighbor_neighbors) >= min_pts:
                neighbors += neighbor_neighbors
        i += 1


# ---------- Example Dataset (for testing) ----------

def generate_dataset(n_points=50):
    """Generate simple 2D dataset with two clusters."""
    data = []
    for _ in range(n_points // 2):
        data.append([random.uniform(0, 5), random.uniform(0, 5)])
    for _ in range(n_points // 2):
        data.append([random.uniform(8, 12), random.uniform(8, 12)])
    return data


# ---------- Run Example ----------

if _name_ == "_main_":
    data = generate_dataset(40)
    eps = 1.5
    min_pts = 3

    labels = dbscan(data, eps, min_pts)

    print("Data Points and their Cluster IDs:")
    for point, label in zip(data, labels):
        print(f"{point} -> Cluster {label}")