import copy
from collections import deque
from dataclasses import dataclass, field
from operator import add
from typing import List


@dataclass
class CountFlashes:
    grid: List[List[int]] = field(default_factory=list)
    flashes: int = 0

    ADJACENTS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
    DIM = 10

    def in_bounds(self, r, c):
        return 0 <= r < self.DIM and 0 <= c < self.DIM

    @staticmethod
    def add_tuple(left, right):
        return tuple(map(add, left, right))

    def explore_flash(self, r, c):
        # Set to flashed
        self.grid[r][c] = 0
        self.flashes += 1
        for adj in self.ADJACENTS:
            next_r, next_c = self.add_tuple((r, c), adj)
            if not self.in_bounds(next_r, next_c) or self.grid[next_r][next_c] == 0:
                # Out of bounds or already flashed this step
                continue
            self.grid[next_r][next_c] += 1
            if self.grid[next_r][next_c] > 9:
                self.explore_flash(next_r, next_c)

    def do_step(self):
        flashes_before = self.flashes
        flash_q = deque()
        for r in range(self.DIM):
            for c in range(self.DIM):
                self.grid[r][c] += 1
                if self.grid[r][c] > 9:
                    flash_q.appendleft((r, c))
        while flash_q:
            r, c = flash_q.pop()
            if self.grid[r][c] == 0:
                # already flashed
                continue
            self.explore_flash(r, c)

        flashes_after = self.flashes
        # When all flash simultaneously
        return flashes_after == flashes_before + 100


if __name__ == '__main__':
    with open('inputs/actual_day11.txt') as f:
        s = f.read().split('\n')
        grid = []
        for row in s:
            grid.append([int(x) for x in row])
    cf1 = CountFlashes(copy.deepcopy(grid))
    # Part A
    for _ in range(100):
        cf1.do_step()
    print(cf1.flashes)
    # Part B
    all_flashed = False
    cf2 = CountFlashes(copy.deepcopy(grid))
    step = 0
    while not all_flashed:
        step += 1
        all_flashed = cf2.do_step()
    print(step)
