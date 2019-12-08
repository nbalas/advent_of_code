from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from collections import namedtuple

logger = init_logs(__name__)

start, end = FileReader.read_input_as_string().split("-")

# Six digit number
# Single digit is always increasing
# At least one double digit i.e. 11 or 44

possible_passwords = []
for num in range(int(start), int(end) + 1):
    num = str(num)
    if num == ''.join(sorted(num)):
        print(f"Given num: {num} and when sorted {''.join(sorted(num))}")
        for c in num:
            # if num.count(c) > 1: ## Part 1 Answer
            if num.count(c) == 2: ## Part 2 Answer
                print(f"THIS COULD BE A PASSWORD: {num}")
                possible_passwords.append(num)
                break

print(f"There are {len(possible_passwords)} possible passwords")
