

def to_snafu(n):
    snafu_map = {0: '0', 1: '1', 2: '2', -1: '-', -2: '='}
    res = []
    map_digit_to_char = lambda n: snafu_map[((n + 2) % 5) - 2]
    while n:
        res.append(map_digit_to_char(n))
        n = (n - ((n + 2) % 5) + 2) // 5
    return ''.join(reversed(res))


def to_int(snafu):
    snafu_map = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    return sum([5 ** i * snafu_map[c] for i, c in enumerate(reversed(snafu))])


def solve(filename: str):
    return to_snafu(sum([to_int(line.rstrip('\n')) for line in open(filename)]))


if __name__ == '__main__':
    print(solve("input25.txt"))
