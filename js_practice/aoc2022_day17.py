from operator import add


class FallingRockSimulation:
    # Shapes are described relative to their bottom-left bounding point.
    MINUS = [(0, 0), (1, 0), (2, 0), (3, 0)]
    PLUS = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    L = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    PIPE = [(0, 0), (0, 1), (0, 2), (0, 3)]
    SQUARE = [(0, 0), (0, 1), (1, 0), (1, 1)]

    WIDTH = 7

    @classmethod
    def get_shape(cls, shape_idx):
        shapes = [cls.MINUS, cls.PLUS, cls.L, cls.PIPE, cls.SQUARE]
        return shapes[shape_idx % len(shapes)]

    @staticmethod
    def add_tuples(left, right):
        return tuple(map(add, left, right))

    def get_initial_cells(self, shape_idx, max_y):
        start = (2, max_y + 4)
        shape = self.get_shape(shape_idx)
        return [self.add_tuples(cell, start) for cell in shape]

    def in_bounds(self, x, y):
        return 0 <= x < self.WIDTH and y >= 0

    def try_move(self, direction, cells, occupied):
        nxt_cells = [self.add_tuples(cell, direction) for cell in cells]
        if all(t not in occupied and self.in_bounds(*t) for t in nxt_cells):
            return True, nxt_cells
        return False, cells

    def simulate(self, jetstream):
        occupied = set()
        shape_idx = 0
        jetstream_idx = 0
        n_jetstream = len(jetstream)
        jetstream_mapping = {'>': (1, 0), '<': (-1, 0)}
        max_y = -1
        while shape_idx < 2022:
            falling_rock = self.get_initial_cells(shape_idx, max_y)
            while True:
                # Push horizontally
                direction = jetstream_mapping[jetstream[jetstream_idx % n_jetstream]]
                _, falling_rock = self.try_move(direction, falling_rock, occupied)
                jetstream_idx += 1
                # Push down
                still_falling, falling_rock = self.try_move((0, -1), falling_rock, occupied)
                if not still_falling:
                    break
            # Update: next shape, occupied blocks, max_y
            shape_idx += 1
            occupied.update(falling_rock)
            max_y = max(max_y, *[y for _, y in falling_rock])
        return max_y + 1


if __name__ == '__main__':
    sim = FallingRockSimulation()
    with open('../2022_py/input17.txt') as f:
        directions = f.read().strip()
        print(sim.simulate(directions))
