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
        return True

    def move_right(self, rocks):
        blocks = self.get_blocks()
        if any((x + 1, y) in rocks or x == 6 for x, y in blocks):
            return False
        self.x += 1
        return True


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


def solve(filename, part_two=True):
    jetstream = read_input(filename)
    shapes = [FlatLine, Cross, LShape, VerticalLine, Square]
    shape_idx, gas_idx, max_y = 0, 0, -1
    n = 1000000000000 if part_two else 2022
    jetstream_methods = {-1: Shape.move_left, 1: Shape.move_right}
    rocks = set()
    # New tracking for cycle detection
    peaks = [0] * 7
    states_seen = dict()
    max_heights = dict()
    while shape_idx < n:
        current_shape = shapes[shape_idx % len(shapes)].make(max_y)
        still_falling = True
        while still_falling:
            jetstream_methods[jetstream[gas_idx % len(jetstream)]](current_shape, rocks)
            gas_idx += 1
            still_falling = current_shape.move_down(rocks)
        # Adjust rock set and height max
        new_rocks = current_shape.get_blocks()
        old_max = max_y
        max_y = max(max_y, *[y for x, y in new_rocks])
        rocks.update(new_rocks)
        # Record peak shape relative to the tallest column
        max_heights[shape_idx] = max_y
        dy = max_y - old_max
        for i in range(len(peaks)):
            peaks[i] -= dy
        for x, y in new_rocks:
            peaks[x] = max(peaks[x], y - max_y)
        state = (shape_idx % len(shapes), gas_idx % len(jetstream), tuple(peaks))
        if state in states_seen:
            # Found cycle!
            n_prev_shape = states_seen[state]
            prev_max_h = max_heights[n_prev_shape]
            cycle_height_change = max_y - prev_max_h
            cycle_length = shape_idx - n_prev_shape
            print(f'Found cycle from {n_prev_shape} to {shape_idx} with (h, l): {cycle_height_change}, {cycle_length}.')
            # Need to cycle simulate till shape_idx == n-1 (0-indexed)
            target = n - n_prev_shape - 1
            cycles = target // cycle_length
            # The excess height to be added is a sum of the initial height before cycle detection and
            # the height of the leftover *after* the final completed cycle.  This can be
            # represented as prev_max_h + (max_heights[n_prev_shape + (target_cycle_offset)] - prev_max_h) + 1
            # Need to add 1 here since our max_y is 0-indexed.
            height_add_on = max_heights[n_prev_shape + (target % cycle_length)] + 1
            return cycle_height_change * cycles + height_add_on
        states_seen[state] = shape_idx
        # Move to next shape
        shape_idx += 1
    return max_y + 1


if __name__ == '__main__':
    print(solve("example17.txt", part_two=False))
    print(solve("input17.txt", part_two=False))
    print(solve("example17.txt"))
    print(solve("input17.txt"))
