import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def solve_part_one(fname):
    lines = read_file_split(fname)
    t = 0
    for line in lines:
        l = [int(i) for i in line]
        increasing = all(l[i] < l[i+1] for i in range(len(l)-1))
        decreasing = all(l[i] > l[i+1] for i in range(len(l)-1))
        diffs = all(abs(l[i+1] - l[i]) in [1,2,3] for i in range(len(l)-1))
        if (increasing or decreasing) and diffs:
            t += 1
    return t


def passes(l):
    increasing = all(l[i] < l[i + 1] for i in range(len(l) - 1))
    decreasing = all(l[i] > l[i + 1] for i in range(len(l) - 1))
    diffs = all(abs(l[i + 1] - l[i]) in [1, 2, 3] for i in range(len(l) - 1))
    return (increasing or decreasing) and diffs


def solve_part_two(fname):
    lines = read_file_split(fname)
    t = 0
    for line in lines:
        l = [int(i) for i in line]
        if passes(l):
            t += 1
            continue
        for i in range(len(l)):
            removed = [l[j] for j in range(len(l)) if j != i]
            if passes(removed):
                t += 1
                break
    return t


def run_solution(day, ignore_example=False, ex_answer_1=2, ex_answer_2=4):
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
