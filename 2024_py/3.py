import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def solve_part_one(fname):
    with open(fname, "r") as f:
        inp = ''.join(f.readlines())
    pattern = r"mul\((\d{1,}),(\d{1,})\)"
    matches = re.findall(pattern, inp)
    return sum(int(x) * int(y) for x, y in matches)


def is_do(s, i):
    pattern = r"^do\(\)"
    return len(re.findall(pattern, s[i:])) > 0


def is_dont(s, i):
    pattern = r"^don't\(\)"
    return len(re.findall(pattern, s[i:])) > 0


def get_mul(s, i):
    pattern = r"^mul\((\d{1,}),(\d{1,})\)"
    matches = re.findall(pattern, s[i:])
    if matches:
        return int(matches[0][0]) * int(matches[0][1])
    else:
        return 0


def solve_part_two(fname):
    with open(fname, "r") as f:
        inp = ''.join(f.readlines())
    activated = True
    s = 0
    for i in range(len(inp)):
        if is_do(inp, i):
            activated = True
        elif is_dont(inp, i):
            activated = False
        elif activated:
            s += get_mul(inp, i)
    return s


def run_solution(day, ignore_example=False, ex_answer_1=161, ex_answer_2=48):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    example_file = f'examples/example{day}b.txt'
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
