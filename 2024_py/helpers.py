import subprocess

SESSION = "53616c7465645f5f6d52ec2ed6632fddc65f8db735600592818aacc0823788cf212a86b7a584caa9e74a30910ed7dbcc33688a7db50c9ada168e766a1d61864c"

# Grid stuff
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_NAMES = ['R', 'D', 'L', 'U']
sum_tuples = lambda tuple1, tuple2: tuple(a + b for a, b in zip(tuple1, tuple2))


def in_bounds(t1, m, n):
    r, c = t1
    return 0 <= r < m and 0 <= c < n


def get_input(day, year=2023, useragent='vganesan'):
    cmd = f'curl https://adventofcode.com/{year}/day/{day}/input --cookie "session={SESSION}" -A \'{useragent}\''
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode('utf-8')
    with open(f"inputs/input{day}.txt", "w") as f:
        f.write(output.rstrip())


if __name__ == "__main__":
    get_input(day=2)
