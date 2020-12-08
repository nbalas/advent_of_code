from math import prod
from collections import namedtuple
from operator import attrgetter
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

import re

logger = init_logs(__name__)

BagData = namedtuple("BagData", ('count', 'color'))

MAIN_BAG = 'shiny gold'


def main():
    bag_map = format_rules(FileReader.read_input_as_list())
    bags_visited = set()
    find_my_parents(bag_map, bags_visited, MAIN_BAG)
    total_bags = find_my_bags(bag_map, MAIN_BAG, 0)
    logger.info("We can put our bag in {} other bags".format(len(bags_visited)))
    logger.info("We have to carry {} bags, whew heavy!".format(total_bags))


# Part 1: we simply need to find all nodes we visit
def find_my_parents(bag_map, bags_visited, current_bag):
    for bag_data in bag_map[current_bag]:
        parent = bag_data.color
        if parent in bags_visited:
            logger.info("Bag {} has already been visited".format(parent))
            continue
        logger.info("Visiting bag {} now!".format(parent))
        bags_visited.add(parent)
        find_my_parents(bag_map, bags_visited, parent)


# Part 2: The search needs to multiply the single path down the tree then add it to all other paths
def find_my_bags(bag_map, current_bag, total_count):
    for bag_data in bag_map[current_bag]:
        logger.info("Count is {}".format(total_count))
        bag_color = bag_data.color
        bag_count = int(bag_data.count)  # multiply this by all inner bags
        logger.info("Found {} {} bag(s)".format(bag_count, bag_color))
        total_count += bag_count * find_my_bags(bag_map, bag_color, 1)

    return total_count


# light salmon bags contains 5 dark brown bags, 2 dotted coral bags, 5 mirrored turquoise bags
# -> {"dark brown": [(5, "light salmon")],
#     "dotted coral": [(2, "light salmon")],
#     "mirrored turquoise": [(5, "light salmon")]}
def format_rules(raw_rules):
    bag_map = {}
    for raw_rule in raw_rules:
        split_bag_input = raw_rule.split('contain')
        parent_bag = parse_bag_color(split_bag_input[0])
        inner_bags = split_bag_input[1]
        # process_inner_bags_leaves(inner_bags, parent_bag, bag_map) # UNCOMMENT THIS FOR PART 1
        process_inner_bags_roots(inner_bags, parent_bag, bag_map)  # PART 2
    return bag_map


# Part 2: we create the tree using the "roots" as roots, i.e. going from outer bags to inner
def process_inner_bags_roots(raw_inner_bags, parent_bag, bag_map):
    if 'no other bags' in raw_inner_bags:
        add_bag_to_dict(parent_bag, None, None, bag_map)  # Initialize the parent bag in the dict
        return

    inner_bags = list(map(str.strip, raw_inner_bags.split(',')))
    for inner_bag in inner_bags:
        result = re.search('^([0-9]+)(.*)', inner_bag)
        if result is None:
            logger.info("hell")
        bag_count = result.groups()[0]
        bag_color = parse_bag_color(result.groups()[1])
        add_bag_to_dict(parent_bag, bag_count, bag_color, bag_map)


# Part 1: we create the tree using the "leaves" as roots, i.e. going from inner bags to outer
def process_inner_bags_leaves(raw_inner_bags, parent_bag, bag_map):
    add_bag_to_dict(parent_bag, None, None, bag_map)  # Initialize the parent bag in the dict

    if 'no other bags' in raw_inner_bags:
        return

    inner_bags = list(map(str.strip, raw_inner_bags.split(',')))
    for inner_bag in inner_bags:
        result = re.search('^([0-9]+)(.*)', inner_bag)
        bag_count = result.groups()[0]
        bag_color = parse_bag_color(result.groups()[1])
        add_bag_to_dict(bag_color, bag_count, parent_bag, bag_map)


def add_bag_to_dict(key, bag_count, bag_value, bag_map):
    if key not in bag_map:
        bag_map[key] = []

    if bag_value is None:
        return

    bag_map[key].append(BagData(bag_count, bag_value))


def parse_bag_color(bag):
    return re.split('bags | bag', bag)[0].strip()


if __name__ == '__main__':
    main()