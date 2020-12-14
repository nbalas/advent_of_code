from collections import namedtuple, defaultdict
from itertools import permutations

from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

JOLT_RANGE = 3


def main():
    adapters = sorted(map(int, FileReader.read_input_as_list()))
    differences = calculate_differences(adapters)
    logger.info(f"Our adapter differences: {differences} and answer: {differences[1] * differences[3]}")
    count_all_permutations(adapters)


# Part 1
def calculate_differences(adapters):
    differences = {i + 1: 0 for i in range(JOLT_RANGE)}
    # Add the first adapter into the list
    differences[adapters[0]] += 1

    for count, adapter in enumerate(adapters[1:]):
        differences[adapter - adapters[count]] += 1

    # Adapter is always three higher than what is given so
    differences[3] += 1
    return differences


# Part 2
def count_all_permutations(adapters):
    adapter_count = defaultdict(int)
    adapter_count[0] = 1

    for adapter in adapters:
        for i in range(1, 4):
            adapter_count[adapter] += adapter_count[adapter - i]
        logger.info(adapter_count)
    logger.info(f"There are {adapter_count[max(adapters)]} possible variations")


if __name__ == '__main__':
    main()