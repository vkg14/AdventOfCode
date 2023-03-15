import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple


@dataclass
class HeapNode:
    negative_distance: int
    group: int
    point: Tuple

    def __lt__(self, other):
        return self.negative_distance < other.negative_distance


def distance_squared(p1, p2):
    return sum((x1 - x2) ** 2 for x1, x2 in zip(p1, p2))


def k_nearest_neighbor_classifier(p, classified_points, k):
    """
    Use heapq which is a min heap API.  Can configure heap node to have the negative distance
    so that we can think of the algorithm as this:
    - use a max heap of max size k
    - maintain the k smallest distances by popping off the max when the next element is closer.
    """
    pq = []
    for group, points in classified_points.items():
        for point in points:
            d = distance_squared(p, point)
            node = HeapNode(-1 * d, group, point)
            if len(pq) < k:
                heapq.heappush(pq, node)
            elif pq[0].negative_distance < node.negative_distance:
                heapq.heappushpop(pq, node)
    counts = defaultdict(int)
    for node in pq:
        counts[node.group] += 1
    return max((c, g) for g, c in counts.items())[1]


if __name__ == '__main__':
    points = {
        0: [(1, 12), (2, 5), (3, 6), (3, 10), (3.5, 8), (2, 11), (2, 9), (1, 7)],
        1: [(5, 3), (3, 2), (1.5, 9), (7, 2), (6, 1), (3.8, 1), (5.6, 4), (4, 2), (2, 5)]
    }
    p = (2.5, 7)
    print(k_nearest_neighbor_classifier(p, points, 3))
