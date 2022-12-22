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

    # If we hit wall, we are still stuck on other side of portal
    if grid[r - dr][c - dc] == '#':
        return curr
    else:
        return r - dr, c - dc


def get_next_position_cube(curr, move, grid):
    nxt_r, nxt_c = tuple([sum(x) for x in zip(*[curr, move])])
    in_bounds = lambda r1, c1: 0 <= r1 < len(grid) and 0 <= c1 < len(grid[0])
    if in_bounds(nxt_r, nxt_c):
        val = grid[nxt_r][nxt_c]
        if val == '#':
            return curr, move
        elif val == '.':
            return (nxt_r, nxt_c), move
    old_move = move
    if old_move == (0, 1):
        if nxt_r in range(50):
            # Moves from east face to the south face
            nxt, move = (149 - nxt_r, 99), (0, -1)
        if nxt_r in range(50, 100):
            # Moves from bottom face to the east face
            nxt, move = (49, nxt_r + 50), (-1, 0)
        if nxt_r in range(100, 150):
            # Moves from south face to the east face
            nxt, move = (149 - nxt_r, 149), (0, -1)
        if nxt_r in range(150, 200):
            # Moves from top face to the south face
            nxt, move = (149, nxt_r - 100), (-1, 0)
    elif old_move == (1, 0):
        if nxt_c in range(50):
            nxt, move = (0, nxt_c + 100), (1, 0)
        if nxt_c in range(50, 100):
            nxt, move = (100 + nxt_c, 49), (0, -1)
        if nxt_c in range(100, 150):
            # East to bottom
            nxt, move = (nxt_c - 50, 99), (0, -1)
    elif old_move == (0, -1):
        if nxt_r in range(0, 50):
            # Moves from north face to west face
            nxt, move = (149 - nxt_r, 0), (0, 1)
        if nxt_r in range(50, 100):
            # Moves from bottom face to west face
            nxt, move = (100, nxt_r - 50), (1, 0)
        if nxt_r in range(100, 150):
            # Moves from west face to north face
            nxt, move = (149 - nxt_r, 50), (0, 1)
        if nxt_r in range(150, 200):
            # Moves from top face to the north face
            nxt, move = (0, nxt_r - 100), (1, 0)
    elif old_move == (-1, 0):
        if nxt_c in range(0, 50):
            # West to bottom face
            nxt, move = (nxt_c + 50, 50), (0, 1)
        if nxt_c in range(50, 100):
            # North to top face
            nxt, move = (100 + nxt_c, 0), (0, 1)
        if nxt_c in range(100, 150):
            # East to top face
            nxt, move = (199, nxt_c - 100), (-1, 0)
    else:
        raise Exception(f"Unknown move direction: {old_move}")

    # Still have to check that next is not a wall
    if grid[nxt[0]][nxt[1]] == '#':
        return curr, old_move
    else:
        return nxt, move


def solve(filename, cube=False):
    grid, curr, moves = read_input(filename)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d_idx = 0
    for m in moves:
        if isinstance(m, int):
            for _ in range(m):
                prev = curr
                if cube:
                    curr, new_dir = get_next_position_cube(curr, directions[d_idx], grid)
                    d_idx = directions.index(new_dir)
                    if d_idx not in range(4):
                        raise Exception(f"Invalid direction index: {d_idx}.")
                else:
                    curr = get_next_position(curr, directions[d_idx], grid)
                if prev == curr:
                    # Hit a wall
                    break
        elif m == 'R':
            d_idx = (d_idx + 1) % 4
        elif m == 'L':
            d_idx = (d_idx - 1) % 4
        else:
            raise Exception(f'UNKNOWN INPUT: {m}')

    return (curr[0] + 1) * 1000 + (curr[1] + 1) * 4 + d_idx


if __name__ == '__main__':
    print(solve("example22.txt"))
    print(solve("input22.txt"))
    print(solve("input22.txt", cube=True))
