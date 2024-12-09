import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *

def read_grid(fname):
    content = get_readlines_stripped(fname)
    obstacles = set()
    start_pos = None
    for i, line in enumerate(content):
        for j, char in enumerate(line):
            if char == "#":
                obstacles.add((i, j))
            elif char == "^":
                start_pos = (i, j)
    m = len(content)
    n = len(content[0])
    return obstacles, start_pos, m, n


def run_part_one(obstacles, start_pos, m, n):
    curr_dir = 3
    visited = set()
    r, c = start_pos
    while 0 <= r < m and 0 <= c < n:
        visited.add((r, c))
        next_pos = sum_tuples((r, c), DIRS[curr_dir])
        if next_pos in obstacles:
            curr_dir = (curr_dir + 1) % 4
            continue
        else:
            r, c = next_pos
    return visited


def solve_part_one(fname):
    obstacles, start_pos, m, n = read_grid(fname)
    visited = run_part_one(obstacles, start_pos, m, n)
    return len(visited) - 1


def solve_part_two(fname):
    obstacles, start_pos, m, n = read_grid(fname)
    og_path = run_part_one(obstacles, start_pos, m, n)
    s = 0
    for nr in range(m):
        for nc in range(n):
            if (nr, nc) in obstacles or (nr, nc) == start_pos or (nr, nc) not in og_path:
                continue
            curr_dir = 3
            r, c = start_pos
            visited = set()
            obstacles.add((nr, nc))
            while 0 <= r < m and 0 <= c < n:
                if (r, c, curr_dir) in visited:
                    s += 1
                    break
                visited.add((r, c, curr_dir))
                next_pos = sum_tuples((r, c), DIRS[curr_dir])
                if next_pos in obstacles:
                    curr_dir = (curr_dir + 1) % 4
                    continue
                else:
                    r, c = next_pos
            obstacles.remove((nr, nc))
    return s


def run_solution(day, ignore_example=False, ex_answer_1=41, ex_answer_2=6):
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
