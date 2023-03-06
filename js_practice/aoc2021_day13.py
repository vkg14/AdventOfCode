from tabulate import tabulate


def parse_file(filename):
    with open(filename) as f:
        raw_text = f.read()
        dots_text, folds_text = raw_text.split('\n\n')
        dots = set()
        for line in dots_text.split('\n'):
            x, y = [int(c) for c in line.split(',')]
            dots.add((x, y))
        folds = []
        for line in folds_text.split('\n'):
            _, _, fold = line.split()
            folds.append(fold.split('='))
    return dots, folds


def shift_dots(coord_idx, shift, dots):
    """
    If any point in dots has a negative coordinate after a fold operation, we must shift all dots along that dimension
    by the *most* negative (minimum) coordinate so that 0-indexing can be maintained.
    """
    shifted_dots = set()
    for dot in dots:
        shifted_dot = list(dot)
        shifted_dot[coord_idx] += shift
        shifted_dots.add(tuple(shifted_dot))
    return shifted_dots


def process_fold(axis, val, dots):
    """
    Important take away:
    - ask what happens at the boundary cases (ie, at the fold point) -- do the points just go-away?
        - answer: in this case they do; work out the math for translation and encapsulate into a function
    - not relevant for this problem but could be relevant: what happens when the bottom folds *over* the top?
        - answer: just shift by the most negative value upwards
    """
    mapping = {}
    coordinate_idx = 0 if axis == 'x' else 1
    shift = 0
    for dot in dots:
        if dot[coordinate_idx] < val:
            continue
        elif dot[coordinate_idx] == val:
            # Boundary points are squashed
            mapping[dot] = None
        else:
            new_dot = list(dot)
            post_fold = 2*val - dot[coordinate_idx]
            new_dot[coordinate_idx] = post_fold
            mapping[dot] = tuple(new_dot)
            shift = max(shift, -1 * post_fold)
    for old_dot, new_dot in mapping.items():
        dots.remove(old_dot)
        if new_dot:
            dots.add(new_dot)
    if shift > 0:
        # Shift all points to have them relative to over-fold
        shift_dots(coordinate_idx, shift, dots)


def plot_dots(dots):
    max_x = max(x for x, _ in dots) + 1
    max_y = max(y for y, _ in dots) + 1
    grid = [['.'] * max_x for _ in range(max_y)]
    for x, y in dots:
        # Moving this outside the above loop means less hits to the set.
        grid[y][x] = '#'
    return grid


if __name__ == '__main__':
    dots, folds = parse_file('inputs/actual_day13.txt')
    for fold in folds:
        process_fold(fold[0], int(fold[1]), dots)
        print(len(dots))
    grid = plot_dots(dots)
    print(tabulate(grid))
