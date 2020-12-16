from re import search
from collections import namedtuple
from operator import methodcaller
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

MASK = 'mask'
MEM = 'mem'
NOP = 'X'

Operation = namedtuple("Operation", ('op', 'value'))


def main():
    operations = parse_input(FileReader.read_input_as_list())
    mem = run_program(operations)
    logger.info(f"Ran program and the sum of our mem is {sum(mem.values())}")


def run_program(operations):
    mask = ''
    mem = {}
    for operation in operations:
        if MASK == operation.op:
            mask = operation.value
        else:
            mem_nums = apply_floating_mask(operation.op[1], mask, [])
            # logger.info(f"Setting value {operation.value} to mem: {mem_nums}")
            for num in mem_nums:
                mem[num] = operation.value
            # mem[operation.op[1]] = apply_mask(operation.value, mask) # Part 1
    return mem


# Part 1
def apply_mask(number, mask):
    bit_num = get_bits(number)
    new_bit_num = ''
    for i, n in enumerate(mask):
        if n is NOP:
            new_bit_num += bit_num[i]
        else:
            new_bit_num += n
    # logger.debug(f"Applied mask {mask} to num {number}: {bit_num} and got {new_bit_num}")
    return int(new_bit_num, 2)


# Part 2
def apply_floating_mask(number, mask, new_nums, new_bit_num=''):
    bit_num = get_bits(number)
    for i in range(len(new_bit_num), len(bit_num)):
        if mask[i] is NOP:
            apply_floating_mask(number, mask, new_nums, new_bit_num + '0')
            apply_floating_mask(number, mask, new_nums, new_bit_num + '1')
            return new_nums
        else:
            new_bit_num += str(int(bit_num[i]) | int(mask[i]))
    # logger.debug(f"Applied mask {mask} to num {number}: {bit_num} and got {new_bit_num}")
    new_nums.append(int(new_bit_num, 2))
    return new_nums


def get_bits(num):
    return '{:036b}'.format(num)


def parse_input(raw_input):
    return list(map(
        lambda pair:
        Operation((MEM, int(search('mem\[([0-9]+)]', pair[0]).groups()[0])), int(pair[1]))
        if MEM in pair[0] else Operation(pair[0], pair[1]),
        map(lambda p: list(map(str.strip, p)), map(methodcaller('split', '='), raw_input))))


if __name__ == '__main__':
    main()
