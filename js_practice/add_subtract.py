from collections import deque
from typing import List, Union


def reverse_all(*lists):
    for iterable in lists:
        iterable.reverse()


def sum_digits(left, right, carry):
    nxt = left + right + carry
    carry = nxt // 10
    nxt = nxt % 10
    return nxt, carry


def add(left: List[int], right: List[int]) -> List[int]:
    if len(left) < len(right):
        return add(right, left)
    carry = 0
    result = deque()
    reverse_all(left, right)
    for i in range(len(left)):
        right_digit = right[i] if i < len(right) else 0
        nxt, carry = sum_digits(left[i], right_digit, carry)
        result.appendleft(nxt)
    if carry:
        result.appendleft(carry)
    # Undo reversal
    reverse_all(left, right)
    return list(result)


def is_lt(left: List[int], right: List[int]):
    return len(left) < len(right) or (len(left) == len(right) and left[0] < right[0])


def sub(left: List[int], right: List[int]) -> List[Union[int, str]]:
    if is_lt(left, right):
        return ['-'] + sub(right, left)
    reverse_all(left, right)
    current_carry = 0
    next_carry = 0
    result = deque()
    for i in range(len(left)):
        right_digit = right[i] if i < len(right) else 0
        next_digit = left[i] - right_digit - current_carry
        if next_digit < 0:
            next_carry = 1
            next_digit += 10
        result.appendleft(next_digit)
        current_carry = next_carry
        next_carry = 0
    # Undo reversal
    reverse_all(left, right)
    return list(result)


if __name__ == '__main__':
    l = [4, 1, 2, 3]
    r = [9, 7, 2]
    print(add(r, l))
    print(sub(r, l))
