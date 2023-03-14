import copy
import heapq
from collections import defaultdict
from collections.abc import Set
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


@dataclass
class Solver:
    board: List[List[str]]
    use_cached: bool = False
    row_remaining: Dict[int, Set[int]] = field(default_factory=dict)
    col_remaining: Dict[int, Set[int]] = field(default_factory=dict)
    box_remaining: Dict[int, Set[int]] = field(default_factory=dict)

    def __post_init__(self):
        if not self.use_cached:
            return
        # Cache the remaining numbers for each row/col/box and set/unset during backtracking
        for i in range(len(self.board)):
            self.row_remaining[i] = self.get_remaining_in_row(i)
            self.col_remaining[i] = self.get_remaining_in_col(i)
            self.box_remaining[i] = self.get_remaining_in_box_from_id(i)

    @staticmethod
    def _get_box_id(r, c):
        """
        We assign a box ID of [0, 9) from top left to bottom right.
        """
        return r // 3 * 3 + c // 3

    def get_remaining_in_row(self, r):
        placed = set([int(x) for x in self.board[r] if x != '.'])
        return set(range(1, 10)) - placed

    def get_remaining_in_col(self, c):
        placed = set([int(self.board[r][c]) for r in range(9) if self.board[r][c] != '.'])
        return set(range(1, 10)) - placed

    def get_remaining_in_box_from_id(self, box_id):
        """
        Takes a box ID.
        """
        r = (box_id // 3) * 3
        c = (box_id % 3) * 3
        return self.get_remaining_in_box(r, c)

    def get_remaining_in_box(self, r, c):
        row_base = r // 3 * 3
        col_base = c // 3 * 3
        placed = set(range(1, 10))
        for r1 in range(row_base, row_base + 3):
            for c1 in range(col_base, col_base + 3):
                if self.board[r1][c1] != '.':
                    placed.remove(int(self.board[r1][c1]))
        return placed

    def get_remaining_for_cell(self, r, c):
        """
        When using "use_cached", the runtime of this method is significantly reduced thus
        confirming improvements of maintaining a hash set rather than recomputing the remaining elements.
        Where we save:
        - no need to read the row / col / box for every cell we explore to compute what needs to be filled in each.
        Where we gain nothing:
        - intersection still needs to be done.
        """
        if not self.use_cached:
            rem_row = self.get_remaining_in_row(r)
            rem_col = self.get_remaining_in_col(c)
            rem_box = self.get_remaining_in_box(r, c)
            return rem_row.intersection(rem_col).intersection(rem_box)
        else:
            rem_row = self.row_remaining[r]
            rem_col = self.col_remaining[c]
            box = self._get_box_id(r, c)
            rem_box = self.box_remaining[box]
            return rem_row.intersection(rem_col).intersection(rem_box)

    @staticmethod
    def get_next_cell(r, c):
        if c < 8:
            return r, c + 1
        elif r < 8:
            return r + 1, 0
        else:
            return None

    def find_next_empty(self, cell) -> Optional[Tuple[int, int]]:
        nxt = self.get_next_cell(*cell)
        while nxt:
            r, c = nxt
            if self.board[r][c] == '.':
                return nxt
            nxt = self.get_next_cell(r, c)
        return None

    def construct_pri_queue(self):
        heap = []
        for r in range(9):
            for c in range(9):
                if self.board[r][c].isdigit():
                    continue
                n = len(self.get_remaining_for_cell(r, c))
                heap.append((n, (r, c)))
        heapq.heapify(heap)
        return heap

    def set_immediately_solvable(self):
        """
        Find items in the board which are immediately solvable (only have 1 possible assignment) and assign them.
        """
        res = False
        for r in range(9):
            for c in range(9):
                if self.board[r][c].isdigit():
                    continue
                rem = self.get_remaining_for_cell(r, c)
                if len(rem) == 0:
                    raise Exception(f"Found item ({r},{c}) with 0 valid entries\n{self.board}\n.")
                elif len(rem) == 1:
                    val = next(iter(rem))
                    self.assign_val(r, c, val)
                    res = True
        return res

    def find_min_constrained(self):
        m = 9
        cell = (-1, -1)
        for r in range(9):
            for c in range(9):
                if self.board[r][c].isdigit():
                    continue
                n_candidates = len(self.get_remaining_for_cell(r, c))
                if n_candidates <= 1:
                    # Short circuit on either a no solution or single solution cell
                    return r, c
                elif n_candidates < m:
                    m = n_candidates
                    cell = r, c
        return cell if m < 9 else None

    def solve_sudoku(self) -> None:
        """
        This sudoku solver follows 2 steps:
        - fill in all single-candidate cells until there are no more
        - find the least constrained cell, try a solution and propagate forward, backtracking if necessary
        """
        while self.set_immediately_solvable():
            # Repeatedly fill-in all 1-candidate cells till there are no more.
            pass

        first_empty = self.find_min_constrained()
        if not first_empty or self.recursive_solver(first_empty):
            print("SOLVED!")
        else:
            print("UNSOLVABLE!")

    def assign_val(self, r, c, val):
        self.board[r][c] = str(val)
        if self.use_cached:
            self.row_remaining[r].remove(val)
            self.col_remaining[c].remove(val)
            box = self._get_box_id(r, c)
            self.box_remaining[box].remove(val)

    def unassign_val(self, r, c, val):
        self.board[r][c] = '.'
        if self.use_cached:
            self.row_remaining[r].add(val)
            self.col_remaining[c].add(val)
            box = self._get_box_id(r, c)
            self.box_remaining[box].add(val)

    def recursive_solver(self, cell):
        r, c = cell
        for val in self.get_remaining_for_cell(r, c):
            self.assign_val(r, c, val)
            nxt_cell = self.find_min_constrained()
            if not nxt_cell or self.recursive_solver(nxt_cell):
                # done
                return True
            self.unassign_val(r, c, val)
        return False


if __name__ == '__main__':
    use_cached = True
    board = [["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."],
             [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
             ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
             [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"],
             [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    solver = Solver(board, use_cached=use_cached)
    solver.solve_sudoku()
    print(solver.board)
    with open("inputs/impossible_finnish_sudoku.txt") as f:
        board = [row.split() for row in f.read().split('\n')]
        solver = Solver(board, use_cached=use_cached)
        solver.solve_sudoku()
        print(solver.board)
