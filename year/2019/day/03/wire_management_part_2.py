import operator
from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from collections import namedtuple

logger = init_logs(__name__)

WIRE_A = "A"
WIRE_B = "B"

RIGHT = 'R'
LEFT = 'L'
DOWN = 'D'
UP = 'U'

START = 'o'
CROSS = 'X'
END_MOVEMENT = '+'
HORIZONTAL = '-'
VERTICAL = '|'
EMPTY = '.'

Movement = namedtuple("Movement", ["direction", "distance"])
Coordinates = namedtuple("Coordinates", ["x", "y"])
Point = namedtuple("Point", ["symbol", "wire_id", "distance_traveled"])
starting_location = Coordinates(0, 0)

intersections = []


def main():
    paths = FileReader.read_input_as_list()
    first_path = list(map(parse_movement_input, paths[0].split(',')))
    second_path = list(map(parse_movement_input, paths[1].split(',')))

    circuit = {}
    distance_traveled = 0
    current_location = starting_location
    init_circuit(circuit)
    for movement in first_path:
        current_location, distance_traveled = process_movement(circuit, movement, current_location, WIRE_A,
                                                               distance_traveled)

    distance_traveled = 0
    current_location = starting_location
    for movement in second_path:
        current_location, distance_traveled = process_movement(circuit, movement, current_location, WIRE_B,
                                                               distance_traveled)

    print(intersections)
    print(f"Closest point to the start is a distance of : {min(intersections)}")


def parse_movement_input(raw_input):
    return Movement(raw_input[0], int(raw_input[1:]))


def process_movement(circuit, movement, current_location, wire_id, distance_traveled):
    print(f"Processing movement: {movement}")
    if RIGHT == movement.direction:
        end_x_coordinate = current_location.x + movement.distance
        for i in range(current_location.x + 1, end_x_coordinate):
            distance_traveled += 1
            place_coordinate(circuit, Coordinates(i, current_location.y), HORIZONTAL, wire_id, distance_traveled)
        distance_traveled += 1
        place_coordinate(circuit, Coordinates(end_x_coordinate, current_location.y), END_MOVEMENT, wire_id,
                         distance_traveled)
        return Coordinates(end_x_coordinate, current_location.y), distance_traveled
    elif LEFT == movement.direction:
        end_x_coordinate = current_location.x - movement.distance
        for i in reversed(range(end_x_coordinate + 1, current_location.x)):
            distance_traveled += 1
            place_coordinate(circuit, Coordinates(i, current_location.y), HORIZONTAL, wire_id, distance_traveled)
        distance_traveled += 1
        place_coordinate(circuit, Coordinates(end_x_coordinate, current_location.y), END_MOVEMENT, wire_id,
                         distance_traveled)
        return Coordinates(end_x_coordinate, current_location.y), distance_traveled
    elif UP == movement.direction:
        end_y_coordinate = current_location.y + movement.distance
        for i in range(current_location.y + 1, end_y_coordinate):
            distance_traveled += 1
            place_coordinate(circuit, Coordinates(current_location.x, i), VERTICAL, wire_id, distance_traveled)
        distance_traveled += 1
        place_coordinate(circuit, Coordinates(current_location.x, end_y_coordinate), END_MOVEMENT, wire_id,
                         distance_traveled)
        return Coordinates(current_location.x, end_y_coordinate), distance_traveled
    elif DOWN == movement.direction:
        end_y_coordinate = current_location.y - movement.distance
        for i in reversed(range(end_y_coordinate + 1, current_location.y)):
            distance_traveled += 1
            place_coordinate(circuit, Coordinates(current_location.x, i), VERTICAL, wire_id, distance_traveled)
        distance_traveled += 1
        place_coordinate(circuit, Coordinates(current_location.x, end_y_coordinate), END_MOVEMENT, wire_id,
                         distance_traveled)
        return Coordinates(current_location.x, end_y_coordinate), distance_traveled
    else:
        raise Exception(f"Unknown type of direction: {movement.direction}")


def place_coordinate(circuit, coordinate, symbol, wire_id, distance_traveled):
    print(f"Putting coordinate {coordinate} in circuit we have traveled {distance_traveled}")
    if coordinate in circuit:
        if circuit[coordinate].wire_id != wire_id and \
                (circuit[coordinate].symbol == END_MOVEMENT or
                 circuit[coordinate].symbol == HORIZONTAL or
                 circuit[coordinate].symbol == VERTICAL):
            print(f"Coordinate {coordinate} exists, we found {circuit[coordinate]} there")
            intersections.append(circuit[coordinate].distance_traveled + distance_traveled)
            circuit[coordinate] = Point(CROSS, wire_id, distance_traveled)
        elif circuit[coordinate] == EMPTY:
            circuit[coordinate] = Point(symbol, wire_id, distance_traveled)
    else:
        circuit[coordinate] = Point(symbol, wire_id, distance_traveled)


def init_circuit(circuit):
    circuit[starting_location] = START


def print_circuit(circuit):
    for i in range(-10, 10):
        print(' ', end='')
        for j in range(-10, 10):
            coordinate = Coordinates(j, i * -1)
            if coordinate in circuit:
                print(circuit[coordinate].symbol, end=' ')
            else:
                print(EMPTY, end=' ')
        print()


if __name__ == '__main__':
    main()
