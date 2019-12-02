import logging
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

UP = '('
DOWN = ')'

floor_modifier = {
    UP: 1,
    DOWN: -1
}


def navigate_stairs(direction):
    if direction in floor_modifier:
        return floor_modifier[direction]
    logging.error("Direction %s is not in our map! %s", direction, floor_modifier)


directions = FileReader.read_input_as_string()

current_floor = 0
input_position = 0
for char in directions:
    current_floor += navigate_stairs(char)
    # This is for Part 2
    input_position += 1
    if current_floor < 0:
        logging.info("Santa is in the basement (%s) on position: %s", current_floor, input_position)
        exit(0)

# Part 1
logging.info("Santa made it to floor: %s", current_floor)

