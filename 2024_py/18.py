import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    content = get_readlines_stripped(fname)
    res = []
    for line in content:
        x, y = [int(l) for l in line.split(',')]
        res.append((x,y))
    return res


def solve_part_one(fname, example=False):
    bytes = parse(fname)
    total = 12 if example else 1024
    return bfs(corrupt_coords(bytes, total), example)


def bfs(corrupt, example=False):
    q = deque()
    q.append(((0, 0), 0))
    visited = {(0, 0)}
    m, n = (7, 7) if example else (71, 71)
    end = (6, 6) if example else (70, 70)
    while q:
        pos, steps = q.popleft()
        if pos == end:
            return steps
        for nxt in get_neighbors(m, n, DIRS, pos):
            if nxt in visited or nxt in corrupt:
                continue
            visited.add(nxt)
            q.append((nxt, steps + 1))
    return -1


def corrupt_coords(bytes, total):
    return {bytes[i] for i in range(total)}


def solve_part_two(fname, example=False):
    bytes = parse(fname)
    start = 13 if example else 1025
    end = len(bytes) - 1
    while start < end:
        mid = (start + end) // 2
        ans = bfs(corrupt_coords(bytes, mid+1), example)
        if ans >= 0:
            start = (start+end)//2 + 1
        else:
            end = (start+end)//2
    return bytes[end]


def run_solution(day, ignore_example=False, ex_answer_1=22, ex_answer_2=(6,1)):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file, example=True)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    if not ignore_example:
        p2 = solve_part_two(example_file, example=True)
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
