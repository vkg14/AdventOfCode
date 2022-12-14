def create_grid(fname, with_floor=False):
    start, min_x, max_x, max_y = 500, 500, 500, 0
    rocks = []
    with open(fname) as f:
        for line in f:
            rock = [[int(y) for y in x.strip().split(',')] for x in line.rstrip('\n').split('->')]
            fixed_rock = []
            for x, y in rock:
                min_x = min(x, min_x)
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                fixed_rock.append((x, y))
            rocks.append(fixed_rock)
    min_x = min(start - max_y, min_x)
    max_x = max(start + max_y, max_x)
    if with_floor:
        max_y += 2
        min_x = min(start - max_y, min_x)
        max_x = max(start + max_y, max_x)
        floor = [(min_x, max_y), (max_x, max_y)]
        rocks.append(floor)
    # Create grid
    m = max_y + 1
    n = max_x - min_x + 1
    matrix = [[0] * n for _ in range(m)]
    for rock in rocks:
        prev = rock[0]
        i = 1
        while i < len(rock):
            cur = rock[i]
            if cur[0] == prev[0]:
                lower, higher = sorted([prev[1], cur[1]])
                for k in range(lower, higher + 1):
                    matrix[k][cur[0] - min_x] = 1
            elif cur[1] == prev[1]:
                lower, higher = sorted([prev[0] - min_x, cur[0] - min_x])
                for k in range(lower, higher + 1):
                    matrix[cur[1]][k] = 1
            i += 1
            prev = cur
    return matrix, min_x, max_y


def simulate_sand_grid(matrix, min_x, max_y):
    r, c = 0, 500 - min_x
    if matrix[r][c]:
        # fully filled
        return False
    while r < max_y:
        stopped = True
        for dr, dc in [(1, 0), (1, -1), (1, 1)]:
            if not matrix[r + dr][c + dc]:
                r += dr
                c += dc
                stopped = False
                break
        if stopped:
            matrix[r][c] = 1
            return True


def solve_grid(fname, with_floor=False):
    matrix, min_x, max_y = create_grid(fname, with_floor)
    stopped_sand = 0
    while True:
        if not simulate_sand_grid(matrix, min_x, max_y):
            break
        stopped_sand += 1
    return stopped_sand


#### ALTERNATIVE SOLUTION USING POINT SET (more sensible) ####
def create_point_set(fname, with_floor=False):
    res = set()
    max_y = 0
    start = 500
    with open(fname) as f:
        for line in f:
            endpoints = [[int(y) for y in x.strip().split(',')] for x in line.rstrip('\n').split('->')]
            max_y = max(max_y, *[j for _, j in endpoints])
            prev, i = endpoints[0], 1
            while i < len(endpoints):
                cur = endpoints[i]
                gen_bounds = lambda a, b: [x + j for j, x in enumerate(sorted([a, b]))]
                if prev[0] == cur[0]:
                    bounds = gen_bounds(prev[1], cur[1])
                    res.update(set([(cur[0], k) for k in range(*bounds)]))
                else:
                    bounds = gen_bounds(prev[0], cur[0])
                    res.update(set([(k, cur[1]) for k in range(*bounds)]))
                prev = cur
                i += 1
    if with_floor:
        max_y += 2
        res.update(set([(k, max_y) for k in range(500 - max_y, 500 + max_y + 1)]))
    return res, max_y


def simulate_sand_points(occupied, max_y):
    x, y = 500, 0
    if (x, y) in occupied:
        return False
    while y < max_y:
        stopped = True
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            if (x + dx, y + dy) not in occupied:
                x += dx
                y += dy
                stopped = False
                break
        if stopped:
            occupied.add((x, y))
            return True
    return False


def solve_points(fname, with_floor=False):
    occupied, max_y = create_point_set(fname, with_floor)
    stopped_sand = 0
    while True:
        if not simulate_sand_points(occupied, max_y):
            break
        stopped_sand += 1
    return stopped_sand


if __name__ == '__main__':
    # print(solve_points("example14.txt", with_floor=False))
    # print(solve_grid("example14.txt", with_floor=False))
    print(solve_points("input14.txt", with_floor=False))
    print(solve_grid("input14.txt", with_floor=False))
    # print(solve_points("example14.txt", with_floor=True))
    # print(solve_grid("example14.txt", with_floor=True))
    print(solve_points("input14.txt", with_floor=True))
    print(solve_grid("input14.txt", with_floor=True))
