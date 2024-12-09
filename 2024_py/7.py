import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse_line(line):
    first, last = line.strip().split(": ")
    nums = [int(i) for i in last.strip().split()]
    return int(first), nums


def can_compute(target, nums, curr):
    if len(nums) == 0:
        return curr == target
    if (can_compute(target, nums[1:], curr * nums[0])
            or can_compute(target, nums[1:], curr + nums[0])):
        return True


def solve_part_one(fname):
    content = get_readlines_stripped(fname)
    s = 0
    for line in content:
        ans, nums = parse_line(line)
        if can_compute(ans, nums[1:], nums[0]):
            s += ans
    return s


def concatenate(num1, num2):
    return int(str(num1) + str(num2))


def can_compute_two(target, nums, curr):
    if len(nums) == 0:
        return curr == target
    if (can_compute_two(target, nums[1:], curr * nums[0])
            or can_compute_two(target, nums[1:], concatenate(curr, nums[0]))
            or can_compute_two(target, nums[1:], curr + nums[0])):
        return True


def solve_part_two(fname):
    content = get_readlines_stripped(fname)
    s = 0
    for line in content:
        ans, nums = parse_line(line)
        if can_compute_two(ans, nums[1:], nums[0]):
            s += ans
    return s


def run_solution(day, ignore_example=False, ex_answer_1=3749, ex_answer_2=11387):
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
