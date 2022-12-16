import math
from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import chain, combinations
from typing import DefaultDict, List, Dict, Set, FrozenSet


@dataclass
class ValveGraph:
    # Intended to be a static representation of valve/tunnel graph
    adjacency: DefaultDict[str, List]
    rates: Dict[str, int]
    apsp: Dict[str, Dict[str, int]] = field(default_factory=dict)
    non_zero_valves: FrozenSet[str] = field(default_factory=frozenset)
    non_zero_order: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        self.non_zero_valves = frozenset([k for k, r in self.rates.items() if r > 0])
        self.non_zero_order = {v: i for i, v in enumerate(self.non_zero_valves)}
        self.floyd_warshall()

    def floyd_warshall(self):
        for v in self.adjacency:
            self.apsp[v] = {v: 0}
            for w in self.adjacency[v]:
                self.apsp[v][w] = 1
        for k in self.adjacency:
            for i in self.adjacency:
                for j in self.adjacency:
                    if (
                            self.apsp[i].get(j, math.inf) > self.apsp[i].get(k, math.inf) +
                            self.apsp[k].get(j, math.inf)
                    ):
                        self.apsp[i][j] = self.apsp[i][k] + self.apsp[k][j]
        for v in self.adjacency:
            # Remove self-loop and zero destinations post APSP computation
            removable_destinations = [w for w in self.apsp[v] if self.rates[w] == 0 or w == v]
            for d in removable_destinations:
                self.apsp[v].pop(d)

    # Using the bit tricks below shaves time from 36s to 33s
    # Allows us not to pass around frozenset
    def is_valve_open(self, valve, n):
        return (n >> self.non_zero_order[valve]) & 1

    def set_valve_bit(self, valve, n):
        return (1 << self.non_zero_order[valve]) | n

    def get_open_subset(self, valves):
        x = 0
        for valve in valves:
            x = self.set_valve_bit(valve, x)
        return x

    def all_valves_open(self, n):
        return n + 1 == (1 << len(self.non_zero_valves))

    def get_complement_flow_rate(self, n):
        r = 0
        for v in self.non_zero_valves:
            if not self.is_valve_open(v, n):
                r += self.rates[v]
        return r


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
    return ValveGraph(adjacency, rates)


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
    graph = parse_input(filename)
    # You know that flow rate of 'AA' is always 0.
    return dfs('AA', 0, 30, graph, dict())


def solve_part1_bfs(filename):
    graph = parse_input(filename)
    return bfs(30, graph.apsp, graph.rates, graph.non_zero_valves)


def dfs(curr: str, opened: int, iterations: int, graph: ValveGraph, cache, target_flow=-math.inf):
    m = 0
    if (curr, iterations, opened) in cache:
        return cache[(curr, iterations, opened)]
    if iterations == 0 or graph.all_valves_open(opened):
        return 0
    if target_flow > 0 and graph.get_complement_flow_rate(opened) * (iterations - 1) < target_flow:
        # Shortcut with max flow rate
        return 0
    for adj, steps in graph.apsp[curr].items():
        # We want to move to and open a valve
        n_move_and_open = steps + 1
        if graph.is_valve_open(adj, opened) or n_move_and_open > iterations:
            # Ignore opened and too-distant valves
            continue
        opened_new = graph.set_valve_bit(adj, opened)
        flow_unlocked = graph.rates[adj] * (iterations - n_move_and_open)
        m = max(m, dfs(adj, opened_new, iterations - n_move_and_open, graph, cache,
                       target_flow - flow_unlocked) + flow_unlocked)
    cache[(curr, iterations, opened)] = m
    return m


def bfs(iterations, apsp, rates, target_set):
    q = deque([('AA', iterations, target_set, 0)])
    running_max = 0
    while q:
        cur, n_iter, closed, flow = q.popleft()
        if n_iter == 0 or len(closed) == 0:
            running_max = max(running_max, flow)
            continue
        for adj, steps in apsp[cur].items():
            n_move_and_open = steps + 1
            if adj not in closed or n_iter < n_move_and_open:
                continue
            closed_copy = set(closed)
            closed_copy.remove(adj)
            flow_unlocked = rates[adj] * (n_iter - n_move_and_open)
            q.append((adj, n_iter - n_move_and_open, closed_copy, flow + flow_unlocked))
    return running_max


def half_powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    start = len(s) // 2
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def solve_part2(filename):
    graph = parse_input(filename)
    max_seen = 0
    cache = dict()
    powerset_length = 2 ** len(graph.non_zero_valves)
    for i, subset in enumerate(half_powerset(graph.non_zero_valves), 1):
        # Use complementary subsets for both elephant and you.
        my_subset = graph.get_open_subset(subset)
        elephant_subset = (1 << len(graph.non_zero_valves)) - my_subset - 1
        m1 = dfs('AA', my_subset, 26, graph, cache)
        m2 = dfs('AA', elephant_subset, 26, graph, cache, target_flow=max_seen-m1)
        max_seen = max(max_seen, m1 + m2)
        if i == powerset_length // 2:
            break
    return max_seen


if __name__ == '__main__':
    print(solve_part1_dfs("example16.txt"))
    print(solve_part1_dfs("input16.txt"))
    print(solve_part2("example16.txt"))
    print(solve_part2("input16.txt"))
