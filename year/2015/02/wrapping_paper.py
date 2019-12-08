import logging
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__, logging.INFO)

SMALLEST_PERIMETER = "smallest_perim"
SIDES = "sides"
VOLUME = "volume"


def parse_dimension_input(dimension_input):
    values = list(map(int, dimension_input.split('x')))
    return {
        SIDES: compute_surface_area(values),
        VOLUME: compute_volume(values),
        SMALLEST_PERIMETER: compute_smallest_perimeter(values)
    }


def compute_surface_area(values):
    if len(values) != 3:
        raise Exception("This is not a valid set of dimensions: %s", values)
    return [(2 * values[0] * values[1]),  (2 * values[0] * values[2]), (2 * values[1] * values[2])]


def compute_volume(values):
    if len(values) != 3:
        raise Exception("This is not a valid set of dimensions: %s", values)
    return values[0] * values[1] * values[2]


def compute_smallest_perimeter(values):
    if len(values) != 3:
        raise Exception("This is not a valid set of dimensions: %s", values)
    doubled_values = [value * 2 for value in values]
    return sum(doubled_values) - max(doubled_values)


def computer_paper_needed(dimension_input):
    dimension_sides = dimension_input[SIDES]
    logging.debug("Input: %s", dimension_sides)
    logging.debug("Surface area of box is: %s and the slack paper needed is: %s",
                  sum(dimension_sides), min(dimension_sides))
    # We must divide by two to get the area of the smallest side
    return (min(dimension_sides)/2) + sum(dimension_sides)


def computer_ribbon_needed(dimension_input):
    dimension_volume = dimension_input[VOLUME]
    dimension_small_perimeter = dimension_input[SMALLEST_PERIMETER]
    logging.debug("Input: %s", dimension_input)
    logging.debug("Volume area of box is: %s and the smallest perimeter is: %s",
                  dimension_volume, dimension_small_perimeter)
    # We must divide by two to get the area of the smallest side
    return dimension_volume + dimension_small_perimeter


dimensions = list(map(parse_dimension_input, FileReader.read_input_as_list()))

total_paper_needed = sum(map(computer_paper_needed, dimensions))

logging.info("Total paper elves need: %s", total_paper_needed)

total_ribbon_needed = sum(map(computer_ribbon_needed, dimensions))

logging.info("Total paper elves need: %s", total_ribbon_needed)



