import re
from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from collections import namedtuple

INPUT_REGEX = r'([a-z ]+)([0-9]+,[0-9]+) through ([0-9]+,[0-9]+)'
Instruction = namedtuple("Instruction", ["action", "start", "end"])

grid = {}

actions = {
    "turn on": lambda start, end: apply_action(start, end, 1),
    "turn off": lambda start, end: apply_action(start, end, -1),
    "toggle": lambda start, end: apply_action(start, end, 2)
}


def main():
    instructions = list(map(parse_instruction, FileReader.read_input_as_list()))
    for instruction in instructions:
        actions[instruction.action](instruction.start, instruction.end)
    print(f"There are {sum(grid.values())} lights on!")


def parse_instruction(instruction):
    matches = re.search(INPUT_REGEX, instruction)
    assert len(matches.groups()) == 3
    return Instruction(matches.group(1).strip(),
                       tuple(map(int, matches.group(2).strip().split(','))),
                       tuple(map(int, matches.group(3).strip().split(','))))


def apply_action(start, end, action):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            if (x, y) in grid:
                grid[(x, y)] = 0 if grid[(x, y)] + action < 0 else grid[(x, y)] + action
            elif action != -1:
                grid[(x, y)] = action


if __name__ == "__main__":
    main()
