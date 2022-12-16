import math
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
    apsp = floyd_warshall(adjacency)
    return dfs('AA', set(), 30, apsp, rates, dict())


def dfs(curr, opened, iterations, apsp, rates, cache):
    m = 0
    hashable_opened = tuple(sorted(list(opened)))
    if (curr, iterations, hashable_opened) in cache:
        return cache[(curr, iterations, hashable_opened)]
    non_zero_rates = len([k for k, r in rates.items() if r != 0])
    if iterations == 0 or len(opened) == non_zero_rates:
        return 0
    if curr not in opened and rates[curr] > 0:
        opened.add(curr)
        m = dfs(curr, opened, iterations - 1, apsp, rates, cache) + rates[curr] * (iterations - 1)
        # Undo opening once sub-problem finishes
        opened.remove(curr)
    for adj in apsp[curr]:
        if adj in opened or apsp[curr][adj] > iterations or rates[adj] == 0:
            # Moving towards opened/zero valve and moving beyond iterations left.
            continue
        m = max(m, dfs(adj, opened, iterations - apsp[curr][adj], apsp, rates, cache))
    cache[(curr, iterations, hashable_opened)] = m
    return m


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def floyd_warshall(adjacency):
    all_pairs_shortest = dict()
    for v in adjacency:
        all_pairs_shortest[v] = {v: 0}
        for w in adjacency[v]:
            all_pairs_shortest[v][w] = 1
    for k in adjacency:
        for i in adjacency:
            for j in adjacency:
                if (
                        all_pairs_shortest[i].get(j, math.inf) > all_pairs_shortest[i].get(k, math.inf) +
                        all_pairs_shortest[k].get(j, math.inf)
                ):
                    all_pairs_shortest[i][j] = all_pairs_shortest[i][k] + all_pairs_shortest[k][j]
    for v in adjacency:
        # Remove self-loop post APSP computation
        all_pairs_shortest[v].pop(v)
    return all_pairs_shortest


def solve_part2(filename):
    adjacency, rates = parse_input(filename)
    apsp = floyd_warshall(adjacency)
    non_zero_flow = [k for k, r in rates.items() if r != 0]
    total = 0
    cache = dict()
    powerset_length = 2**len(non_zero_flow)
    for i, subset in enumerate(powerset(non_zero_flow), 1):
        # Use complementary subsets for both elephant and you.
        m1 = dfs('AA', set(subset), 26, apsp, rates, cache)
        m2 = dfs('AA', set(non_zero_flow).difference(set(subset)), 26, apsp, rates, cache)
        total = max(total, m1 + m2)
        if i > powerset_length // 2:
            break
    return total


if __name__ == '__main__':
    print(solve_part1_dfs("example16.txt"))
    print(solve_part1_dfs("input16.txt"))
    print(solve_part2("example16.txt"))
    print(solve_part2("input16.txt"))
