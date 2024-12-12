import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    content = get_readlines_stripped(fname)
    return content[0].split()


def split_and_trim_to_int(s, first_half, ret_str=False):
    val = int(s[:len(s)//2]) if first_half else int(s[len(s)//2:])
    return str(val) if ret_str else val


def solve_part_one(fname):
    inp = parse(fname)
    nxt = []
    for _ in range(25):
        for num in inp:
            if num == '0':
                nxt.append('1')
            elif len(num) % 2 == 0:
                nxt.append(split_and_trim_to_int(num, True, True))
                nxt.append(split_and_trim_to_int(num, False, True))
            else:
                nxt.append(str(int(num)*2024))
        inp = nxt
        nxt = []
    return len(inp)


def solve_part_two(fname):
    inp = [int(e) for e in parse(fname)]
    iterations = 75

    @cache
    def apply_blink(num, blink):
        if blink == iterations:
            return 1
        if num == 0:
            return apply_blink(1, blink + 1)
        s = str(num)
        if len(s) % 2 == 0:
            return (apply_blink(split_and_trim_to_int(s, True), blink + 1)
                    + apply_blink(split_and_trim_to_int(s, False), blink + 1))
        return apply_blink(num * 2024, blink + 1)

    num_stones = 0
    for stone in inp:
        num_stones += apply_blink(stone, 0)
    return num_stones


def run_solution(day, ignore_example=False, ex_answer_1=55312, ex_answer_2=0):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file)
        print(p1)
        assert p1 == ex_answer_1, "Part 1 example case is incorrect."

    print("Solution to Part 1:", solve_part_one(input_file))
    print("\n**********************\n")

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
