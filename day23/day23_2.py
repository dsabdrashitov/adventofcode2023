import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

FOREST = '#'
TRAIL = '.'

D = {
    '>': (0, +1),
    'v': (+1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def find_longest(n, m, field, start, end):
    answer = 0
    stack = [([start])]
    while len(stack) > 0:
        curpath = stack.pop()
        cur = curpath[-1]
        if field[cur[0]][cur[1]] == FOREST:
            continue
        if cur in curpath[:-1]:
            continue
        if cur == end:
            _logger.debug(f"{answer} <?- {len(curpath) - 1}")
            _logger.debug(f"steck_size = {len(stack)}")
            answer = max(answer, len(curpath) - 1)
            continue
        for d in D.values():
            stack.append(curpath + [add(cur, d)])
    return answer


def solve(f):
    field = []
    for line in f:
        field.append(FOREST + line.strip() + FOREST)
    m = len(field[0])
    field.append(FOREST * m)
    field.insert(0, FOREST * m)
    n = len(field)
    start = (1, field[1].index(TRAIL))
    end = (n - 2, field[n - 2].index(TRAIL))
    _logger.info(f"{start} -> {end}")
    answer = find_longest(n, m, field, start, end)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    main()
