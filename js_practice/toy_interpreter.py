from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Instruction:
    """
    Explanation at high level:
    - We walk through the list of instructions.
    - Have a list of if / elifs to separate behavior of each instruction
    - We initialize a stack (list) and a ptr (index into instruction list)
    - On every instruction processing, we perform operation on stack, print to std out, or adjust the ptr
    - Jump adjusts the ptr in a non-linear way but all other operations add 1 to the jump ptr
    Edge cases:
    - When ptr moves past the length of instruction list, program is done
    - Popping off of empty stack? (possible in pop, print/pop, concat) -> throw?
    """
    name: str
    push_arg: Optional[str]
    jump_arg: Optional[int]


def pop(stack: List[str]) -> str:
    if not stack:
        raise Exception("Cannot pop off empty stack.")
    return stack.pop()


def interpret(instructions: List[Instruction]):
    stack = []
    ptr = 0
    while ptr < len(instructions):
        instruction: Instruction = instructions[ptr]
        if instruction.name == "Jump":
            ptr = instruction.jump_arg
            continue
        elif instruction.name == "Push":
            stack.append(instruction.push_arg)
        elif instruction.name == "Pop":
            pop(stack)
        elif instruction.name == "Print_and_Pop":
            print(pop(stack))
        else:
            # Concat
            stack.append(f'{pop(stack)}{pop(stack)}')
        ptr += 1


def get_index_conversions(instructions: List[Instruction]):
    shift = 0
    mapped_indices = {}
    for i, instruction in enumerate(instructions):
        mapped_indices[i] = i + shift * 2
        if instruction.name == "Jump":
            shift += 1
    return mapped_indices


def transform(instructions: List[Instruction]) -> List[Instruction]:
    """
    Explanation at high level:
    - Go through each instruction and add it to a new list
    - If its a jump, add a push and print_and_pop before it to match the lines that we are jumping to
    - Return this new set of instructions
    Edge cases:
    - The instruction indices change which is now relevant to jumps
    - Jump jumps to a new instruction in the list -> how do we compute this?
    - Debug print is for old indices (as they exist without the new added instructions)
    """
    new_instructions = []
    conversions = get_index_conversions(instructions)
    for i, instruction in enumerate(instructions):
        if instruction.name == "Jump":
            initial_jump_arg = instruction.jump_arg
            new_instructions.append(Instruction("Push", push_arg=f"debug: jumping from {i} to {initial_jump_arg}!"))
            new_instructions.append(Instruction("Print_and_pop"))
            new_instructions.append(Instruction("Jump", jump_arg=conversions[initial_jump_arg]))
            continue
        new_instructions.append(instruction)
    return new_instructions
