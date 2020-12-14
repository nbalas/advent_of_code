from collections import namedtuple

from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

Coordinates = namedtuple("Coordinates", ('x', 'y'))
Instruction = namedtuple("Instruction", ('action', 'value'))


# North -y
# South +y
# East +x
# West -x
DIRECTIONS = {
    "N": lambda current_cords, value: Coordinates(current_cords.x, current_cords.y - value),
    "E": lambda current_cords, value: Coordinates(current_cords.x + value, current_cords.y),
    "S": lambda current_cords, value: Coordinates(current_cords.x, current_cords.y + value),
    "W": lambda current_cords, value: Coordinates(current_cords.x - value, current_cords.y)
}

DEGREES_TO_DIRECTION = {
    0: "N",
    90: "E",
    180: "S",
    270: "W"
}

ROTATION = {
    "L": lambda degrees: degrees if degrees == 180 else (degrees + 180) % 360,
    "R": lambda degrees: degrees,
}

SHIP_MOVEMENT = {
    "F": lambda current_cords, waypoint, value: Coordinates(current_cords.x + (waypoint.x * value), current_cords.y + (waypoint.y * value))
}

STARTING_DIRECTION = 'E'
STARTING_DEGREES = 90


def main():
    directions = list(map(lambda d: Instruction(d[:1], int(d[1:])), FileReader.read_input_as_list()))
    final_cords = run_directions(directions)
    logger.info(f"Our final coordinates are {final_cords} with a Manhattan distance of {abs(final_cords.x) + abs(final_cords.y)}")


def run_directions(directions):
    current_ship_cords = Coordinates(0, 0)
    current_waypoint_cords = Coordinates(10, -1)
    for direction in directions:
        current_ship_cords, current_waypoint_cords = apply_direction(direction, current_ship_cords,
                                                                     current_waypoint_cords)
        logger.debug(f"Ship's coordinates {current_ship_cords}, waypoint's coords {current_waypoint_cords}")
    return current_ship_cords


def apply_direction(direction, ship_cords, waypoint):
    action = direction.action
    value = direction.value
    logger.debug(f"Executing {action} {value}")
    if action in SHIP_MOVEMENT:
        return SHIP_MOVEMENT[action](ship_cords, waypoint, value), waypoint
    if action in DIRECTIONS:
        return ship_cords, DIRECTIONS[action](waypoint, value)
    if action in ROTATION:
        degree_change = ROTATION[action](value)
        waypoint = rotate_waypoint(waypoint, degree_change)
        return ship_cords, waypoint
    logger.error(f"Could not run action {action} for value {value}")
    raise TypeError


# Part 2
def rotate_waypoint(waypoint_cords, value):
    logger.info(f"Rotating waypoint {waypoint_cords} around by {value} degrees")
    if value == 0 or value == 360:
        return waypoint_cords
    if value == 270:
        return Coordinates(waypoint_cords.y, -waypoint_cords.x)
    if value == 180:
        return Coordinates(-waypoint_cords.x, -waypoint_cords.y)
    if value == 90:
        return Coordinates(-waypoint_cords.y, waypoint_cords.x)
    logger.error(f"Could not rotate waypoint, invalid rotation amount: {value}")
    raise TypeError


if __name__ == '__main__':
    main()