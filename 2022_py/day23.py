from collections import defaultdict

import math


def read_input(filename: str):
    elves = set()
    with open(filename) as f:
        for i, line in enumerate(f):
            sp = [*line.rstrip('\n')]
            for j in range(len(sp)):
                if sp[j] == '#':
                    elves.add((i, j))
    return elves


def proposed_move(elf, idx, elves):
    surrounding_positions = [(-1, 0), (-1, 1), (-1, -1), (1, 0), (1, 1), (1, -1), (0, 1), (0, -1)]
    checks = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(1, -1), (1, 0), (1, 1)],
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 1), (0, 1), (1, 1)]
    ]
    no_move = True
    for move in surrounding_positions:
        if tuple([sum(x) for x in zip(*[elf, move])]) in elves:
            no_move = False
            break
    if no_move:
        return elf, elf

    for i in range(4):
        check = checks[(idx + i) % 4]
        can_move = True
        for move in check:
            if tuple([sum(x) for x in zip(*[elf, move])]) in elves:
                can_move = False
                break
        if can_move:
            return elf, tuple([sum(x) for x in zip(*[elf, check[1]])])

    return elf, elf


def solve(filename: str, n=10):
    elves = read_input(filename)
    idx = 0
    rounds = 1
    for i in range(n):
        next_moves = defaultdict(list)
        for elf in elves:
            elf, nxt = proposed_move(elf, idx, elves)
            if elf == nxt:
                continue
            next_moves[nxt].append(elf)
        no_move = True
        for nxt in next_moves.keys():
            if len(next_moves[nxt]) > 1:
                continue
            no_move = False
            elf = next_moves[nxt][0]
            elves.remove(elf)
            elves.add(nxt)
        if no_move:
            return rounds
        idx += 1
        rounds += 1

    max_r = -math.inf
    max_c = -math.inf
    min_r = math.inf
    min_c = math.inf
    for r, c in elves:
        max_r = max(max_r, r)
        min_r = min(min_r, r)
        max_c = max(max_c, c)
        min_c = min(min_c, c)
    return (max_r - min_r + 1) * (max_c - min_c + 1) - len(elves)


if __name__ == '__main__':
    print(solve("example23.txt"))
    print(solve("input23.txt"))
    print(solve("example23.txt", n=10**20))
    print(solve("input23.txt", n=10**20))
