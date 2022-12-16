import math
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from typing import Tuple

Sensor = namedtuple('Sensor', ['x', 'y', 'd'])


@dataclass
class LineSegment:
    p1: Tuple[int, int]
    p2: Tuple[int, int]

    @property
    def x1(self):
        return self.p1[0]

    @property
    def y1(self):
        return self.p1[1]

    @property
    def x2(self):
        return self.p2[0]

    @property
    def y2(self):
        return self.p2[1]

    def intersect(self, other: 'LineSegment'):
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        x3, y3 = other.x1, other.y1
        x4, y4 = other.x2, other.y2
        denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denom == 0:
            return None
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
        if ua < 0 or ua > 1:  # out of range
            return None
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
        if ub < 0 or ub > 1:  # out of range
            return None
        x = int(x1 + ua * (x2 - x1))
        y = int(y1 + ua * (y2 - y1))
        return x, y


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


def find_points_on_boundary(sensor, low_bound, high_bound):
    radius = sensor.d + 1
    res = set()
    min_y = max(low_bound, sensor.y - radius)
    max_y = min(high_bound, sensor.y + radius)
    for y in range(min_y, max_y + 1):
        dx = radius - abs(sensor.y - y)
        for x in [sensor.x - dx, sensor.x + dx]:
            if low_bound <= x <= high_bound:
                res.add((x, y))
    return res


def manhattan_distance(sensor, x, y):
    return abs(sensor.x - x) + abs(sensor.y - y)


def solve_part2_sashko(filename, high_bound=4000000):
    low_bound = 0
    # beacons don't matter - only sensor w/ distance
    sensors = [sensor for sensor, _, _ in parse_positions(filename)]
    boundary_points = set()
    for sensor in sensors:
        boundary_points.update(find_points_on_boundary(sensor, low_bound, high_bound))
    for x, y in boundary_points:
        satisfies_all = True
        for sensor in sensors:
            if manhattan_distance(sensor, x, y) <= sensor.d:
                satisfies_all = False
                break
        if satisfies_all:
            return x * 4000000 + y
    raise Exception("Found no point that satisfies all sensors!")


def solve_part2_sensor_pairs(filename, high_bound=4000000):
    low_bound = 0
    # beacons don't matter - only sensor w/ distance
    sensors = [sensor for sensor, _, _ in parse_positions(filename)]
    segments = []
    for sensor in sensors:
        radius = sensor.d + 1
        p1 = (sensor.x - radius, sensor.y)
        p2 = (sensor.x, sensor.y + radius)
        p3 = (sensor.x + radius, sensor.y)
        p4 = (sensor.x, sensor.y - radius)
        for boundary_edge in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
            segments.append(LineSegment(*boundary_edge))
    n_segments = len(segments)
    intersections = set()
    for i in range(n_segments):
        for j in range(i+1, n_segments):
            intersection = segments[i].intersect(segments[j])
            if not intersection or min(*intersection) < low_bound or max(*intersection) > high_bound:
                continue
            intersections.add(intersection)
    # Find intersection that satisfies all sensors
    for x, y in intersections:
        satisfies_all = True
        for sensor in sensors:
            if manhattan_distance(sensor, x, y) <= sensor.d:
                satisfies_all = False
                break
        if satisfies_all:
            return x * 4000000 + y
    raise Exception("Found no point that satisfies all sensors!")


if __name__ == '__main__':
    # print(solve_part1("example15.txt", y_target=10))
    # print(solve_part1("input15.txt"))
    # print(solve_part2("example15.txt", high_bound=20))
    # print(solve_part2_sensor_pairs("example15.txt", high_bound=20))
    # print(solve_part2_sashko("example15.txt", high_bound=20))
    # print(solve_part2("input15.txt"))
    print(solve_part2_sensor_pairs("input15.txt"))
    # print(solve_part2_sashko("input15.txt"))
