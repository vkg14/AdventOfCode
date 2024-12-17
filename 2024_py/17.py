import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def parse(fname):
    with open(fname, "r") as f:
        registers, program = [x.strip() for x in f.read().split('\n\n')]
    parsed_reg = []
    for reg in registers.split('\n'):
        parsed_reg.append(int(reg.split(': ')[1].strip()))
    program = [int(x) for x in program.split(': ')[1].split(',')]
    return parsed_reg, program


def run_program(i, program, a, b, c):
    combo_operands = {0: 0,
                      1: 1,
                      2: 2,
                      3: 3,
                      4: a,
                      5: b,
                      6: c}
    if program[i] == 0:
        # print(f"a = a // 2^(combo({[program[i+1]]})")
        new_a = a // 2**(combo_operands[program[i+1]])
        return i+2, new_a, b, c, -1
    elif program[i] == 1:
        # print(f"b = b ^ {program[i+1]}")
        new_b = b ^ program[i+1]
        return i+2, a, new_b, c, -1
    elif program[i] == 2:
        # print(f"b = combo({program[i+1]}) mod 8")
        new_b = combo_operands[program[i+1]] % 8
        return i+2, a, new_b, c, -1
    elif program[i] == 3:
        # print(f"jump {program[i+1]}")
        if a == 0:
            return i+2, a, b, c, -1
        else:
            return program[i+1], a, b, c, -1
    elif program[i] == 4:
        # print("b = b ^ c")
        new_b = b ^ c
        return i+2, a, new_b, c, -1
    elif program[i] == 5:
        # print(f"output -> combo({program[i+1]}) mod 8")
        output = combo_operands[program[i+1]] % 8
        return i+2, a, b, c, output
    elif program[i] == 6:
        # print(f"b = a // 2^(combo({[program[i+1]]})")
        new_b = a // 2**(combo_operands[program[i+1]])
        return i+2, a, new_b, c, -1
    elif program[i] == 7:
        # print(f"c = a // 2^(combo({[program[i+1]]})")
        new_c = a // 2**(combo_operands[program[i+1]])
        return i+2, a, b, new_c, -1


def run(a, b, c, program):
    i = 0
    res = []
    while i < len(program):
        i, a, b, c, output = run_program(i, program, a, b, c)
        if output >= 0:
            res.append(output)

    return res


def solve_part_one(fname):
    registers, program = parse(fname)
    a, b, c = registers
    return ','.join(str(x) for x in run(a, b, c, program))


"""
2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0 -> 

b = a mod 8
b = b ^ 5
c = a // 2**(b)
b = b ^ 6
a = a // 8
b = b ^ c
output -> b mod 8
jump 0

- Only the last 3 bits of A matter for each iteration's output (b = a mod 8) ??
- A gets last 3 bits truncated in each iter (a // 8)
- B and C get reset during each iteration based on A
"""
def solve_part_two(fname):
    registers, program = parse(fname)

    def get_min_a_recurse(idx, prev):
        for incr in range(8):
            nxt = prev * 8 + incr
            if run(nxt, 0, 0, program) == program[idx:]:
                if idx == 0:
                    return nxt
                ret = get_min_a_recurse(idx - 1, nxt)
                if ret >= 0:
                    return ret
        return -1

    return get_min_a_recurse(len(program) - 1, 0)


def run_solution(day, ignore_example=True, ex_answer_1="4,6,3,5,6,3,5,2,1,0", ex_answer_2=0):
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
