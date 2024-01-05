import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

INSTRUCTION_PAT = re.compile(r"[^,]+")


def hash17(s):
    result = 0
    for c in s:
        result = ((result + ord(c)) * 17) % 256
    return result


def solve(f):
    instructions = []
    for line in f:
        line = line.strip()
        instructions.extend(INSTRUCTION_PAT.findall(line))
    answer = 0
    for i in instructions:
        answer = answer + hash17(i)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
