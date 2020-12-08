from operator import methodcaller
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)


def main():
    groups = parse_groups(FileReader.read_input_as_string())
    unique_answers = list(map(filter_for_all_yes, groups))
    sum_of_unique_answers = sum(list(map(len, unique_answers)))
    logger.info("There are {} unique answers".format(sum_of_unique_answers))


# Part 2
def filter_for_all_yes(group):
    yes_answers = dict()
    for answers in group:
        for a in answers:
            if a not in yes_answers:
                yes_answers[a] = 0
            yes_answers[a] += 1
    return list(filter(lambda i: i[1] is len(group), yes_answers.items()))


# Part 1
def get_unique_answers(group):
    yes_answers = dict()
    for answers in group:
        for a in answers:
            if a not in yes_answers:
                yes_answers[a] = 0
            yes_answers[a] += 1
    return yes_answers


def parse_groups(raw_answers):
    raw_groups = raw_answers.split("\n\n")
    return list(map(methodcaller('split', '\n'), raw_groups))


if __name__ == '__main__':
    main()