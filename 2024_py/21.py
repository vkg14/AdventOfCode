import os
import re
import sys
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from heapq import heappush, heappop
from itertools import permutations

from helpers import *

NUMERIC_KEYPAD = [[7, 8, 9], [4, 5, 6], [1, 2, 3], ['.', 0, 'A']]

DIRECTIONAL_KEYPAD = ['.^A', '<v>']


def transform_grid_as_map(grid):
    res = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            res[(r, c)] = grid[r][c]
    return res


def parse(fname):
    return get_readlines_stripped(fname)


def all_pairs_sp(graph):
    m = max(r+1 for r, _ in graph.keys())
    n = max(c+1 for _, c in graph.keys())

    def bfs(start_pos):
        q = deque([(start_pos, 0, '')])
        start = graph[start_pos]
        best = {start: 0, '.': 0}
        paths = defaultdict(list)
        while q:
            pos, step, path = q.popleft()
            cur = graph[pos]
            paths[cur].append(path + 'A')

            for d, d_sign in zip(DIRS, DIR_SIGNS):
                nxt_pos = sum_tuples(pos, d)
                if not in_bounds(nxt_pos, m, n):
                    continue

                nxt = graph[nxt_pos]
                if nxt not in best or best[nxt] == step+1:
                    best[nxt] = step+1
                    q.append((nxt_pos, step + 1, path + d_sign))

        return paths

    all_pairs = {}
    for r in range(m):
        for c in range(n):
            cell = (r, c)
            button = graph[cell]
            if button != '.':
                all_pairs[button] = bfs(cell)
    return all_pairs


def get_input_sequence(numeric_apsp, directional_apsp, code, top_layer, debug=False):
    @cache
    def min_path(seq, layer):
        curr = 'A'
        total_length = 0
        input_sequence = ''
        apsp = numeric_apsp if layer == top_layer else directional_apsp
        for char_s in seq:
            char = int(char_s) if char_s.isdigit() else char_s

            if layer == 0:
                first = apsp[curr][char][0]
                total_length += len(first)
                # building the actual sequence here will overflow pt2 so hide behind debug flag
                input_sequence += first if debug else ''
            else:
                min_seen = sys.maxsize
                min_seq = ''
                for nxt_path in apsp[curr][char]:
                    length, sequence = min_path(nxt_path, layer-1)
                    if length < min_seen:
                        min_seen = length
                        min_seq = sequence
                total_length += min_seen
                input_sequence += min_seq

            curr = char
        return total_length, input_sequence

    return min_path(code, top_layer)


def solve_part_one(fname):
    numeric_keypad_graph = transform_grid_as_map(NUMERIC_KEYPAD)
    apsp_numeric_keypad = all_pairs_sp(numeric_keypad_graph)

    directional_keypad_graph = transform_grid_as_map(DIRECTIONAL_KEYPAD)
    apsp_directional_keypad = all_pairs_sp(directional_keypad_graph)

    codes = parse(fname)
    t = 0
    for code in codes:
        length, _ = get_input_sequence(apsp_numeric_keypad, apsp_directional_keypad, code, 2)
        t += length * int(code.lstrip('0')[:-1])
    return t


def solve_part_two(fname):
    numeric_keypad_graph = transform_grid_as_map(NUMERIC_KEYPAD)
    apsp_numeric_keypad = all_pairs_sp(numeric_keypad_graph)

    directional_keypad_graph = transform_grid_as_map(DIRECTIONAL_KEYPAD)
    apsp_directional_keypad = all_pairs_sp(directional_keypad_graph)

    codes = parse(fname)
    t = 0
    for code in codes:
        length, _ = get_input_sequence(apsp_numeric_keypad, apsp_directional_keypad, code, 25)
        t += length * int(code.lstrip('0')[:-1])
    return t


def run_solution(day, ignore_example=False, ex_answer_1=126384):
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
