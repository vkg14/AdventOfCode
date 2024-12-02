import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def solve_part_one(fname):
    lines = read_file_split(fname)
    first = sorted(x[0] for x in lines)
    second = sorted(x[1] for x in lines)
    t = 0
    for f, s in zip(first, second):
        t += abs(int(f)-int(s))
    return t


def solve_part_two(fname):
    lines = read_file_split(fname)
    counter = Counter(x[1] for x in lines)
    t = 0
    for x in [e[0] for e in lines]:
        t += int(x) * counter[x]
    return t


def run_solution(day, ignore_example=False, ex_answer_1=11, ex_answer_2=31):
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
