from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from operator import methodcaller
from collections import namedtuple, defaultdict
from re import search
from math import prod
from queue import LifoQueue
from copy import copy

logger = init_logs(__name__)

Tile = namedtuple('Tile', ('id', 'vertical', 'horizontal', 'contents', ))
Vertical = namedtuple('Vertical', ('up', 'down'))
Horizontal = namedtuple('Horizontal', ('left', 'right'))


def main():
    tiles, all_sides = parse_input(FileReader.read_input_as_string())
    corners = get_corners(tiles, all_sides)
    logger.info(f"Corners are {corners} mult they are {prod(map(int, corners))}")


def get_corners(tiles, all_sides):
    corners = []
    for tile_id in tiles:
        tile = tiles[tile_id]
        up = side_matches(all_sides, tile.vertical.up)
        down = side_matches(all_sides, tile.vertical.down)
        left = side_matches(all_sides, tile.horizontal.left)
        right = side_matches(all_sides, tile.horizontal.right)
        matched_sides = [up, down, left, right]
        if len([side for side in matched_sides if side]) == 2:
            corners += tile.id
    return corners


def side_matches(all_sides, side):
    sides = all_sides[side]
    rev_sides = all_sides[side[::-1]]
    if sides + rev_sides == 1:
        return None
    return side if sides else rev_sides


def parse_input(raw_input):
    tiles = raw_input.split('\n\n')
    tile_map = {}
    all_sides = defaultdict(int)
    for tile in tiles:
        raw_tile = tile.split('\n')
        tile_id = search('Tile ([0-9]+):', raw_tile[0]).groups(0)
        parsed_tile = raw_tile[1:]
        up = parsed_tile[0]
        down = parsed_tile[-1]
        left = ''.join([i[0] for i in parsed_tile])
        right = ''.join([i[-1] for i in parsed_tile])
        vertical = Vertical(left, right)
        horizontal = Horizontal(up, down)
        all_sides[up] += 1
        all_sides[down] += 1
        all_sides[right] += 1
        all_sides[left] += 1
        tile_map[tile_id] = Tile(tile_id, vertical, horizontal, tile)
    return tile_map, all_sides


if __name__ == '__main__':
    main()