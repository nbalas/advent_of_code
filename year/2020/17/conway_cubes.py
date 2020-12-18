from collections import namedtuple
from logs.setup_logs import init_logs
from itertools import repeat
from readers.file_reader import FileReader

logger = init_logs(__name__)

ACTIVE = '#'
INACTIVE = '.'

Coordinates = namedtuple('Coordinates', ('x', 'y', 'z', 'w'))


def main():
    cubes = parse_input(FileReader.read_input_as_list())
    for _ in repeat(None, 6):
        cubes = run_cycle(cubes)
    logger.info(f"There are {len(cubes)} active cubes")


def run_cycle(cubes):
    new_state = set()
    for cube in cubes:
        for neighbor in neighbors(cube):
            if neighbor not in cubes:
                if active_neighbors(cubes, neighbor) == 3:
                    new_state.add(neighbor)
        if 1 < active_neighbors(cubes, cube) < 4:
            new_state.add(cube)
    return new_state


def neighbors(coords):
    for z in range(coords.z-1, coords.z+2):
        for y in range(coords.y-1, coords.y+2):
            for x in range(coords.x - 1, coords.x + 2):
                for w in range(coords.w - 1, coords.w + 2):
                    if z == coords.z and y == coords.y and x == coords.x and w == coords.w:
                        continue
                    yield Coordinates(x, y, z, w)


def active_neighbors(cubes, coords):
    n = 0
    for neighbor in neighbors(coords):
        if neighbor in cubes:
            n += 1
    return n


def parse_input(raw_input):
    cubes = set()
    for y, row in enumerate(raw_input):
        for x, value in enumerate(row):
            if value is ACTIVE:
                cubes.add(Coordinates(x, y, 0, 0))
    return cubes


if __name__ == '__main__':
    main()