
# parse.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
Module with functions to parse user input.
"""

from pathlib import Path

def create_path(line: str) -> Path:
    if line[0] == '"':
        line = line[1:-1]
    path = Path(line)
    if path.exists():
        return path
    else:
        return None


def find_pathway(line) -> int:
    for i in range(len(line), 0, -1):
        if Path(line[:i]).exists():
            return i


def find_quoted_input(line: str) -> tuple:
    qt_substr = None
    if line[0] == '"':
        end_quote = line[1:].find('"')
        qt_substr = line[1:end_quote+1]
        next_index = line[end_quote:].find('-') + end_quote
        return qt_substr, next_index


def parse_c_input(argument: str) -> dict:
    argument_dict = {}
    argument = argument[2:]
    next_index = 0
    if argument[0] == '"': # if file path is quoted
        directory, next_index = find_quoted_input(argument)
        if Path(directory).is_dir():
            argument_dict['directory'] = directory
        else:
            return None
    else:
        next_index = argument.find('-')
        directory = argument[0:next_index-1]

        if Path(directory).is_dir():
            argument_dict['directory'] = directory
        else:
            print("[ERROR] Directory is not valid")
            return None
    
    argument = argument[next_index:]
    for i in range(len(argument)):
        if argument[i] == '-':
            next_index = argument[i:].find(' ')
            option = argument[i:next_index]
            next_index = next_index + 1
            if argument[next_index] == '"':
                name = argument[next_index + 1:-1]
            else:
                name = argument[next_index:]
            argument_dict['option'] = option
            argument_dict['name'] = name

    return argument_dict


def parse_e_input(argument: str) -> tuple:
    argument_list = []
    argument = argument[2:]
    for i in range(len(argument)):
        if argument[i] == '-':
            edited_argument = argument[i:]
            next_index = edited_argument.find(' ')
            if next_index == -1:
                option = edited_argument
                argument_list.append({'option': option})
                continue
            option = edited_argument[:next_index]
            edited_argument = edited_argument[next_index:]
            last_index = edited_argument.find(' -')
            if last_index == -1:
                opt_input = edited_argument[1:]
            else:
                opt_input = edited_argument[1:last_index]
            argument_list.append({'option': option, 'opt_input': opt_input})

    return tuple(argument_list)

