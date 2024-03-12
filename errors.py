
# errors.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
Module with functions to deal with error and exception handling in the journal system.
"""

CMD_ERROR_MSG = "[CommandError] Command is not valid."
LEN_ERROR_MSG = "[LengthError] Blank posts are not allowed."

class CommandError(Exception):
    """
    Raised when the user doesn't enter a valid command.
    """

class LengthError(Exception):
    """
    Raised when the user inputs a blank post or bio.
    """

def valid_command(cmd:str) -> None:
    """
    Returns true if the inputted command is valid.
    """
    commands = ('L', 'D', 'R', 'O', 'E', 'P')
    try:
        if cmd not in commands:
            raise CommandError
        else:
            return True
    except CommandError:
        print(CMD_ERROR_MSG)
        return False

def valid_len(message:str) -> None:
    """
    Returns true if the message is not empty or purely whitespace.
    """
    try:
        if (len(message) == 0) or (message.isspace()):
            raise LengthError
        else:
            return True
    except LengthError:
        print(LEN_ERROR_MSG)
        return False
