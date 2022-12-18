import math
from collections import deque
from operator import add


def get_neighbors(cube):
    return [tuple(map(add, cube, delta)) for delta in
            [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]]


def part_one(filename: str):
    cubes = set()
    total_faces = 0
    min_coords = [math.inf, math.inf, math.inf]
    max_coords = [-math.inf, -math.inf, -math.inf]
    with open(filename) as f:
        for line in f:
            coords = tuple([int(x) for x in line.rstrip('\n').split(',')])
            for dim in range(len(coords)):
                min_coords[dim] = min(min_coords[dim], coords[dim] - 1)
                max_coords[dim] = max(max_coords[dim], coords[dim] + 1)
            total_faces += 6
            for adjacent in get_neighbors(coords):
                if adjacent in cubes:
                    total_faces -= 2
            cubes.add(coords)
    return total_faces, cubes, min_coords, max_coords


def solve(filename: str):
    p1_res, cubes, min_coords, max_coords = part_one(filename)
    # Start search one x-coord below the min tuple point
    start = tuple(map(add, min(cubes), (-1, 0, 0)))
    n_dims = len(start)
    visited = {start}
    q = deque([start])
    p2_res = 0
    while q:
        nxt = q.popleft()
        for adjacent in get_neighbors(nxt):
            if any(adjacent[dim] < min_coords[dim] or adjacent[dim] > max_coords[dim] for dim in
                   range(n_dims)) or adjacent in visited:
                continue
            # Any reachable cube is an exposed face - each outer point can reach multiple cubes and multiple
            # outer points can reach same cube but these hit different exposed faces.
            if adjacent in cubes:
                p2_res += 1
                continue
            visited.add(adjacent)
            q.append(adjacent)
    return p1_res, p2_res


if __name__ == '__main__':
    print(solve("example18.txt"))
    print(solve("input18.txt"))
