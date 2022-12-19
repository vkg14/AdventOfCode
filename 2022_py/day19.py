import math
from collections import deque, defaultdict


def get_blueprint(filename):
    with open(filename) as f:
        for line in f:
            bp_id, costs = line.rstrip('\n').split(': ')
            bp_id = int(bp_id.split()[1])
            costs = costs.split('.')
            blueprint = dict()
            for cost in costs:
                if not cost:
                    break
                robot = cost.strip().split()[1]
                cost_dict = dict()
                for c in cost.split(' costs ')[1].split(' and '):
                    c, t = c.split()
                    cost_dict[t] = int(c)
                blueprint[robot] = cost_dict
            yield bp_id, blueprint


def time_to_build_robot(cost, robots, elements):
    time_to_collect = 0
    for element, c in cost.items():
        needed = c - elements[element]
        time_needed = math.inf if not robots[element] else math.ceil(needed / robots[element])
        time_to_collect = max(time_to_collect, time_needed)
    return time_to_collect


def construct_state(bp, robots, elements, minute):
    # The state is the number of robots and elements we have at the end of some minute
    state = []
    for e in sorted(bp.keys()):
        state.extend([robots[e], elements[e]])
    state.append(minute)
    return tuple(state)


def max_cost(element, bp):
    return max(bp[r].get(element, 0) for r in bp)


def solve_blueprint(bp, n=24):
    """
    Idea here is to BFS, keeping track of geode potential at the end of n minutes, with a few optimizations:
    - we fast-forward to states where we have just built a robot (removing all intermediate production-only states)
    - we never look to create a robot when we are already have enough robots of that element to cover any assoc. cost
    - we collapse states where we have mass-produced some element beyond what is usable in the remaining time to the max
    usable amount (this maximum is constant for a given minute t and element e).
    """
    s_robots = defaultdict(int)
    s_robots['ore'] = 1
    s_elements = defaultdict(int)
    minute = 0
    q = deque([(s_robots, s_elements, minute)])
    visited = {construct_state(bp, s_robots, s_elements, minute)}
    max_seen = 0
    while q:
        robots, elements, minute = q.popleft()
        max_seen = max(max_seen, elements['geode'] + robots['geode'] * (n - minute))
        for robot, cost in bp.items():
            # Optimization for pruning: don't make a robot we already have enough to cover any build cost
            if robot != 'geode' and robots[robot] == max_cost(robot, bp):
                # Don't consider making this robot
                continue
            t = time_to_build_robot(cost, robots, elements)
            if minute + t + 1 < n:
                e_copy = elements.copy()
                r_copy = robots.copy()
                for r in robots:
                    e_copy[r] += robots[r] * (t + 1)
                for e in cost:
                    e_copy[e] -= cost[e]
                r_copy[robot] += 1
                # Optimization: collapse all states with excess elements to the max consumable amount
                for e in bp:
                    if e == 'geode':
                        continue
                    max_cost_e = max_cost(e, bp)
                    time_left = n - (minute + t + 1)
                    max_usable_e = time_left * max_cost_e - r_copy[e] * (time_left - 1)
                    e_copy[e] = min(e_copy[e], max_usable_e)
                state = construct_state(bp, r_copy, e_copy, minute + t + 1)
                if state not in visited:
                    visited.add(state)
                    q.append((r_copy, e_copy, minute + t + 1))
    return max_seen


def solve(filename: str):
    bp_gen = get_blueprint(filename)
    max_seen = (0, 0)
    maxes = {}
    for bp_id, bp in bp_gen:
        maxes[bp_id] = solve_blueprint(bp)
        max_seen = max(max_seen, (maxes[bp_id], bp_id))
    return sum(a * b for a, b in maxes.items())


def solve_part_two(filename: str):
    bp_gen = get_blueprint(filename)
    res = 1
    for bp_id, bp in bp_gen:
        geocodes = solve_blueprint(bp, n=32)
        print(bp_id, bp, geocodes)
        res *= geocodes
        if bp_id == 3:
            break
    return res


if __name__ == '__main__':
    print(solve("example19.txt"))
    print(solve("input19.txt"))
    print(solve_part_two("example19.txt"))
    print(solve_part_two("input19.txt"))
