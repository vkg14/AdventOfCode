from collections import deque, defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Tuple, Dict


@dataclass
class Conversions:
    facts: DefaultDict[str, Dict[str, float]]

    def add_fact(self, fro: str, to: str, val: float):
        self.facts[fro][to] = val
        self.facts[to][fro] = 1.0/val

    def add_multiple_facts(self, facts: List[Tuple[str, str, float]]):
        for fro, to, val in facts:
            self.add_fact(fro, to, val)

    def query(self, inp: float, start: str, end: str) -> float:
        visited = set()
        queue = deque([(start, inp)])
        while queue:
            unit, v = queue.popleft()
            visited.add(unit)
            for nxt, conv in self.facts[unit].items():
                if nxt in visited:
                    continue
                if nxt == end:
                    return conv * v
                queue.append((nxt, conv * v))
        raise Exception(f"No conversion between {start} and {end}")


if __name__ == '__main__':
    c = Conversions(defaultdict(dict))
    c.add_fact('m', 'ft', 3.28)
    c.add_fact('ft', 'in', 12)
    c.add_fact('in', 'cm', 2.54)
    c.add_fact('cm', 'mm', 10)
    c.add_fact('hr', 'min', 60)
    print(c.query(2, 'm', 'in'))
    print(c.query(2000, 'mm', 'in'))
    c.query(2, 'hr', 'ft')
