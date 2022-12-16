from collections import defaultdict
from itertools import chain, combinations


def parse_input(filename: str):
    adjacency = defaultdict(list)
    rates = dict()
    with open(filename) as f:
        for line in f:
            l = line.rstrip('\n').split(';')
            first_half = l[0].split()
            valve = first_half[1]
            rate = int(first_half[4].split('=')[1])
            if 'valves' in l[1]:
                second_half = l[1].split('valves ')
            else:
                second_half = l[1].split('valve ')
            adj = second_half[1].split(', ')
            adjacency[valve].extend(adj)
            rates[valve] = rate
    return adjacency, rates


def bitfield(n, d):
    res = [int(digit) for digit in bin(n)[2:]]
    pad = [0] * (d - len(res))
    return pad + res


def bitarr_to_int(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out


def solve_part1_top_down(filename):
    # SLOW BOTTOM UP APPROACH WITH BITMASK
    adjacency, rates = parse_input(filename)
    order = dict()
    i = 0
    for k in rates:
        if rates[k] == 0:
            continue
        order[k] = i
        i += 1
    n = len(order)
    dp = dict()
    for v, rate in rates.items():
        for i in range(2 ** len(order)):
            dp[(v, 1, i)] = 0
    for i in range(2, 31):
        for v, rate in rates.items():
            for j in range(2 ** len(order)):
                m = max(dp[(w, i - 1, j)] for w in adjacency[v])
                if rates[v] == 0:
                    dp[(v, i, j)] = m
                    continue
                bitarr = bitfield(j, n)
                if not bitarr[order[v]]:
                    bitarr[order[v]] = 1
                    new_j = bitarr_to_int(bitarr)
                    m = max(m, dp[(v, i - 1, new_j)] + rate * (i - 1))
                dp[(v, i, j)] = m

    return dp[('AA', 30, 0)]


def solve_part1_dfs(filename):
    adjacency, rates = parse_input(filename)
    return dfs('AA', set(), 30, adjacency, rates, dict())


def dfs(curr, opened, iterations, adjacency, rates, cache):
    m = 0
    hashable_opened = tuple(sorted(list(opened)))
    if (curr, iterations, hashable_opened) in cache:
        return cache[(curr, iterations, hashable_opened)]
    if iterations == 0 or len(opened) == len(rates):
        return 0
    if curr not in opened and rates[curr] > 0:
        opened.add(curr)
        m = dfs(curr, opened, iterations - 1, adjacency, rates, cache) + rates[curr] * (iterations - 1)
        opened.remove(curr)
    for w in adjacency[curr]:
        m = max(m, dfs(w, opened, iterations - 1, adjacency, rates, cache))
    cache[(curr, iterations, hashable_opened)] = m
    return m


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def solve_part2(filename):
    adjacency, rates = parse_input(filename)
    non_zero_flow = [k for k, r in rates.items() if r != 0]
    total = 0
    cache = dict()
    for subset in powerset(non_zero_flow):
        m1 = dfs('AA', set(subset), 26, adjacency, rates, cache)
        m2 = dfs('AA', set(non_zero_flow).difference(set(subset)), 26, adjacency, rates, cache)
        total = max(total, m1 + m2)
    return total


if __name__ == '__main__':
    # print(solve_part1_dfs("example16.txt"))
    # print(solve_part1_dfs("input16.txt"))
    print(solve_part2("example16.txt"))
    print(solve_part2("input16.txt"))
