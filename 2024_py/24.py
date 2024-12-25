import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from heapq import heappush, heappop

from helpers import *

def parse_gates(eqs):
    gate_type = {}
    deps = {}
    for l in eqs.split('\n'):
        lhs, rhs = l.strip().split(' -> ')
        arg1, gate, arg2 = lhs.strip().split()
        gate_type[rhs] = gate
        deps[rhs] = [arg1, arg2]
    return gate_type, deps


def parse(fname):
    with open(fname) as f:
        vals, eqs = f.read().split('\n\n')
    values = dict(tuple(l.strip().split(': ') for l in vals.split('\n')))
    for k in values.keys():
        values[k] = int(values[k])
    gate_type, deps = parse_gates(eqs)
    return values, gate_type, deps


def find_binary(letter, values):
    return sum(values[f] * (2**i) for i, f in enumerate(sorted(k for k in values.keys() if k.startswith(letter))))


def find_binary_rep(letter, values):
    return list(values[f] for f in sorted(k for k in values.keys() if k.startswith(letter)))


def find_indices_of_ones(n):
    return [i for i, bit in enumerate(bin(n)[:1:-1]) if bit == '1']


def search_part_one(values, gate_type, deps):
    output_gate_deps = defaultdict(set)

    def dfs(cur):
        if not any(cur.startswith(sw) for sw in 'xyz'):
            output_gate_deps[node].add(cur)

        if cur in values:
            return values[cur]

        v1, v2 = [dfs(nxt) for nxt in deps[cur]]
        if gate_type[cur] == 'XOR':
            ret = v1 ^ v2
        elif gate_type[cur] == 'AND':
            ret = v1 & v2
        else:
            assert gate_type[cur] == 'OR', f"Unknown gate {gate_type[cur]}"
            ret = v1 | v2

        values[cur] = ret
        return ret

    for node in deps.keys():
        if node.startswith('z'):
            dfs(node)

    return values, output_gate_deps


def solve_part_one(fname):
    values, _ = search_part_one(*parse(fname))
    return find_binary('z', values)


def solve_part_two(fname):
    values, gate_type, deps = parse(fname)
    for k, v in deps.items():
        if any(dep.startswith('z') for dep in v):
            raise Exception(f"{k} has dependence on z-gates: {v}.")

    x_rep = find_binary('x', values)
    y_rep = find_binary('y', values)

    p1_solved, output_gate_deps = search_part_one(*parse(fname))
    z_rep = find_binary('z', p1_solved)
    ones = find_indices_of_ones(z_rep - (x_rep + y_rep))
    bad_z_gates = ['z' + str(g).zfill(2) for g in ones]
    print(bad_z_gates)

    @cache
    def gate_repr(cur, depth=0):
        if cur in values or depth >= 3:
            return cur

        cur1 = gate_repr(deps[cur][0], depth + 1)
        cur2 = gate_repr(deps[cur][1], depth + 1)
        if gate_type[cur] == "AND":
            return f"{cur}{{({cur1}) & ({cur2})}}"
        if gate_type[cur] == "OR":
            return f"{cur}{{({cur1}) | ({cur2})}}"
        if gate_type[cur] == "XOR":
            return f"{cur}{{({cur1}) ^ ({cur2})}}"


    # z14, z18, z23, and z34 are incorrect
    print(gate_repr("z13"))
    # hbk and z14 need to be swapped bc z14 ==> z15 without 15 sum bit
    print(gate_repr("z14"))
    print(gate_repr("bfn"))
    print(gate_repr("hbk"))
    print(gate_repr("z15"))
    print(gate_repr("z16"))
    print('\n')
    print(gate_repr("z17"))
    print(gate_repr("z18"))
    print(gate_repr("z19"))
    # kvn needs to be swapped with z18 directly
    print(gate_repr("kvn"))
    print('\n')
    # & instead of | between carry and sum bits
    print(gate_repr("z22"))
    print(gate_repr("z23"))
    print(gate_repr("dvw"))
    print(gate_repr("jbb"))
    print(gate_repr("vvk"))
    print(gate_repr("z24"))
    # dbb is just z23
    print(gate_repr("dbb"))
    print('\n')
    # cvh and tfn to swap sum and carry bits of 34/35
    print(gate_repr("z34"))
    print(gate_repr("z35"))
    print(gate_repr("z36"))
    print('\n')

    return ','.join(sorted(['cvh', 'tfn', 'kvn', 'z18', 'hbk', 'z14', 'dbb', 'z23']))


def run_solution(day, ignore_example=False, ex_answer_1=2024):
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
