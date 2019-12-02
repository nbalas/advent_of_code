import logging
from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from collections import namedtuple

logger = init_logs(__name__, logging.INFO)

NORTH = '^'
SOUTH = 'v'
EAST = '>'
WEST = '<'


def main():
    history = {}
    Coordinates = namedtuple("Coordinates", ["x", "y"])

    current_location = Coordinates(0, 0)

    full_route = FileReader.read_input_as_string()

    # Solution for Part 1
    deliver_present(history, current_location)

    for next_direction in full_route:
        current_location = move_current_location(next_direction, current_location)
        deliver_present(history, current_location)

    logging.info(f"Delivered presents to {len(history)} unique homes")

    # Solution for Part 2
    history = {}
    current_location = Coordinates(0, 0)
    robo_current_location = Coordinates(0, 0)

    deliver_present(history, current_location)
    deliver_present(history, robo_current_location)
    for count, next_direction in enumerate(full_route):
        if count % 2:
            current_location = move_current_location(next_direction, current_location)
            deliver_present(history, current_location)
        else:
            robo_current_location = move_current_location(next_direction, robo_current_location)
            deliver_present(history, robo_current_location)

    logging.info(f"Delivered presents to {len(history)} unique homes with the help of ROBO-Santa")


def move_current_location(direction, location):
    if NORTH == direction:
        return location[0], location[1] + 1
    if SOUTH == direction:
        return location[0], location[1] - 1
    if EAST == direction:
        return location[0] + 1, location[1]
    if WEST == direction:
        return location[0] - 1, location[1]
    raise Exception(f"Could not parse the given direction: {direction}")


def deliver_present(history, location):
    history[location] = True


if __name__ == "__main__":
    main()
