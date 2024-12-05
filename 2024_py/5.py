import os
import re
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *


def helper(fname):
    with open(fname, "r") as f:
        content = f.read()
    first, second = content.split("\n\n")
    mappings = defaultdict(set)
    for l in first.split('\n'):
        x, y = [int(z) for z in l.split('|')]
        mappings[x].add(y)
    correct = []
    incorrect = []
    for l in second.split('\n'):
        items = [int(z) for z in l.split(',')]
        success = True
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                if items[i] in mappings[items[j]]:
                    success = False
                    incorrect.append(items)
                    break
            if not success:
                break
        if success:
            correct.append(items)
    return correct, incorrect, mappings


def solve_part_one(fname):
    correct, _, _= helper(fname)
    return sum(x[len(x)//2] for x in correct)


def solve_part_two(fname):
    _, incorrect, mappings = helper(fname)

    def topological_sort(graph, universe):
        visited = set()
        stack = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor in universe:
                        dfs(neighbor)
                stack.append(node)

        for node in universe:
            dfs(node)

        return stack[::-1]

    s = 0
    for uni in incorrect:
        order = topological_sort(mappings, uni)
        s += order[len(order)//2]

    return s


def run_solution(day, ignore_example=False, ex_answer_1=143, ex_answer_2=123):
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
