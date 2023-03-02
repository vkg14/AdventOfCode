import math
from collections import defaultdict, deque
from operator import add


def read_input(filename: str):
    # You don't need walls - start and end position are the only reachable points outside boundary.
    walls = set()
    blizzards = defaultdict(list)
    directions = {
        '>': (0, 1),
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0)
    }
    # Set start and end to None to reduce confusion and ensure they are set correctly
    start = None
    sp = []
    with open(filename) as f:
        for i, line in enumerate(f):
            row = i - 1
            sp = [*line.rstrip('\n')]
            if i == 0:
                start = (row, sp.index('.') - 1)
            for j in range(len(sp)):
                col = j - 1
                if sp[j] == '#':
                    walls.add((row, col))
                elif sp[j] in directions:
                    blizzards[(row, col)].append(directions[sp[j]])
    # Use last i and last sp for end
    end = (i-1, sp.index('.') - 1)
    return start, end, blizzards, walls


def tuple_sum(tup1, tup2):
    return tuple(map(add, tup1, tup2))


def move_blizzards(blizzards, right, bottom):
    new_blizzards = defaultdict(list)
    mods = (bottom, right)
    for pos, l in blizzards.items():
        for direction in l:
            next_pos = tuple(p % m for p, m in zip(tuple_sum(pos, direction), mods))
            new_blizzards[next_pos].append(direction)
            continue
    return new_blizzards


def solve(filename: str):
    start, end, blizzards, walls = read_input(filename)
    return search(start, end, blizzards, walls)


def get_bounds(walls):
    # The max dim of walls is the length of occupied space of the blizzards.
    right = max(c for _, c in walls)
    bottom = max(r for r, _ in walls)
    # Blizzards can never reach start or end point so they only roam amongst the inner portion of grid.
    repetitions = right * bottom // math.gcd(right, bottom)
    return right, bottom, repetitions


def inbounds(pos, right, bottom, start):
    # Explicitly include start check since it's outside the bounds of the map
    r, c = pos
    return pos == start or (0 <= r < bottom and 0 <= c < right)


def search(start, end, blizzards, walls, cache=None, offset=0):
    right, bottom, repetitions = get_bounds(walls)
    q = deque([(start, 1)])
    current_round = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
    visited = {(start, 1)}
    while True:
        pos, rd = q.popleft()
        if rd > current_round:
            current_round = rd
            if cache:
                blizzards = cache[(current_round + offset) % repetitions]
            else:
                blizzards = move_blizzards(blizzards, right, bottom)
        for move in directions:
            next_pos = tuple_sum(pos, move)
            if next_pos == end:
                return rd
            if next_pos in blizzards or not inbounds(pos, right, bottom, start):
                # Hits a blizzard or is not within the bounds of the map
                continue
            saved_state = (next_pos, (rd + 1) % repetitions)
            state = (next_pos, (rd + 1))
            if saved_state in visited:
                continue
            q.append(state)
            visited.add(saved_state)


def solve_two(filename: str):
    start, end, blizzards, walls = read_input(filename)
    right, bottom, repetitions = get_bounds(walls)
    print(f'Total repetitions: {repetitions}')
    cache = {0: blizzards}
    for i in range(1, repetitions):
        cache[i] = move_blizzards(cache[i-1], right, bottom)
    rd1 = search(start, end, blizzards, walls, cache)
    rd2 = search(end, start, blizzards, walls, cache, offset=rd1)
    rd3 = search(start, end, blizzards, walls, cache, offset=rd1+rd2)
    return rd1 + rd2 + rd3


if __name__ == '__main__':
    print(solve("example24.txt"))
    print(solve("input24.txt"))
    print(solve_two("example24.txt"))
    print(solve_two("input24.txt"))
