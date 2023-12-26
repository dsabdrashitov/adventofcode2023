import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"


def allzero(a):
    for x in a:
        if x != 0:
            return False
    return True


def encode(a):
    result = [list(a)]
    for i in range(len(a) - 1):
        der = []
        for j in range(len(result[i]) - 1):
            der.append(result[i][j + 1] - result[i][j])
        result.append(der)
        if allzero(der):
            break
    return result


def solve(f):
    answer = 0
    for line in f:
        a = [int(s) for s in line.strip().split()]
        b = encode(a)
        b[-1].append(0)
        for i in range(len(b) - 1, 0, -1):
            b[i - 1].append(b[i - 1][-1] + b[i][-1])
        _logger.debug(b)
        answer = answer + b[0][-1]
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
