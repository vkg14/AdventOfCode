import subprocess

SESSION = "53616c7465645f5f59a74d5dd354ff8e4f265e4fa310668325775821243ee01ec68a5254ffef71989d3c41f75289ecea97107ef6372586af481b6adbd46925a3"

# Grid direction stuff
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_NAMES = ['R', 'D', 'L', 'U']
RIGHT, DOWN, LEFT, UP = (range(4))

# Grid tuple moving
sum_tuples = lambda tuple1, tuple2: tuple(a + b for a, b in zip(tuple1, tuple2))
diff_tuples = lambda tuple1, tuple2: tuple(a - b for a, b in zip(tuple1, tuple2))
mul_tuple = lambda tuple1, c: tuple(c * t for t in tuple1)


def in_bounds(t1, m, n):
    r, c = t1
    return 0 <= r < m and 0 <= c < n


def get_grid_as_map(fname):
    content = get_readlines_stripped(fname)
    full_grid = {}
    for i, line in enumerate(content):
        for j, char in enumerate(line):
            full_grid[(i, j)] = char
    m = len(content)
    n = len(content[0])
    return full_grid, m, n


def iter_cells(m, n):
    for r in range(m):
        for c in range(n):
            yield (r, c)


def print_grid(grid, m, n, filler='.'):
    res = [[filler] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            res[r][c] = grid.get((r, c), filler)
    _simulate_tabulate_plain(res)


def get_neighbors(m, n, directions, pos):
    for d in directions:
        nxt = sum_tuples(pos, d)
        if in_bounds(nxt, m, n):
            yield nxt


def get_readlines_stripped(fname):
    with open(fname, "r") as f:
        return [l.strip() for l in f.readlines()]


def read_file_split(fname):
    with open(fname, "r") as f:
        return [line.split() for line in f]


def _simulate_tabulate_plain(grid):
    # Determine the maximum width for each column
    num_cols = len(grid[0]) if grid else 0
    col_widths = [0] * num_cols

    for row in grid:
        for col_index, cell in enumerate(row):
            col_widths[col_index] = max(col_widths[col_index], len(str(cell)))

    # Print the grid with aligned columns
    for row in grid:
        row_str = "  ".join(f"{str(cell).ljust(col_widths[col_index])}"
                            for col_index, cell in enumerate(row))
        print(row_str)


def get_input(day, year=2024, useragent='vganesan'):
    cmd = f'curl https://adventofcode.com/{year}/day/{day}/input --cookie "session={SESSION}" -A \'{useragent}\''
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8')
    with open(f"inputs/input{day}.txt", "w") as f:
        f.write(output.rstrip())


if __name__ == "__main__":
    get_input(day=2)
