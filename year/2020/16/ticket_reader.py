from re import search
from collections import namedtuple, defaultdict
from operator import methodcaller
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

Rule = namedtuple('Rule', ('label', 'ranges'))


def main():
    rules, your_ticket, other_tickets = parse_input(FileReader.read_input_as_string())
    valid_tickets = validate_tickets(rules, other_tickets)
    decrypted_rules = decrypt_ticket(rules, valid_tickets)

    departure_indices = [decrypted_rules[key] for key in decrypted_rules if 'departure' in key]
    final_product = 1
    for index in departure_indices:
        final_product *= your_ticket[index]

    logger.info(f"Part 2 product: {final_product}")


def decrypt_ticket(rules, tickets):
    decrypted_rules = defaultdict(list)
    for i in range(0, len(rules)):
        num_pool = set([ticket[i] for ticket in tickets])
        for rule in rules:
            if not num_pool - rule.ranges:
                logger.info(f"Rule {rule.label} matches index {i}")
                decrypted_rules[rule.label].append(i)

    sorted_rules = sorted(decrypted_rules.items(), key=lambda x: len(x[1]))

    paired_rules = {}
    for r in sorted_rules:
        possible_indices = set(r[1])

        if 1 < len(possible_indices):
            for k in paired_rules.values():
                possible_indices.remove(k)

        paired_rules[r[0]] = possible_indices.pop()


    return paired_rules


# Part 1
def validate_tickets(rules, tickets):
    available_values = set()
    invalid_values = []
    valid_tickets = []

    for rule in rules:
        available_values.update(rule.ranges)

    for ticket in tickets:
        valid_ticket = True
        for value in ticket:
            if value not in available_values:
                valid_ticket = False
                invalid_values.append(value)
        if valid_ticket:
            valid_tickets.append(ticket)

    logger.debug(f"Total invalid values {sum(invalid_values)}")
    return valid_tickets


def parse_input(raw_input):
    sections = raw_input.split('\n\n')

    rules = list(map(lambda y: Rule(y[0], list(map(str.strip, y[1].split('or')))),
        map(lambda x: x.split(':'), list(map(str.strip, sections[0].split('\n'))))))

    rules = list(map(lambda rule: Rule(rule.label, range_parser(rule.ranges)), rules))

    your_ticket = list(map(int, sections[1].split(':')[1].strip().split(',')))

    other_tickets = list(map(lambda x: list(map(int, x.split(','))), sections[2].split('\n')[1:]))

    return rules, your_ticket, other_tickets


def range_parser(ranges):
    possible_values = set()
    for num_range in ranges:
        bounds = num_range.split('-')
        possible_values.update(range(int(bounds[0]), int(bounds[1])+1))
    return possible_values


if __name__ == '__main__':
    main()