import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

START = 'S'
D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
PIPES = {
    "F": (D[1], D[0]),
    "J": (D[3], D[2]),
    "7": (D[2], D[1]),
    "L": (D[3], D[0]),
    "|": (D[1], D[3]),
    "-": (D[0], D[2]),
}


def inside(p, field):
    return 0 <= p[0] < len(field) and 0 <= p[1] < len(field[p[0]])


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def find_start(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == START:
                return i, j
    raise Exception("Start not found.")


def find_exit(start, field):
    for i in range(len(D)):
        e = add(start, D[i])
        if inside(e, field):
            if add(e, PIPES[field[e[0]][e[1]]][0]) == start or add(e, PIPES[field[e[0]][e[1]]][1]) == start:
                return e


def find_loop(start, field):
    exit1 = find_exit(start, field)
    result = [start, exit1]
    while result[-1] != start:
        e0 = add(result[-1], PIPES[field[result[-1][0]][result[-1][1]]][0])
        e1 = add(result[-1], PIPES[field[result[-1][0]][result[-1][1]]][1])
        if e0 == result[-2]:
            result.append(e1)
        elif e1 == result[-2]:
            result.append(e0)
        else:
            raise Exception("Botva!")
    return result


def solve(f):
    field = []
    for line in f:
        field.append(line.strip())
    start = find_start(field)
    _logger.info(start)
    loop = find_loop(start, field)
    answer = (len(loop) - 1) // 2
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
