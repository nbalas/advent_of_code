from collections import namedtuple
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

ROWS = 127
SEATS = 7

LOWER = ['F', 'L']
UPPER = ['B', 'R']

BoardingPass = namedtuple('BoardingPass', ("row", "seat", "seatId"))


def main():
    passes = FileReader.read_input_as_list()
    parsed_passes = list(map(parse_boarding_pass, passes))
    highest_seat_id = max(parsed_passes, key=lambda v: v.seatId)
    logger.info("Highest seat id is: {}".format(highest_seat_id.seatId)) # Part 1

    seat_ids = list(map(lambda p: p.seatId, parsed_passes))
    seat_ids.sort()
    current_seat_id = seat_ids[0]
    while True:
        if current_seat_id not in seat_ids:
            break
        current_seat_id += 1
    logger.info("Our seat is: {}".format(current_seat_id))



def parse_boarding_pass(boarding_pass):
    row = decode_code(boarding_pass[:7], ROWS)
    seat = decode_code(boarding_pass[7:], SEATS)
    return BoardingPass(row, seat, compute_seat_id(row, seat))


def decode_code(code, base):
    lower = 0
    upper = base
    for c in code:
        if c in LOWER:
            upper = upper - halve_difference(lower, upper)
        elif c in UPPER:
            lower = lower + halve_difference(lower, upper)
        else:
            logger.error("Unknown code character! {}".format(c))
    decoded_code = lower if code[-1] in LOWER else upper
    return decoded_code


def halve_difference(lower, upper):
    return ((upper - lower) + 1) // 2


def compute_seat_id(row, seat):
    return row * 8 + seat


if __name__ == '__main__':
    main()