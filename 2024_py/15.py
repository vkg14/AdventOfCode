import os
import re
import sys
from collections import defaultdict, Counter, deque
from functools import reduce
from heapq import heappush, heappop

from helpers import *

sys.setrecursionlimit(2000)

def parse_grid(grid):
    obstacles = set()
    boxes = set()
    start_pos = None
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "O":
                boxes.add((i, j))
            if char == "#":
                obstacles.add((i, j))
            elif char == "@":
                start_pos = (i, j)
    m = len(grid)
    n = len(grid[0])
    return obstacles, boxes, start_pos, m, n


def parse(fname):
    with open(fname, "r") as f:
        content = f.read()
    grid, moves = content.split("\n\n")
    obstacles, boxes, start_pos, m, n = parse_grid(grid.split('\n'))
    all_moves = ''.join(moves.split('\n'))
    return obstacles, boxes, start_pos, m, n, all_moves


def try_move_box(obstacles, boxes, d, box_pos):
    nxt_pos = sum_tuples(d, box_pos)
    if nxt_pos in obstacles:
        # Can't move
        return False
    if nxt_pos not in boxes:
        boxes.remove(box_pos)
        boxes.add(nxt_pos)
        return True
    # recurse
    if try_move_box(obstacles, boxes, d, nxt_pos):
        boxes.remove(box_pos)
        boxes.add(nxt_pos)
        return True
    else:
        return False


def solve_part_one(fname):
    obstacles, boxes, start_pos, m, n, all_moves = parse(fname)
    char_to_dirs = ['>', 'v', '<', '^']
    curr = start_pos
    for move in all_moves:
        idx = char_to_dirs.index(move)
        d = DIRS[idx]
        nxt_pos = sum_tuples(curr, d)
        if nxt_pos in obstacles:
            continue
        elif nxt_pos in boxes:
            if try_move_box(obstacles, boxes, d, nxt_pos):
                # Successfully moved box
                curr = nxt_pos
        else:
            curr = nxt_pos

    t = 0
    for r, c in boxes:
        t += 100 * r + c
    return t


def parse_grid_two(grid):
    obstacles = set()
    left_boxes = set()
    right_boxes = set()
    start_pos = None
    for i, line in enumerate(grid):
        j_offset = 0
        for j, char in enumerate(line):
            j_actual = j + j_offset
            if char == "O":
                left_boxes.add((i, j_actual))
                right_boxes.add((i, j_actual + 1))
                j_offset += 1
            if char == "#":
                obstacles.add((i, j_actual))
                obstacles.add((i, j_actual+1))
                j_offset += 1
            elif char == "@":
                start_pos = (i, j_actual)
                j_offset += 1
            elif char == ".":
                j_offset += 1
    m = len(grid)
    n = max(c+1 for _, c in obstacles)
    return obstacles, left_boxes, right_boxes, start_pos, m, n


def parse_two(fname):
    with open(fname, "r") as f:
        content = f.read()
    grid, moves = content.split("\n\n")
    obstacles, l_boxes, r_boxes, start_pos, m, n = parse_grid_two(grid.split('\n'))
    all_moves = ''.join(moves.split('\n'))
    return obstacles, l_boxes, r_boxes, start_pos, m, n, all_moves


def try_move_box_lr(obstacles, d, l_boxes, r_boxes, box_pos):
    nxt_pos = sum_tuples(d, box_pos)
    curr_boxes = r_boxes if box_pos in r_boxes else l_boxes
    other_boxes = l_boxes if box_pos in r_boxes else r_boxes
    if nxt_pos in obstacles:
        # Can't move
        return False
    # have to check other one
    if nxt_pos not in other_boxes:
        curr_boxes.remove(box_pos)
        curr_boxes.add(nxt_pos)
        return True
    # recurse
    if try_move_box_lr(obstacles, d, l_boxes, r_boxes, nxt_pos):
        curr_boxes.remove(box_pos)
        curr_boxes.add(nxt_pos)
        return True
    else:
        return False


def can_move_box_ud(obstacles, d, l_boxes, r_boxes, box_pos):
    is_right = box_pos in r_boxes
    pair_box = sum_tuples(box_pos, (0, -1)) if is_right else sum_tuples(box_pos, (0, 1))
    for b in [box_pos, pair_box]:
        nxt_pos = sum_tuples(b, d)
        if nxt_pos in obstacles:
            return False
        if nxt_pos in l_boxes or nxt_pos in r_boxes:
            if not can_move_box_ud(obstacles, d, l_boxes, r_boxes, nxt_pos):
                return False
    return True


def do_move_box_ud(d, l_boxes, r_boxes, box_pos):
    if box_pos not in l_boxes and box_pos not in r_boxes:
        return

    if box_pos in r_boxes:
        l_box = sum_tuples(box_pos, (0, -1))
        r_box = box_pos
    else:
        l_box = box_pos
        r_box = sum_tuples(box_pos, (0, 1))

    for b in [l_box, r_box]:
        nxt_pos = sum_tuples(b, d)
        do_move_box_ud(d, l_boxes, r_boxes, nxt_pos)

    l_boxes.remove(l_box)
    l_boxes.add(sum_tuples(l_box, d))
    r_boxes.remove(r_box)
    r_boxes.add(sum_tuples(r_box, d))
    return


def solve_part_two(fname):
    obstacles, l_boxes, r_boxes, start_pos, m, n, all_moves = parse_two(fname)
    char_to_dirs = ['>', 'v', '<', '^']
    curr = start_pos
    for move in all_moves:
        idx = char_to_dirs.index(move)
        d = DIRS[idx]
        nxt_pos = sum_tuples(curr, d)
        if nxt_pos in obstacles:
            continue
        elif nxt_pos in l_boxes or nxt_pos in r_boxes:
            if idx % 2 == 0 and try_move_box_lr(obstacles, d, l_boxes, r_boxes, nxt_pos):
                curr = nxt_pos
            elif idx % 2 == 1 and can_move_box_ud(obstacles, d, l_boxes, r_boxes, nxt_pos):
                do_move_box_ud(d, l_boxes, r_boxes, nxt_pos)
                curr = nxt_pos
        else:
            curr = nxt_pos

    t = 0
    for r, c in l_boxes:
        t += 100 * r + c
    return t


def run_solution(day, ignore_example=False, ex_answer_1=10092, ex_answer_2=9021):
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
