from collections import defaultdict
from operator import add

import math


def read_input(filename: str):
    elves = set()
    with open(filename) as f:
        for i, line in enumerate(f):
            sp = [*line.rstrip('\n')]
            elves.update((i, j) for j in range(len(sp)) if sp[j] == '#')
    return elves


def tuple_sum(tup1, tup2):
    return tuple(map(add, tup1, tup2))


def proposed_move(elf, idx, elves):
    surrounding_positions = [(-1, 0), (-1, 1), (-1, -1), (1, 0), (1, 1), (1, -1), (0, 1), (0, -1)]
    checks = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(1, -1), (1, 0), (1, 1)],
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 1), (0, 1), (1, 1)]
    ]
    # Does not move when empty around it
    if all(tuple_sum(elf, move) not in elves for move in surrounding_positions):
        return elf

    for i in range(4):
        check = checks[(idx + i) % 4]
        if all(tuple_sum(elf, move) not in elves for move in check):
            return tuple_sum(elf, check[1])

    # Elf has another elf in every surrounding "check"
    return elf


def solve(filename: str, n=10):
    elves = read_input(filename)
    idx = 0
    for i in range(n):
        next_moves = defaultdict(list)
        for elf in elves:
            nxt = proposed_move(elf, idx, elves)
            if elf == nxt:
                continue
            next_moves[nxt].append(elf)
        no_move = True
        for nxt in next_moves:
            if len(next_moves[nxt]) > 1:
                continue
            no_move = False
            elf = next_moves[nxt][0]
            elves.remove(elf)
            elves.add(nxt)
        if no_move:
            # Number of rounds to reach no move
            return idx + 1
        idx += 1

    max_r = max(r for r, _ in elves)
    min_r = min(r for r, _ in elves)
    max_c = max(c for _, c in elves)
    min_c = min(c for _, c in elves)
    return (max_r - min_r + 1) * (max_c - min_c + 1) - len(elves)


if __name__ == '__main__':
    print(solve("example23.txt"))
    print(solve("input23.txt"))
    print(solve("example23.txt", n=10**20))
    print(solve("input23.txt", n=10**20))
