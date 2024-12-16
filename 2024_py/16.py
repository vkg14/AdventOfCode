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
    for i, line in enumerate(content):
        for j, char in enumerate(line):
            if char == "#":
                obstacles.add((i, j))
            elif char == "S":
                start_pos = (i, j)
            elif char == "E":
                end_pos = (i, j)
    m = len(content)
    n = len(content[0])
    return obstacles, start_pos, end_pos, m, n


def solve_part_one(fname):
    obstacles, start_pos, end_pos, m, n = parse(fname)
    pq = []
    heappush(pq, (0, start_pos, (0, 1)))  # (distance, node)

    scores = {start_pos: 0}

    while pq:
        score, pos, d = heappop(pq)

        if score > scores.get(pos, sys.maxsize):
            continue

        if pos == end_pos:
            return score

        idx = DIRS.index(d)
        for n_idx in [idx, (idx+1) % 4, (idx-1) % 4]:
            next_d = DIRS[n_idx]
            nxt_pos = sum_tuples(pos, next_d)
            if nxt_pos in obstacles or not in_bounds(nxt_pos, m, n):
                continue
            nxt_score = score + (1 if next_d == d else 1001)

            if nxt_score < scores.get(nxt_pos, sys.maxsize):
                scores[nxt_pos] = nxt_score
                heappush(pq, (nxt_score, nxt_pos, next_d))

    return -1


def solve_part_two(fname):
    return -1


def run_solution(day, ignore_example=False, ex_answer_1=11048, ex_answer_2=0):
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
