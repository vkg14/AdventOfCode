import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse_tuple(s):
    tup = s.split('=')[1]
    return tuple(int(t) for t in tup.split(','))

def parse(fname):
    content = get_readlines_stripped(fname)
    robots = []
    for line in content:
        pos, vel = line.split()
        robots.append([parse_tuple(pos), parse_tuple(vel)])
    return robots


def solve_part_one(fname, is_example=False):
    robots = parse(fname)
    max_x = 11 if is_example else 101
    max_y = 7 if is_example else 103
    final_positions = []
    for pos, vel in robots:
        r = sum_tuples(pos, mul_tuple(vel, 100))
        modded = (r[0] % max_x, r[1] % max_y)
        final_positions.append(modded)

    total = [0, 0, 0, 0]
    for x, y in final_positions:
        if x < (max_x - 1) // 2 and y < (max_y - 1) // 2:
            total[0] += 1
        elif x > (max_x - 1) // 2 and y < (max_y - 1) // 2:
            total[1] += 1
        elif x < (max_x - 1) // 2 and y > (max_y - 1) // 2:
            total[2] += 1
        elif x > (max_x - 1) // 2 and y > (max_y - 1) // 2:
            total[3] += 1

    return reduce(lambda x, y: x * y, total)


def check_for_consecutive_line(robots, line_sz=10):
    sorted_robots = sorted(robots)
    last_x = -1
    last_y = -1
    consecutive = 0
    for x, y in sorted_robots:
        if x == last_x and y == last_y + 1:
            consecutive += 1
        else:
            consecutive = 1
        last_x = x
        last_y = y
        if consecutive == line_sz:
            return True
    return False


def solve_part_two(fname, is_example=False):
    robots = parse(fname)
    max_x = 11 if is_example else 101
    max_y = 7 if is_example else 103
    curr_robots = robots
    second = 0
    while True:
        second += 1
        nxt_robots = []
        for pos, vel in curr_robots:
            nxt = sum_tuples(pos, vel)
            nxt_modded = nxt[0] % max_x, nxt[1] % max_y
            nxt_robots.append((nxt_modded, vel))
        if check_for_consecutive_line([r[0] for r in nxt_robots]):
            return second
        curr_robots = nxt_robots


def run_solution(day, ignore_example=False, ex_answer_1=12, ex_answer_2=0):
    example_file = f'examples/example{day}.txt'
    input_file = f'inputs/input{day}.txt'

    if not ignore_example:
        p1 = solve_part_one(example_file, True)
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
