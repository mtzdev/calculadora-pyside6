import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def isValidNumber(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False

def convertNumber(number: str):
    try:
        new_number = float(number)
        if new_number.is_integer():
            return int(new_number)
        return new_number

    except ValueError:
        return None
