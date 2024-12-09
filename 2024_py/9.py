import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse_one(fname):
    with open(fname, "r") as f:
        content = f.read().strip()
    idx = 0
    fn = 0
    free_spaces = []
    occupied = []
    for i, n in enumerate(content):
        n = int(n)
        if i % 2 == 1:
            free_spaces.extend([idx + i for i in range(n)])
            idx += n
            occupied.extend([-1 for _ in range(n)])
        else:
            for j in range(n):
                occupied.append(fn)
            fn += 1
            idx += n
    return free_spaces, occupied


def compute_checksum(final_spaces):
    return sum([k * v if v != -1 else 0 for k, v in enumerate(final_spaces)])


def solve_part_one(fname):
    free_spaces, occupied = parse_one(fname)
    last = len(occupied) - 1
    for nidx in free_spaces:
        while occupied[last] == -1:
            last -= 1
            occupied.pop()
        if last < nidx:
            break
        occupied[nidx] = occupied[last]
        last -= 1
        occupied.pop()
    return compute_checksum(occupied)


def parse_two(fname):
    # same as parse_one except free_spaces is List[tuple]
    with open(fname, "r") as f:
        content = f.read().strip()
    idx = 0
    fn = 0
    free_spaces = []
    occupied = []
    for i, n in enumerate(content):
        n = int(n)
        if i % 2 == 1:
            free_spaces.append((idx, n))
            idx += n
            occupied.extend([-1 for _ in range(n)])
        else:
            for j in range(n):
                occupied.append(fn)
            fn += 1
            idx += n
    return free_spaces, occupied


def insert_into_empty_slot(start, sz, fn, free_spaces, occupied):
    for i in range(len(free_spaces)):
        free_start, free_sz = free_spaces[i]
        if start <= free_start:
            # Don't move things forward
            return
        if sz <= free_sz:
            # Found a slot to insert!
            for j in range(sz):
                occupied[free_start+j] = fn
                occupied[start+j] = -1
            # Adjust free_spaces with new size and start
            free_spaces[i] = free_start + sz, free_sz - sz
            return


def solve_part_two(fname):
    free_spaces, occupied = parse_two(fname)
    last = len(occupied) - 1
    while last >= 0:
        while occupied[last] == -1:
            last -= 1
        start = last
        while start > 0 and occupied[start-1] == occupied[start]:
            start -= 1
        sz = last - start + 1
        fn = occupied[start]
        insert_into_empty_slot(start, sz, fn, free_spaces, occupied)
        # Make sure to set last correctly
        last = start - 1
    return compute_checksum(occupied)


def run_solution(day, ignore_example=False, ex_answer_1=1928, ex_answer_2=2858):
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
