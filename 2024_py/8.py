import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    with open(fname, "r") as f:
        content = [l.strip() for l in f.readlines()]
    mapping = defaultdict(list)
    m = len(content)
    n = len(content[0])
    for r, line in enumerate(content):
        for c, char in enumerate(line):
            if char == ".":
                continue
            mapping[char].append((r,c))
    return mapping, m, n


def solve_part_one(fname):
    mapping, m, n = parse(fname)
    antinodes = set()
    for char in mapping:
        points = mapping[char]
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                diff = diff_tuples(points[i], points[j])
                first = sum_tuples(points[i], diff)
                second = diff_tuples(points[j], diff)
                if in_bounds(first, m, n):
                    antinodes.add(first)
                if in_bounds(second, m, n):
                    antinodes.add(second)
    return len(antinodes)


def solve_part_two(fname):
    mapping, m, n = parse(fname)
    antinodes = set()
    for char in mapping:
        points = mapping[char]
        if len(points) < 2:
            continue
        for i in range(len(points)):
            antinodes.add(points[i])
            for j in range(i+1, len(points)):
                diff = diff_tuples(points[i], points[j])
                first = sum_tuples(points[i], diff)
                while in_bounds(first, m, n):
                    antinodes.add(first)
                    first = sum_tuples(first, diff)
                second = diff_tuples(points[j], diff)
                while in_bounds(second, m, n):
                    antinodes.add(second)
                    second = diff_tuples(second, diff)
    return len(antinodes)


def run_solution(day, ignore_example=False, ex_answer_1=14, ex_answer_2=34):
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
