import copy
import operator
import random

from tabulate import tabulate


class Shape:
    I = [
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    ]

    def __init__(self, r, c, orientations):
        self.r = r
        self.c = c
        self.orientations = orientations
        self.rotation = 0

    @staticmethod
    def make_random_shape(r, c):
        shapes = [Shape.I]
        return Shape(r, c, random.choice(shapes))

    def set_offset(self, direction):
        self.r, self.c = add_tuples((self.r, self.c), direction)

    def get_absolute_shape_position(self):
        positions = []
        m = len(self.orientations[self.rotation])
        n = len(self.orientations[self.rotation][0])
        for r in range(m):
            for c in range(n):
                if self.orientations[self.rotation][r][c]:
                    positions.append((r + self.r, c + self.c))
        return positions

    def rotate(self, offset):
        self.rotation = (self.rotation + offset) % 4


def add_tuples(t1, t2):
    return tuple(map(operator.add, t1, t2))


def move_positions(positions, direction):
    return [add_tuples(position, direction) for position in positions]


class Tetris:
    DOWN = 'D'
    DIR_INPUTS = {
        'L': (0, -1),
        'R': (0, 1),
        DOWN: (1, 0)
    }

    ROT_INPUTS = {'RR': 1, 'LR': -1}

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0] * width for _ in range(height)]
        self.falling_shape = self.spawn_shape()
        self.score = 0

    def spawn_shape(self):
        # TOD0: change spawn place
        return Shape.make_random_shape(0, self.width//2)

    def _is_in_bounds(self, r, c):
        return 0 <= r < self.height and 0 <= c < self.width

    def does_collide(self, positions):
        for r, c in positions:
            if not self._is_in_bounds(r, c) or self.board[r][c]:
                return True
        return False

    def clear_row(self, row):
        self.board.pop(row)
        self.board.insert(0, [0] * self.width)

    def lock_shape_into_grid(self):
        positions = self.falling_shape.get_absolute_shape_position()
        check_rows = set()
        for r, c in positions:
            self.board[r][c] = 1
            check_rows.add(r)
        for row in check_rows:
            if all(x for x in self.board[row]):
                self.clear_row(row)
        self.falling_shape = self.spawn_shape()

    def process_input(self, inp):
        if inp in self.ROT_INPUTS:
            offset = self.ROT_INPUTS[inp]
            undo = offset * -1
            self.falling_shape.rotate(offset)
            positions = self.falling_shape.get_absolute_shape_position()
            if self.does_collide(positions):
                self.falling_shape.rotate(undo)
        elif inp in self.DIR_INPUTS:
            direction = self.DIR_INPUTS[inp]
            nxt_position = move_positions(self.falling_shape.get_absolute_shape_position(), direction)
            if not self.does_collide(nxt_position):
                self.falling_shape.set_offset(direction)
            elif inp == self.DOWN:
                self.lock_shape_into_grid()

    def show_board(self):
        board_copy = copy.deepcopy(self.board)
        for r, c in self.falling_shape.get_absolute_shape_position():
            board_copy[r][c] = '#'
        print("******************")
        print(tabulate(board_copy))
        print("******************")


if __name__ == '__main__':
    tetris = Tetris(10, 10)
    tetris.show_board()
    while True:
        inp = input()
        if inp == 'E':
            break
        tetris.process_input(inp)
        tetris.show_board()
