from collections import namedtuple, defaultdict
from copy import deepcopy
from itertools import permutations

from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'

PART_1_OCCUPIED_LIMIT = 4
PART_2_OCCUPIED_LIMIT = 5

Coordinates = namedtuple("Coordinates", ('x', 'y'))


DIRECTIONS = {
    "N": lambda cords: Coordinates(cords.x, cords.y - 1),
    "NE": lambda cords: Coordinates(cords.x + 1, cords.y - 1),
    "E": lambda cords: Coordinates(cords.x + 1, cords.y),
    "SE": lambda cords: Coordinates(cords.x + 1, cords.y + 1),
    "S": lambda cords: Coordinates(cords.x, cords.y + 1),
    "SW": lambda cords: Coordinates(cords.x - 1, cords.y + 1),
    "W": lambda cords: Coordinates(cords.x - 1, cords.y),
    "NW": lambda cords: Coordinates(cords.x - 1, cords.y - 1)
}


def main():
    current_seating_map = list(map(list, FileReader.read_input_as_list()))

    while True:
        # print_seat_map(current_seating_map)
        new_seating_map = run_rules(current_seating_map)
        if new_seating_map == current_seating_map:
            logger.info("Our seating map changes no longer, we have stabilized")
            break
        current_seating_map = new_seating_map
    logger.info(f"There are {count_occupied(new_seating_map)} occupied seats")


def run_rules(seating_map):
    next_seating_map = deepcopy(seating_map)
    for y_value, row in enumerate(seating_map):
        for x_value, seat in enumerate(row):
            current_cords = Coordinates(x_value, y_value)
            if seat is EMPTY_SEAT and not has_occupied_seats_in_any_direction(seating_map, 0, current_cords):
                next_seating_map[current_cords.y][current_cords.x] = OCCUPIED_SEAT
            elif seat is OCCUPIED_SEAT and has_occupied_seats_in_any_direction(seating_map, PART_2_OCCUPIED_LIMIT, current_cords):
                next_seating_map[current_cords.y][current_cords.x] = EMPTY_SEAT
    return next_seating_map


# Part 1
def has_occupied_seats_surrounding(seating_map, occupied_seats_limit, current_cords):
    occupied_seats = 0
    for x_range in range(-1, 2):
        for y_range in range(-1, 2):
            # logger.debug(f"Processing {x_range}, {y_range}")
            if x_range == 0 and y_range == 0:
                continue
            current_x = current_cords.x + x_range
            current_y = current_cords.y + y_range
            if invalid_coordinates(seating_map, Coordinates(current_x, current_y)):
                continue
            if seating_map[current_y][current_x] is OCCUPIED_SEAT:
                occupied_seats += 1
                if occupied_seats_limit <= occupied_seats:
                    return True
    # logger.debug(f"There are {occupied_seats} occupied_seats for coordinates {current_cords}")
    return False


# Part 2
def has_occupied_seats_in_any_direction(seating_map, occupied_seats_limit, current_cords):
    occupied_seats = 0
    for direction in DIRECTIONS:
        directional_cords = current_cords
        while True:
            directional_cords = DIRECTIONS[direction](directional_cords)
            # logger.debug(f"Searching for occupied seat {direction} of {current_cords} in {directional_cords}")
            if invalid_coordinates(seating_map, directional_cords) or seating_map[directional_cords.y][directional_cords.x] is EMPTY_SEAT:
                break
            if seating_map[directional_cords.y][directional_cords.x] is OCCUPIED_SEAT:
                occupied_seats += 1
                if occupied_seats_limit <= occupied_seats:
                    return True
                break
    return False


def invalid_coordinates(seating_map, cords):
    return cords.y < 0 or len(seating_map) <= cords.y or cords.x < 0 or len(seating_map[cords.y]) <= cords.x


def count_occupied(seating_map):
    return sum(map(len, [[seat for seat in row if seat is OCCUPIED_SEAT] for row in seating_map]))


def print_seat_map(seating_map):
    for row in seating_map:
        logger.info(row)
    logger.info('\n')


if __name__ == '__main__':
    main()