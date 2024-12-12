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
            graph[(i, j)] = char
    return graph, m, n


def solve_part_one(fname):
    g, m, n = parse(fname)
    vis = set()

    def dfs(graph, pos, visited):
        visited.add(pos)
        val = graph[pos]
        area = 1
        peri = 0
        for d in DIRS:
            neighbor = sum_tuples(pos, d)
            if neighbor not in visited and in_bounds(neighbor, m, n) and graph[neighbor] == val:
                oa, op = dfs(graph, neighbor, visited)
                area += oa
                peri += op
            elif not in_bounds(neighbor, m, n) or graph[neighbor] != val:
                peri += 1
        return area, peri

    t = 0
    for r in range(m):
        for c in range(n):
            if (r, c) not in vis:
                a, p = dfs(g, (r, c), vis)
                t += a * p
    return t


def get_corners(graph, pos, m, n):
    val = graph[pos]
    corners = 0
    for dr in [-1, 1]:
        for dc in [-1, 1]:
            row_adjacent = sum_tuples(pos, (dr, 0))
            col_adjacent = sum_tuples(pos, (0, dc))
            if (not in_bounds(row_adjacent, m, n) or graph[row_adjacent] != val) and (not in_bounds(col_adjacent, m, n) or graph[col_adjacent] != val):
                corners += 1
            diag = sum_tuples(pos, (dr, dc))
            if (in_bounds(row_adjacent, m, n) and graph[row_adjacent] == val) and (in_bounds(col_adjacent, m, n) and graph[col_adjacent] == val) and (not in_bounds(diag, m, n) or graph[diag] != val):
                corners += 1
    return corners


def solve_part_two(fname):
    g, m, n = parse(fname)
    vis = set()

    def dfs(graph, pos, visited):
        visited.add(pos)
        val = graph[pos]
        area = 1
        sides = 0
        for d in DIRS:
            neighbor = sum_tuples(pos, d)
            if neighbor not in visited and in_bounds(neighbor, m, n) and graph[neighbor] == val:
                oa, os = dfs(graph, neighbor, visited)
                area += oa
                sides += os
        sides += get_corners(graph, pos, m, n)
        return area, sides

    t = 0
    for r in range(m):
        for c in range(n):
            if (r, c) not in vis:
                a, s = dfs(g, (r, c), vis)
                t += a*s
    return t


def run_solution(day, ignore_example=False, ex_answer_1=1930, ex_answer_2=1206):
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
