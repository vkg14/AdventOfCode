import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    content = get_readlines_stripped(fname)
    graph = {}
    m = len(content)
    n = len(content[0])
    for i, line in enumerate(content):
        for j, char in enumerate(line):
            graph[(i, j)] = int(char)
    return graph, m, n


def solve_part_one(fname):
    g, m, n = parse(fname)

    def dfs(graph, pos, visited):
        visited.add(pos)
        val = graph[pos]
        if val == 9:
            return 1
        total = 0
        for d in DIRS:
            neighbor = sum_tuples(pos, d)
            if neighbor not in visited and in_bounds(neighbor, m, n) and graph[neighbor] == val+1:
                total += dfs(graph, neighbor, visited)
        return total

    t = 0
    for r in range(m):
        for c in range(n):
            if g[(r, c)] == 0:
                t += dfs(g, (r, c), set())
    return t


def solve_part_two(fname):
    g, m, n = parse(fname)

    def dfs(graph, pos):
        val = graph[pos]
        if val == 9:
            return 1
        total = 0
        for d in DIRS:
            neighbor = sum_tuples(pos, d)
            if in_bounds(neighbor, m, n) and graph[neighbor] == val+1:
                total += dfs(graph, neighbor)
        return total

    t = 0
    for r in range(m):
        for c in range(n):
            if g[(r, c)] == 0:
                t += dfs(g, (r, c))
    return t


def solve_part_two_other(fname):
    g, m, n = parse(fname)
    zeroes = []
    nines = []
    for r in range(m):
        for c in range(n):
            if g[(r, c)] == 0:
                zeroes.append((r, c))
            if g[(r, c)] == 9:
                nines.append((r, c))

    def count_paths(graph, start, end, visited):
        if start == end:
            return 1

        visited.add(start)
        val = graph[start]
        total_paths = 0

        for d in DIRS:
            neighbor = sum_tuples(start, d)
            if neighbor not in visited and in_bounds(neighbor, m, n) and graph[neighbor] == val + 1:
                total_paths += count_paths(graph, neighbor, end, visited)

        visited.remove(start)
        return total_paths

    t = 0
    for z in zeroes:
        for nine in nines:
            t += count_paths(g, z, nine, set())
    return t


def run_solution(day, ignore_example=False, ex_answer_1=36, ex_answer_2=81):
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
