import os
import re
import sys
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    grid, m, n = get_grid_as_map(fname)
    start = [(r, c) for r, c in iter_cells(m, n) if grid[(r, c)] == 'S'][0]
    end = [(r, c) for r, c in iter_cells(m, n) if grid[(r, c)] == 'E'][0]
    return grid, start, end, m, n


def best_path(grid, m, n, start, end):
    q = deque([(start, 0)])
    prev = {start: None}
    best = {}
    while q:
        pos, step = q.popleft()
        best[pos] = step
        for nxt in get_neighbors(m, n, DIRS, pos):
            if nxt in prev or grid[nxt] == '#':
                continue
            prev[nxt] = pos
            q.append((nxt, step + 1))

    path = [end]
    curr = end
    while curr != start:
        path.append(prev[curr])
        curr = prev[curr]

    return best[end], path, best


def explore_cheat(grid, m, n, start, tolerance=20):
    q = deque([(start, 0)])
    prev = {}
    best = {}
    while q:
        pos, step = q.popleft()
        # Must be on a safe spot at the end
        if grid[pos] != '#' and pos != start:
            best[pos] = step

        # Once we hit tolerance, we can't move forward
        if step == tolerance:
            continue

        for nxt in get_neighbors(m, n, DIRS, pos):
            if nxt in prev:
                continue
            prev[nxt] = pos
            q.append((nxt, step + 1))
    return best


def solve(fname, saved_time=100, tolerance=20):
    grid, start, end, m, n = parse(fname)
    # Run BFS from end -> start so best[pos] = len_path(pos, end)
    total_picos, path, best = best_path(grid, m, n, end, start)
    goal_picos = total_picos - saved_time

    cheats = 0
    for steps, start_cheat in enumerate(path):
        reachable = explore_cheat(grid, m, n, start_cheat, tolerance=tolerance)

        for end_cheat, length in reachable.items():
            # start -> start_cheat, start_cheat -> end_cheat, end_cheat -> end
            total_picos = steps + length + best[end_cheat]
            if total_picos <= goal_picos:
                cheats += 1
    return cheats


def solve_part_one(fname, example=False):
    return solve(fname, saved_time=2 if example else 100, tolerance=2)


def solve_part_two(fname, example=False):
    return solve(fname, saved_time=72 if example else 100, tolerance=20)


def run_solution(day, ignore_example=False, ex_answer_1=44, ex_answer_2=29):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file, True)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    if not ignore_example:
        p2 = solve_part_two(example_file, True)
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
