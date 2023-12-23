import sys
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


def go(cur, field, goal, used):
    if used[cur[0]][cur[1]]:
        return -1
    if field[cur[0]][cur[1]] == FOREST:
        return -1
    if cur == goal:
        return 0
    used[cur[0]][cur[1]] = True
    if field[cur[0]][cur[1]] == TRAIL:
        result = -1
        for d in D.values():
            ret = go(add(cur, d), field, goal, used)
            if ret != -1:
                result = max(result, ret + 1)
    else:
        ret = go(add(cur, D[field[cur[0]][cur[1]]]), field, goal, used)
        if ret == -1:
            result = -1
        else:
            result = ret + 1
    used[cur[0]][cur[1]] = False
    return result


def find_longest(n, m, field, start, end):
    used = [[False] * m for _ in range(n)]
    return go(start, field, end, used)


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
    logging.basicConfig(level=logging.INFO)
    _logger.info(f"recursionlimit = {sys.getrecursionlimit()}")
    sys.setrecursionlimit(10000)
    main()
