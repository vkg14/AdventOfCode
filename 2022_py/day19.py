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
        if not robots[element]:
            # We cannot currently make this material
            return math.inf
        time_needed = math.ceil(needed / robots[element])
        time_to_collect = max(time_to_collect, time_needed)
    return time_to_collect


def construct_state(robots, elements, minute):
    # The state is the number of robots and elements we have at the end of some minute
    materials = ['ore', 'clay', 'obsidian', 'geode']
    return tuple(robots[e] for e in materials) + tuple(elements[e] for e in materials) + (minute,)


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
    max_costs = {element: max(bp[r].get(element, 0) for r in bp) for element in bp}
    minute = 0
    q = deque([(s_robots, s_elements, minute)])
    visited = {construct_state(s_robots, s_elements, minute)}
    max_seen = 0
    while q:
        robots, elements, minute = q.popleft()
        guaranteed_geodes = elements['geode'] + robots['geode'] * (n - minute)
        max_seen = max(max_seen, guaranteed_geodes)
        # Optimization: you can only make (t-1) * t / 2 geodes given t time steps including the current.
        max_potential_geodes = (n - minute - 1) * (n - minute) // 2
        if max_seen > guaranteed_geodes + max_potential_geodes:
            continue
        # Fast-forward state to the time *after* building the next robot
        fast_forward_times = [
            (
                time_to_build_robot(
                    bp[r], robots, elements
                    # Optimization for pruning: don't make a robot we already have enough to cover any build cost
                ) if r == 'geode' or robots[r] < max_costs[r] else math.inf, r)
            for r in bp]
        for t, robot in sorted(fast_forward_times):
            cost = bp[robot]
            if minute + t + 1 >= n:
                # Not enough time to make this robot.
                break
            elements_new = elements.copy()
            robots_new = robots.copy()
            for r in robots:
                elements_new[r] += robots[r] * (t + 1)
            for e in cost:
                elements_new[e] -= cost[e]
            robots_new[robot] += 1
            # Optimization: collapse all states with excess elements to the max consumable amount
            for e in bp:
                if e == 'geode':
                    continue
                time_left = n - (minute + t + 1)
                max_usable_e = time_left * max_costs[e] - robots_new[e] * (time_left - 1)
                elements_new[e] = min(elements_new[e], max_usable_e)
            state = construct_state(robots_new, elements_new, minute + t + 1)
            if state not in visited:
                visited.add(state)
                q.append((robots_new, elements_new, minute + t + 1))
                # Prune all states past where the next geode and obsidian are make-able
                if robot == 'geode':
                    break
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
        res *= geocodes
        if bp_id == 3:
            break
    return res


if __name__ == '__main__':
    # print(solve("example19.txt"))
    # print(solve("input19.txt"))
    # print(solve_part_two("example19.txt"))
    print(solve_part_two("input19.txt"))
