import abc
from dataclasses import dataclass


def read_input(filename):
    with open(filename) as f:
        for line in f:
            sp = list(line.rstrip('\n'))
            return [1 if x == '>' else -1 for x in sp]


@dataclass
class Shape(abc.ABC):
    x: int
    y: int

    @abc.abstractmethod
    def get_blocks(self):
        raise NotImplementedError("J")

    @staticmethod
    @abc.abstractmethod
    def make(max_y):
        raise NotImplementedError("J")

    def move_down(self, rocks):
        blocks = self.get_blocks()
        if any((x, y - 1) in rocks or y == 0 for x, y in blocks):
            return False
        self.y -= 1
        return True

    def move_left(self, rocks):
        blocks = self.get_blocks()
        if any((x - 1, y) in rocks or x == 0 for x, y in blocks):
            return False
        self.x -= 1

    def move_right(self, rocks):
        blocks = self.get_blocks()
        if any((x + 1, y) in rocks or x == 6 for x, y in blocks):
            return False
        self.x += 1


class FlatLine(Shape):
    def get_blocks(self):
        return [(self.x + i, self.y) for i in range(4)]

    @staticmethod
    def make(max_y):
        return FlatLine(2, max_y + 4)


class Cross(Shape):
    @staticmethod
    def make(max_y):
        return Cross(3, max_y + 5)

    def get_blocks(self):
        horiz = [(self.x + i, self.y) for i in range(-1, 2)]
        vert = [(self.x, self.y + i) for i in range(-1, 2)]
        return horiz + vert


class LShape(Shape):
    @staticmethod
    def make(max_y):
        return LShape(4, max_y + 4)

    def get_blocks(self):
        horiz = [(self.x - i, self.y) for i in range(3)]
        vert = [(self.x, self.y + i + 1) for i in range(2)]
        return horiz + vert


class VerticalLine(Shape):
    @staticmethod
    def make(max_y):
        return VerticalLine(2, max_y + 4)

    def get_blocks(self):
        return [(self.x, self.y + i) for i in range(4)]


class Square(Shape):
    @staticmethod
    def make(max_y):
        return Square(2, max_y + 4)

    def get_blocks(self):
        return [(self.x + i, self.y + j) for i in range(2) for j in range(2)]


def solve(filename, n=1000000000000):
    jetstream = read_input(filename)
    shapes = [FlatLine, Cross, LShape, VerticalLine, Square]
    shape_idx = 0
    gas_idx = 0
    max_y = -1
    current_shape = shapes[shape_idx].make(max_y)
    rocks = set()
    # New tracking for cycle detection
    peaks = [0] * 7
    states_seen = dict()
    max_heights = dict()
    while shape_idx < n:
        gas = jetstream[gas_idx % len(jetstream)]
        if gas == 1:
            current_shape.move_right(rocks)
        elif gas == -1:
            current_shape.move_left(rocks)
        gas_idx += 1
        fall_res = current_shape.move_down(rocks)
        if not fall_res:
            new_rocks = current_shape.get_blocks()
            old_max = max_y
            max_y = max(max_y, *[y for x, y in new_rocks])
            rocks.update(new_rocks)
            # Record peak shape
            max_heights[shape_idx] = max_y
            dy = max_y - old_max
            for i in range(len(peaks)):
                peaks[i] -= dy
            for x, y in new_rocks:
                peaks[x] = max(peaks[x], y - max_y)
            state = (shape_idx % len(shapes), gas_idx % len(jetstream), tuple(peaks))
            if state in states_seen and n > 10 ** 6:
                # Found cycle!
                n_prev_shape = states_seen[state]
                prev_max_h = max_heights[n_prev_shape]
                cycle_height_change = max_y - prev_max_h
                cycle_length = shape_idx - n_prev_shape
                target = n - n_prev_shape
                cycles = target // cycle_length
                leftover_height_change = max_heights[n_prev_shape + (target % cycle_length)] - prev_max_h
                return prev_max_h + (cycle_height_change * cycles) + leftover_height_change
            states_seen[state] = shape_idx
            # Move to next shape
            shape_idx += 1
            current_shape = shapes[shape_idx % len(shapes)].make(max_y)
    return max_y + 1


if __name__ == '__main__':
    print(solve("example17.txt", n=2022))
    print(solve("input17.txt", n=2022))
    print(solve("example17.txt"))
    print(solve("input17.txt"))
