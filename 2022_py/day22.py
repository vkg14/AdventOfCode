def extract_moves(line):
    moves = []
    curr = []
    for c in line:
        if c in ('L', 'R'):
            moves.append(int(''.join(curr)))
            moves.append(c)
            curr = []
        else:
            curr.append(c)
    moves.append(int(''.join(curr)))
    return moves


def read_input(filename):
    array = []
    start = None
    placeholder = None
    with open(filename) as f:
        line = next(f).rstrip('\n')
        while line:
            sp = [*line]
            sp = [x if x != ' ' else placeholder for x in sp]
            if not start:
                start = (0, sp.index('.'))
            array.append(sp)
            line = next(f).rstrip('\n')
        moves = extract_moves(next(f).rstrip('\n'))
    maxlen = max(len(a) for a in array)
    for i in range(len(array)):
        padding = maxlen - len(array[i])
        array[i] += [placeholder] * padding
    return array, start, moves


def get_next_position(curr, move, grid):
    nxt_r, nxt_c = tuple([sum(x) for x in zip(*[curr, move])])
    in_bounds = lambda r1, c1: 0 <= r1 < len(grid) and 0 <= c1 < len(grid[0])
    if in_bounds(nxt_r, nxt_c):
        val = grid[nxt_r][nxt_c]
        if val == '#':
            return curr
        elif val == '.':
            return nxt_r, nxt_c
    # Moving along row/column for wrapping
    dr, dc = [-m for m in move]
    r, c = curr
    while in_bounds(r, c) and grid[r][c] is not None:
        r += dr
        c += dc
    if grid[r - dr][c - dc] == '#':
        return curr
    else:
        return r - dr, c - dc


def solve(filename):
    grid, curr, moves = read_input(filename)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d_idx = 0
    for m in moves:
        if isinstance(m, int):
            for _ in range(m):
                nxt = get_next_position(curr, directions[d_idx], grid)
                if nxt == curr:
                    curr = nxt
                    break
                curr = nxt
        elif m == 'R':
            d_idx = (d_idx + 1) % 4
        elif m == 'L':
            d_idx = (d_idx - 1) % 4
        else:
            raise Exception('UNKNOWN INPUT!')

    return (curr[0] + 1) * 1000 + (curr[1] + 1) * 4 + d_idx


if __name__ == '__main__':
    print(solve("example22.txt"))
    print(solve("input22.txt"))
