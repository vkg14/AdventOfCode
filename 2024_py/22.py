import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    numbers = [int(i) for i in get_readlines_stripped(fname)]
    return numbers


def evolve(n):
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    return ((n * 2048) ^ n) % 16777216


def solve_part_one(fname):
    nums = parse(fname)
    total = 0
    for num in nums:
        nxt = num
        for _ in range(2000):
            nxt = evolve(nxt)
        total += nxt
    return total


def run_diffs(num):
    last_dig = num % 10
    diffs = []
    prices = []
    for _ in range(2000):
        num = evolve(num)
        nxt_digit = num % 10
        diffs.append(nxt_digit - last_dig)
        prices.append(nxt_digit)
        last_dig = nxt_digit
    return diffs, prices[3:]


def solve_part_two(fname, example=False):
    nums = parse(fname)
    if example:
        nums = [1, 2, 3, 2024]
    profit = defaultdict(int)
    for num in nums:
        diffs, prices = run_diffs(num)
        seen = set()
        for i, px in enumerate(prices):
            last_diffs = tuple(diffs[i:i+4])
            if last_diffs not in seen:
                seen.add(last_diffs)
                profit[last_diffs] += px
    return max(profit.values())


def run_solution(day, ignore_example=False, ex_answer_1=37327623, ex_answer_2=23):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

    if not ignore_example:
        p2 = solve_part_two(example_file, example=True)
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
