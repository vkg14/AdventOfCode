import math
from collections import defaultdict, namedtuple

Sensor = namedtuple('Sensor', ['x', 'y', 'd'])


def parse_positions(filename: str):
    with open(filename) as f:
        for line in f:
            l = line.rstrip('\n').split()
            x1 = int(l[2].rstrip(',').split('=')[1])
            y1 = int(l[3].rstrip(':').split('=')[1])
            x2 = int(l[8].rstrip(',').split('=')[1])
            y2 = int(l[9].split('=')[1])
            dist = abs(x2 - x1) + abs(y2 - y1)
            yield Sensor(x1, y1, dist), x2, y2


def find_range(sensor, potential_y, low_bound, high_bound):
    if potential_y < low_bound or potential_y > high_bound:
        return []
    dx = sensor.d - abs(sensor.y - potential_y)
    if dx < 0:
        return []
    return [max(low_bound, sensor.x - dx), min(high_bound, sensor.x + dx)]


def solve_part1(filename, y_target=2000000):
    s = set()
    beacons = set()
    for sensor, x2, y2 in parse_positions(filename):
        bounds = find_range(sensor, y_target, -math.inf, math.inf)
        if not bounds:
            continue
        s.update(set(range(bounds[0], bounds[1] + 1)))
        if y2 == y_target:
            beacons.add(x2)
    return len(s.difference(beacons))


def merge(sorted_ranges, next_range):
    sorted_ranges.append(next_range)
    sorted_ranges.sort()
    new_ranges = []
    for r in sorted_ranges:
        if not new_ranges or r[0] > new_ranges[-1][1]:
            new_ranges.append(r)
            continue
        new_ranges[-1][1] = max(new_ranges[-1][1], r[1])
    return new_ranges


def merge_other(sorted_ranges, new_range):
    res = []
    i = 0
    while i < len(sorted_ranges) and sorted_ranges[i][1] < new_range[0]:
        res.append(sorted_ranges[i])
        i += 1
    merged_range = new_range
    while i < len(sorted_ranges) and sorted_ranges[i][0] <= merged_range[1]:
        merged_range[1] = max(merged_range[1], sorted_ranges[i][1])
        i += 1
    res.append(merged_range)
    res.extend(sorted_ranges[i:])
    return res


def solve_part2(filename, high_bound=4000000):
    low_bound = 0
    # beacons don't matter - only sensor w/ distance
    sensors = [sensor for sensor, _, _ in parse_positions(filename)]
    ranges = defaultdict(list)
    for sensor in sensors:
        for y2 in range(sensor.y - sensor.d, sensor.y + sensor.d + 1):
            next_range = find_range(sensor, y2, low_bound, high_bound)
            if not next_range:
                continue
            ranges[y2] = merge(ranges[y2], next_range)

    y, range_with_gap = [(y, ranges[y]) for y in ranges if len(ranges[y]) > 1][0]
    x = range_with_gap[0][1] + 1
    return x * 4000000 + y


if __name__ == '__main__':
    print(solve_part1("example15.txt", y_target=10))
    print(solve_part1("input15.txt"))
    print(solve_part2("example15.txt", high_bound=20))
    print(solve_part2("input15.txt"))
