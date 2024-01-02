import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

REPEAT = 5

BROKEN = '#'
NORMAL = '.'
UNKNOWN = '?'
LINE_PAT = re.compile(r"([#.?]+) ([\d,]+)")
NUM_PAT = re.compile(r"\d+")


def is_good(i, length, line):
    if i + length > len(line):
        return False
    for j in range(i, i + length):
        if line[j] == NORMAL:
            return False
    return True


def solve_variants(line, desc):
    a = [[[0, 0] for _ in range(len(desc) + 1)] for _ in range(len(line) + 1)]
    a[0][0][0] = 1
    for i in range(len(line)):
        for j in range(len(desc) + 1):
            if line[i] == NORMAL or line[i] == UNKNOWN:
                a[i + 1][j][0] = a[i + 1][j][0] + a[i][j][1]
                a[i + 1][j][0] = a[i + 1][j][0] + a[i][j][0]
            if j < len(desc) and is_good(i, desc[j], line):
                a[i + desc[j]][j + 1][1] = a[i + desc[j]][j + 1][1] + a[i][j][0]
    result = a[len(line)][len(desc)][0] + a[len(line)][len(desc)][1]
    _logger.debug(result)
    return result


def solve(f):
    lines = []
    descriptions = []
    for line in f:
        match = LINE_PAT.match(line)
        lines.append(UNKNOWN.join([match.group(1)] * REPEAT))
        descriptions.append([int(s) for s in NUM_PAT.findall(match.group(2))] * REPEAT)
    answer = 0
    for i in range(len(lines)):
        answer = answer + solve_variants(lines[i], descriptions[i])
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
