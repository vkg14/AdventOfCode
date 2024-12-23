import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    content = get_readlines_stripped(fname)
    edges = defaultdict(set)
    for line in content:
        x, y = line.split('-')
        edges[x].add(y)
        edges[y].add(x)
    return edges


def solve_part_one(fname):
    edges = parse(fname)

    keys = list(edges.keys())
    n = len(keys)
    t = 0
    for i in range(n):
        ith = keys[i]
        for j in range(i+1, n):
            jth = keys[j]
            if jth not in edges[ith]:
                continue
            for k in range(j+1, n):
                kth = keys[k]
                if kth not in edges[jth] or kth not in edges[ith]:
                    continue
                if any(x.startswith('t') for x in [ith, jth, kth]):
                    t += 1
    return t


def solve_part_two(fname):
    edges = parse(fname)

    @cache
    def find_completely_connected(cur, cc):
        max_cc = cc
        for adj in edges[cur]:
            if adj in cc or not cc.issubset(edges[adj]):
                # skip if adj is not fully connected to existing component
                # or already in existing component
                continue
            candidate = find_completely_connected(adj, cc | frozenset([adj]))
            if len(max_cc) < len(candidate):
                max_cc = candidate
        return max_cc

    max_cc = frozenset()
    for key in edges.keys():
        candidate = find_completely_connected(key, frozenset([key]))
        if len(max_cc) < len(candidate):
            max_cc = candidate
    return ','.join(sorted(list(max_cc)))


def run_solution(day, ignore_example=False, ex_answer_1=7, ex_answer_2='co,de,ka,ta'):
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
