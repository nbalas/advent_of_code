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
Point = namedtuple("Point", ["symbol", "wire_id"])
starting_location = Coordinates(0, 0)

intersections = []


def main():
    paths = FileReader.read_input_as_list()
    first_path = list(map(parse_movement_input, paths[0].split(',')))
    second_path = list(map(parse_movement_input, paths[1].split(',')))

    ## Part 1
    circuit = {}
    current_location = starting_location
    init_circuit(circuit)
    for movement in first_path:
        current_location = process_movement(circuit, movement, current_location, WIRE_A)

    print_circuit(circuit)

    current_location = starting_location
    for movement in second_path:
        current_location = process_movement(circuit, movement, current_location, WIRE_B)

    print_circuit(circuit)
    print(intersections)
    print(f"Closest point to the start is a distance of : {min(map(sum_coordinate, intersections))}")


def sum_coordinate(coordinate):
    return abs(coordinate.x) + abs(coordinate.y)


def parse_movement_input(raw_input):
    return Movement(raw_input[0], int(raw_input[1:]))


def process_movement(circuit, movement, current_location, wire_id):
    # print(f"Processing movement: {movement}")
    if RIGHT == movement.direction:
        end_x_coordinate = current_location.x + movement.distance
        for i in range(current_location.x + 1, end_x_coordinate - 1):
            place_coordinate(circuit, Coordinates(i, current_location.y), HORIZONTAL, wire_id)
        place_coordinate(circuit, Coordinates(end_x_coordinate, current_location.y), END_MOVEMENT, wire_id)
        return Coordinates(end_x_coordinate, current_location.y)
    elif LEFT == movement.direction:
        end_x_coordinate = current_location.x - movement.distance
        for i in range(end_x_coordinate + 1, current_location.x - 1):
            place_coordinate(circuit, Coordinates(i, current_location.y), HORIZONTAL, wire_id)
        place_coordinate(circuit, Coordinates(end_x_coordinate, current_location.y), END_MOVEMENT, wire_id)
        return Coordinates(end_x_coordinate, current_location.y)
    elif UP == movement.direction:
        end_y_coordinate = current_location.y + movement.distance
        for i in range(current_location.y + 1, end_y_coordinate - 1):
            place_coordinate(circuit, Coordinates(current_location.x, i), VERTICAL, wire_id)
        place_coordinate(circuit, Coordinates(current_location.x, end_y_coordinate), END_MOVEMENT, wire_id)
        return Coordinates(current_location.x, end_y_coordinate)
    elif DOWN == movement.direction:
        end_y_coordinate = current_location.y - movement.distance
        for i in range(end_y_coordinate + 1, current_location.y - 1):
            place_coordinate(circuit, Coordinates(current_location.x, i), VERTICAL, wire_id)
        place_coordinate(circuit, Coordinates(current_location.x, end_y_coordinate), END_MOVEMENT, wire_id)
        return Coordinates(current_location.x, end_y_coordinate)
    else:
        raise Exception(f"Unknown type of direction: {movement.direction}")


def place_coordinate(circuit, coordinate, symbol, wire_id):
    # print(f"Putting coordinate {coordinate} in circuit")
    if coordinate in circuit and circuit[coordinate].wire_id != wire_id:
        if (circuit[coordinate].symbol == END_MOVEMENT or
                circuit[coordinate].symbol == HORIZONTAL or
                circuit[coordinate].symbol == VERTICAL):
            print(f"Coordinate {coordinate} exists, we found {circuit[coordinate]} there")
            circuit[coordinate] = Point(CROSS, wire_id)
            intersections.append(coordinate)
        elif circuit[coordinate] == EMPTY:
            circuit[coordinate] = Point(symbol, wire_id)
    else:
        circuit[coordinate] = Point(symbol, wire_id)


def init_circuit(circuit):
    circuit[starting_location] = START


def print_circuit(circuit):
    for i in range(-10, 10):
        print(' ', end='')
        for j in range(-10, 10):
            coordinate = Coordinates(j, i * -1)
            if coordinate in circuit:
                print(circuit[coordinate], end=' ')
            else:
                print(EMPTY, end=' ')
        print()


if __name__ == '__main__':
    main()
