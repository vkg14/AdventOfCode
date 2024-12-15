import subprocess

SESSION = "53616c7465645f5f59a74d5dd354ff8e4f265e4fa310668325775821243ee01ec68a5254ffef71989d3c41f75289ecea97107ef6372586af481b6adbd46925a3"

# Grid stuff
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_NAMES = ['R', 'D', 'L', 'U']
sum_tuples = lambda tuple1, tuple2: tuple(a + b for a, b in zip(tuple1, tuple2))
diff_tuples = lambda tuple1, tuple2: tuple(a - b for a, b in zip(tuple1, tuple2))
mul_tuple = lambda tuple1, c: tuple(c * t for t in tuple1)


def in_bounds(t1, m, n):
    r, c = t1
    return 0 <= r < m and 0 <= c < n


def get_readlines_stripped(fname):
    with open(fname, "r") as f:
        return [l.strip() for l in f.readlines()]


def read_file_split(fname):
    with open(fname, "r") as f:
        return [line.split() for line in f]


def get_input(day, year=2024, useragent='vganesan'):
    cmd = f'curl https://adventofcode.com/{year}/day/{day}/input --cookie "session={SESSION}" -A \'{useragent}\''
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8')
    with open(f"inputs/input{day}.txt", "w") as f:
        f.write(output.rstrip())


if __name__ == "__main__":
    get_input(day=2)
