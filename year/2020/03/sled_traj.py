from collections import namedtuple
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

Coordinates = namedtuple('Coordinates', ('x', 'y'))
Trajectory = namedtuple('Trajectory', ('x', 'y'))
starting_coordinates = Coordinates(0, 0)
x_traj = 1  # Right
y_traj = 1  # Down
EMPTY = '.'
TREE = '#'

test_trajectories = [Trajectory(1, 1), Trajectory(3, 1), Trajectory(5, 1), Trajectory(7, 1), Trajectory(1, 2)]


# First attempt
def main():
    tree_map = list(map(list, FileReader.read_input_as_list()))
    x_size = len(tree_map[0])
    product = 1
    for trajectory in test_trajectories:
        current_cords = update_coordinate(starting_coordinates, trajectory.x, trajectory.y)
        trees_hit = 0
        while current_cords.y < len(tree_map):
            # logger.debug("Validating row {} at place {}".format(current_cords.y, current_cords.x % trajectory.x))
            if tree_map[current_cords.y][current_cords.x % x_size] == TREE:
                # logger.info("hit tree at {}, {}".format(current_cords.x, current_cords.y))
                trees_hit += 1
            current_cords = update_coordinate(current_cords, trajectory.x, trajectory.y)
        logger.info("Was hit by {} trees".format(trees_hit))
        product *= trees_hit
    logger.info("Final tree product: {}".format(product))


def update_coordinate(coordinate, x, y):
    return Coordinates(coordinate.x + x, coordinate.y + y)


# Second attempt and got the same answer as first, but is better
def do_better():
    tree_map = list(map(list, FileReader.read_input_as_list()))
    product = 1
    for trajectory in test_trajectories:
        trees_hit = 0
        for counter, tree_line in enumerate(tree_map):
            x_coord = (counter * trajectory.x) % len(tree_line)
            if tree_line[x_coord] == TREE:
                # logger.info("hit tree at row {} place {}".format(counter, x_coord))
                trees_hit += 1
        logger.info("Was hit by {} trees".format(trees_hit))
        product *= trees_hit
    logger.info("Final tree product: {}".format(product))


if __name__ == '__main__':
    main()
