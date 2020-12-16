from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

OUT_OF_SERVICE = 'x'
MAX_TIME = 1000000000000000


def main():
    current_time, buses = parse_input(FileReader.read_input_as_list())
    arriving = calculate_arrival_times(buses, current_time)
    minutes = min(arriving.keys())
    next_bus = arriving[minutes]
    logger.info(f"Bus {next_bus} is arriving in {minutes} minutes; part 1 answer: {next_bus * minutes}")

    bus_schedule = parse_required_schedule(FileReader.read_input_as_list())
    find_schedule_time(bus_schedule)



# Part 1
def calculate_arrival_times(buses, time):
    return dict(map(lambda bus: (bus - (time % bus), bus), buses))


def parse_input(raw_input):
    current_time = int(raw_input[0])
    buses = [int(bus) for bus in raw_input[1].split(',') if bus is not OUT_OF_SERVICE]
    return current_time, buses


# Part 2
def parse_required_schedule(raw_input):
    full_schedule = [bus for bus in raw_input[1].split(',')]
    bus_schedule = {}
    minute_count = 0
    for bus in full_schedule:
        if bus is OUT_OF_SERVICE:
            pass
        else:
            bus_schedule[int(bus)] = minute_count % int(bus)
        minute_count += 1
    return bus_schedule


def find_schedule_time(bus_schedule):
    buses = list(bus_schedule.keys())
    next_match = 1
    test_time = 0
    iter_value = buses[0]

    logger.info(f"Finding matching schedules from highest bus: {buses}")

    while test_time < MAX_TIME:
        arrival_times = calculate_arrival_times_for_scheduler(bus_schedule, test_time)
        if arrival_times[buses[next_match]] == bus_schedule[buses[next_match]]:
            iter_value = iter_value * buses[next_match]
            logger.info(f"Found another match:\n{arrival_times} almost is\n{bus_schedule}, new iteration value {iter_value}")
            next_match += 1
        if arrival_times == bus_schedule:
            logger.info(f"winrar, {test_time}")
            break
        test_time += iter_value


def calculate_arrival_times_for_scheduler(bus_schedule, time):
    return dict(map(lambda b: (b, (b - (time % b)) % b), bus_schedule.keys()))


if __name__ == '__main__':
    main()