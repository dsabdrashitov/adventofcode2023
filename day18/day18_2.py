import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

D_R = (0, +1)
D_D = (+1, 0)
D_L = (0, -1)
D_U = (-1, 0)
DIR = {
    '0': D_R,
    '1': D_D,
    '2': D_L,
    '3': D_U,
}
DIRS = (D_R, D_D, D_L, D_U)
COM_PAT = re.compile(r"[RDUL] \d+ \(#([0-9a-f]{5})([0-3])\)")


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mult(t, m):
    return t[0] * m, t[1] * m


def solve(f):
    commands = []
    for line in f:
        match = COM_PAT.match(line.strip())
        commands.append((match.group(2), int(match.group(1), 16)))
    s = 0
    b = 1
    pos0 = (0, 0)
    for command in commands:
        d = DIR[command[0]]
        pos1 = add(pos0, mult(d, command[1]))
        if d == D_R or d == D_L:
            s = s + pos0[0] * (pos1[1] - pos0[1])
        b = b + command[1]
        pos0 = pos1
    s = abs(s)
    _logger.info(s)
    _logger.info(b)
    answer = s + 1 + b // 2
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
