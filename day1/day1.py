import re

# NAME = "sample.in"
NAME = "input.txt"

DIGITS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

BACK = {v: k for k, v in DIGITS.items()}

BASE = 5

current_line = None


def next_token(f):
    global current_line
    if current_line is None:
        current_line = f.readline()
    while True:
        current_line = current_line.strip()
        if len(current_line) == 0:
            current_line = f.readline()
            # EOF, empty line has /n at the end
            if len(current_line) == 0:
                return None
        else:
            i = 0
            while i < len(current_line) and not str.isspace(current_line[i]):
                i = i + 1
            result = current_line[:i]
            current_line = current_line[i:]
            return result


def eol(f):
    global current_line
    if current_line is None:
        current_line = f.readline()
    current_line = current_line.strip()
    return len(current_line) == 0


def solve(f):
    num_sum = 0
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        digits = re.findall(r'\d', line)
        first = digits[0]
        last = digits[-1]
        num = int(first + last)
        num_sum = num_sum + num
    return num_sum


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
