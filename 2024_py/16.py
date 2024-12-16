import os
import re
import sys
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *

sys.setrecursionlimit(2000)


def parse(fname):
    content = get_readlines_stripped(fname)
    obstacles = set()
    start_pos = None
    end_pos = None
    full_grid = {}
    for i, line in enumerate(content):
        for j, char in enumerate(line):
            if char == "#":
                obstacles.add((i, j))
            elif char == "S":
                start_pos = (i, j)
            elif char == "E":
                end_pos = (i, j)
            full_grid[(i, j)] = char
    m = len(content)
    n = len(content[0])
    return full_grid, obstacles, start_pos, end_pos, m, n


def run_dijkstra(fname):
    _, obstacles, start_pos, end_pos, m, n = parse(fname)
    pq = []
    # score, pos, d, prev_score, prev_pos, prev_d
    heappush(pq, (0, start_pos, (0, 1), -1, None, None))

    scores = {(start_pos, (0, 1)): 0}
    # how to get from (score, pos, d) -> last
    prev = defaultdict(list)

    best_score = sys.maxsize

    while pq:
        score, pos, d, prev_score, prev_pos, prev_d = heappop(pq)

        if score > scores.get((pos, d), sys.maxsize):
            continue

        if pos == end_pos:
            best_score = min(best_score, score)

        # Add path to "best paths" but no need to re-explore if seen
        already_seen = (score, pos, d) in prev
        prev[(score, pos, d)].append((prev_score, prev_pos, prev_d))
        if already_seen:
            continue

        idx = DIRS.index(d)
        for n_idx in [idx, (idx+1) % 4, (idx-1) % 4]:
            next_d = DIRS[n_idx]
            nxt_pos = sum_tuples(pos, next_d)
            if nxt_pos in obstacles or not in_bounds(nxt_pos, m, n):
                continue
            nxt_score = score + (1 if next_d == d else 1001)

            # include == paths here
            if nxt_score <= scores.get((nxt_pos, next_d), sys.maxsize):
                scores[(nxt_pos, next_d)] = nxt_score
                heappush(pq, (nxt_score, nxt_pos, next_d, score, pos, d))

    return best_score, end_pos, prev


def solve_part_one(fname):
    best_score, _, _ = run_dijkstra(fname)
    return best_score


def solve_part_two(fname):
    best_score, end_pos, prev = run_dijkstra(fname)

    q = deque()
    tiles = set()
    for d in DIRS:
        q.append((best_score, end_pos, d))

    while q:
        s, p, d = q.popleft()
        tiles.add(p)
        for ps, pp, pd in prev[(s, p, d)]:
            if ps < 0:
                continue
            q.append((ps, pp, pd))

    return len(tiles)


def run_solution(day, ignore_example=False, ex_answer_1=11048, ex_answer_2=64):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    if not ignore_example:
        p2 = solve_part_two(example_file)
        print(p2)
        assert p2 == ex_answer_2, "Part 2 example case is incorrect."

    print("Solution to Part 2:", solve_part_two(input_file))


if __name__ == '__main__':
    # File stuff
    current_script = __file__
    num = os.path.basename(current_script).split('.')[0]
    try:
        num = int(num)
    except ValueError as e:
        print(f"Your file is not a number: {num}.")
        exit(1)
    if not os.path.exists(f'inputs/input{num}.txt'):
        get_input(day=num)
    print(f"Solving problem {num}\n*************\n")

    run_solution(num)
