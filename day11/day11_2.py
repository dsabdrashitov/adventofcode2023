import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

# MULTIPLICATION = 100
MULTIPLICATION = 1000000

GALAXY = '#'


def calc_doubled(field):
    n = len(field)
    m = len(field[0])
    cntn = [0] * n
    cntm = [0] * m
    for i in range(n):
        for j in range(m):
            if field[i][j] == GALAXY:
                cntn[i] = cntn[i] + 1
                cntm[j] = cntm[j] + 1
    doubled = [[0] * (n + 1), [0] * (m + 1)]
    for i in range(n):
        doubled[0][i + 1] = doubled[0][i] + (0 if cntn[i] > 0 else 1)
    for j in range(m):
        doubled[1][j + 1] = doubled[1][j] + (0 if cntm[j] > 0 else 1)
    return doubled


def find_stars(field):
    result = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == GALAXY:
                result.append((i, j))
    return result


def solve(f):
    field = []
    for line in f:
        field.append(line.strip())
    doubled = calc_doubled(field)
    stars = find_stars(field)
    answer = 0
    for i in range(len(stars)):
        for j in range(i):
            addi = (doubled[0][stars[i][0]] - doubled[0][stars[j][0] + 1]) * (MULTIPLICATION - 1)
            addj = (doubled[1][stars[i][1]] - doubled[1][stars[j][1] + 1]) * (MULTIPLICATION - 1)
            d = abs(stars[i][0] - stars[j][0] + addi) + abs(stars[i][1] - stars[j][1] + addj)
            answer = answer + d
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
