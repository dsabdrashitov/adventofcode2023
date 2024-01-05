import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

CYCLES = 1000000000

FIXED = '#'
ROUND = 'O'
FREE = '.'


def do_cycle(field, do_debug=False):
    ground = [0] * len(field[0])
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[j] = i + 1
            elif field[i][j] == ROUND:
                tmp = field[i][j]
                field[i][j] = FREE
                field[ground[j]][j] = tmp
                ground[j] = ground[j] + 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("NORTH:")
        for x in field:
            _logger.debug(''.join(x))
    ground = [0] * len(field)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[i] = j + 1
            elif field[i][j] == ROUND:
                tmp = field[i][j]
                field[i][j] = FREE
                field[i][ground[i]] = tmp
                ground[i] = ground[i] + 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("WEST:")
        for x in field:
            _logger.debug(''.join(x))
    ground = [len(field)] * len(field[0])
    for i in range(len(field) - 1, -1, -1):
        for j in range(len(field[i]) - 1, -1, -1):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[j] = i
            elif field[i][j] == ROUND:
                tmp = field[i][j]
                field[i][j] = FREE
                field[ground[j] - 1][j] = tmp
                ground[j] = ground[j] - 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("SOUTH:")
        for x in field:
            _logger.debug(''.join(x))
    ground = [len(field[0])] * len(field)
    for i in range(len(field) - 1, -1, -1):
        for j in range(len(field[i]) - 1, -1, -1):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[i] = j
            elif field[i][j] == ROUND:
                tmp = field[i][j]
                field[i][j] = FREE
                field[i][ground[i] - 1] = tmp
                ground[i] = ground[i] - 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("EAST:")
        for x in field:
            _logger.debug(''.join(x))


def collect(field):
    return ''.join([''.join(field[i]) for i in range(len(field))])


def solve(f):
    field = []
    for line in f:
        line = line.strip()
        field.append([line[i] for i in range(len(line))])
    history = {collect(field): 0}
    done = 0
    while done < CYCLES:
        do_cycle(field, done == 0)
        done = done + 1
        cf = collect(field)
        if cf in history:
            break
        else:
            history[cf] = done
    _logger.info(f"{history[collect(field)]} -> {done}")
    skip = done - history[collect(field)]
    rem = (CYCLES - done) % skip
    for _ in range(rem):
        do_cycle(field)
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
    logging.basicConfig(level=logging.DEBUG)
    main()
