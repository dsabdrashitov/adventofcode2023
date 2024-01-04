import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

FIXED = '#'
ROUND = 'O'
FREE = '.'


def solve(f):
    field = []
    for line in f:
        line = line.strip()
        field.append([line[i] for i in range(len(line))])
    ground = [0] * len(field[0])
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[j] = i + 1
            elif field[i][j] == ROUND:
                field[i][j] = FREE
                field[ground[j]][j] = ROUND
                ground[j] = ground[j] + 1
            else:
                raise Exception("Wrong input")
    for x in field:
        _logger.debug(''.join(x))
    answer = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == ROUND:
                answer = answer + len(field) - i
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
