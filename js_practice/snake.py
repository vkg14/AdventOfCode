import copy
import heapq
from collections import deque
from dataclasses import dataclass
from operator import add
from random import randrange
from typing import List, Tuple

from tabulate import tabulate


class Snake:
    INPUT_MAP = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    def __init__(self, dim: int, start: List[Tuple[int, int]], food: Tuple[int, int]):
        self.dim = dim
        self.body = deque(start)
        self.occupied = set(start)
        self.food = food
        self.game_over = False

    def __hash__(self):
        frozen = frozenset(self.occupied)
        return hash(frozen)

    @staticmethod
    def add_tuples(left: Tuple, right: Tuple) -> Tuple:
        return tuple(map(add, left, right))

    def _in_bounds(self, r, c):
        return 0 <= r < self.dim and 0 <= c < self.dim

    def respawn_food(self):
        r = randrange(self.dim)
        c = randrange(self.dim)
        while (r, c) in self.occupied:
            r = randrange(self.dim)
            c = randrange(self.dim)
        self.food = r, c
        print(f'New food at {self.food}!')

    def is_collision(self, coords):
        return coords in self.occupied or not self._in_bounds(*coords)

    def process_input(self, inp):
        """
        - Compute new head
        - If not food: remove tail and check for collisions
        - If food: do not remove tail and respawn food (end)
        - Add head to body and set
        """
        if self.game_over:
            return
        direction = self.INPUT_MAP.get(inp, None)
        if not direction:
            raise Exception(f"Unexpected input: {inp}")
        new_head = self.add_tuples(self.body[0], direction)
        should_gen_food = False
        if new_head != self.food:
            # Only remove tail if not food
            tail = self.body.pop()
            self.occupied.remove(tail)
            if self.is_collision(new_head):
                self.game_over = True
                return
        else:
            # Found food
            should_gen_food = True
        self.body.appendleft(new_head)
        self.occupied.add(new_head)
        # Should only respawn post applying head
        if should_gen_food:
            self.respawn_food()


def get_next_state(current_state: Snake, inp: str) -> Snake:
    next_state = copy.deepcopy(current_state)
    next_state.process_input(inp)
    return next_state


@dataclass
class HeapNode:
    priority: int
    snake: Snake
    moves: List[str]

    def __lt__(self, other: 'HeapNode'):
        return self.priority < other.priority


def manhattan_distance(p1, p2):
    return sum(abs(t - s) for s, t in zip(p1, p2))


def snake_ai_search(current_state: Snake):
    food = current_state.food
    dist = manhattan_distance(current_state.body[0], food)
    pq: List[HeapNode] = [HeapNode(dist, current_state, [])]
    seen_states = {current_state}
    while pq:
        nxt = heapq.heappop(pq)
        if nxt.snake.body[0] == food:
            return nxt.moves
        for direction in Snake.INPUT_MAP.keys():
            snake_copy = get_next_state(nxt.snake, direction)
            if snake_copy.game_over or snake_copy in seen_states:
                continue
            dist = manhattan_distance(snake_copy.body[0], food)
            heapq.heappush(pq, HeapNode(dist, snake_copy, nxt.moves + [direction]))
            seen_states.add(snake_copy)
    return []


def display_snake_game(snake):
    grid = [['.'] * snake.dim for _ in range(snake.dim)]
    for r, c in snake.occupied:
        grid[r][c] = '~'
    special_points = [(snake.food, '#'), (snake.body[0], 'H'), (snake.body[-1], 'T')]
    for point, char in special_points:
        r, c = point
        grid[r][c] = char
    print("*SNAKE GRID*")
    print(tabulate(grid))


def simulate(max_score=10):
    snake = Snake(6, [(1, 2), (1, 3), (1, 4)], (4, 4))
    display_snake_game(snake)
    moves = snake_ai_search(snake)
    while moves and len(snake.body) < max_score:
        print(f'Moves: {moves}')
        for move in moves:
            snake.process_input(move)
        display_snake_game(snake)
        moves = snake_ai_search(snake)
    print(f"Score of {len(snake.body)} achieved.")


if __name__ == '__main__':
    simulate(30)
