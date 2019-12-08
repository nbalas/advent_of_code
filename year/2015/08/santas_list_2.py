from readers.file_reader import FileReader

## Do not count
# ""

## Escape sequences
# \\
# \"
# \x**

BACKSLASH = r'\\'
QUOTE = r'\"'
HEX = r'\x'

non_in_mem_value = {
    BACKSLASH: 1,
    QUOTE: 1,
    HEX: 3
}


def escape_characters(name):
    escaped_name = ['"']
    for char in name:
        if char in ['"', '\\']:
            escaped_name.append(f"\\{char}")
        else:
            escaped_name.append(char)
    escaped_name.append('"')
    built_escaped_name = ''.join(escaped_name)
    print(f"Processed name {name} to {built_escaped_name}")
    return built_escaped_name

def main():
    names = map(escape_characters, map(str.strip, FileReader.read_input_as_list()))
    in_mem = 0
    code_representation = 0
    for name in names:
        skip = 0
        trimmed_name = name[1:len(name)-1]
        code_representation += len(name)
        in_mem += len(trimmed_name)
        for i, _ in enumerate(trimmed_name):
            if i > len(trimmed_name) - 1:
                break
            eval_string = trimmed_name[i:i+2]
            if skip > 0:
                print(f"Skipping with {skip} left")
                skip -= 1
                continue
            print(f"Processing {eval_string} in {trimmed_name}")
            if eval_string in non_in_mem_value:
                print(f"Found {eval_string} in name")
                skip = non_in_mem_value[eval_string]
                in_mem -= skip
                continue

    print(f"There are {in_mem} chars in mem and {code_representation} chars for actual code representation)")
    print(f"Your answer is: {code_representation - in_mem}")


if __name__ == "__main__":
    main()
