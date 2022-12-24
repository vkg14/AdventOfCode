from collections import defaultdict, deque
from operator import add

import math


def read_input(filename: str):
    walls = set()
    blizzards = defaultdict(list)
    directions = {
        '>': (0, 1),
        '^': (-1, 0),
        '<': (0, -1),
        'v': (1, 0)
    }
    start = None
    end = (0, 0)
    with open(filename) as f:
        for i, line in enumerate(f):
            sp = [*line.rstrip('\n')]
            for j in range(len(sp)):
                if sp[j] == '#':
                    walls.add((i, j))
                elif sp[j] in directions:
                    blizzards[(i, j)].append(directions[sp[j]])
            if not start:
                start = (i, sp.index('.'))
            end = (i, sp.index('.') if '.' in sp else -1)
    return start, end, blizzards, walls


def tuple_sum(tup1, tup2):
    return tuple(map(add, tup1, tup2))


def move_blizzards(blizzards, walls, right, bottom):
    new_blizzards = defaultdict(list)
    for pos, l in blizzards.items():
        for direction in l:
            next_pos = tuple_sum(pos, direction)
            if next_pos not in walls:
                new_blizzards[next_pos].append(direction)
            else:
                if direction == (1, 0):
                    wrap = (1, next_pos[1]) if (0, next_pos[1]) in walls else (0, next_pos[1])
                    new_blizzards[wrap].append(direction)
                elif direction == (-1, 0):
                    wrap = (bottom-1, next_pos[1]) if (bottom, next_pos[1]) in walls else (bottom, next_pos[1])
                    new_blizzards[wrap].append(direction)
                elif direction == (0, 1):
                    wrap = (next_pos[0], 1)
                    new_blizzards[wrap].append(direction)
                else:
                    # left
                    wrap = (next_pos[0], right-1)
                    new_blizzards[wrap].append(direction)
    return new_blizzards


def solve(filename: str):
    start, end, blizzards, walls = read_input(filename)
    return search(start, end, blizzards, walls)


def search(start, end, blizzards, walls):
    right = max(c for _, c in walls)
    bottom = max(r for r, _ in walls)
    repetitions = (right - 1) * (bottom - 1)
    q = deque([(start, 1)])
    current_round = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
    visited = {(start, 1)}
    while True:
        pos, rd = q.popleft()
        if rd > current_round:
            blizzards = move_blizzards(blizzards, walls, right, bottom)
            current_round = rd
        for move in directions:
            next_pos = tuple_sum(pos, move)
            if next_pos in walls or next_pos in blizzards or min(next_pos) < 0 or max(next_pos) > max(bottom, right):
                continue
            if next_pos == end:
                return rd, blizzards
            saved_state = (next_pos, (rd + 1) % repetitions)
            state = (next_pos, (rd + 1))
            if saved_state in visited:
                continue
            q.append(state)
            visited.add(saved_state)


def solve_two(filename: str):
    start, end, blizzards, walls = read_input(filename)
    rd1, blizzards = search(start, end, blizzards, walls)
    rd2, blizzards = search(end, start, blizzards, walls)
    rd3, blizzards = search(start, end, blizzards, walls)
    return rd1 + rd2 + rd3


if __name__ == '__main__':
    print(solve("example24.txt"))
    print(solve("input24.txt"))
    print(solve_two("example24.txt"))
    print(solve_two("input24.txt"))
