import logging

_logger = logging.getLogger(__name__)

NAME = "sample.in"
# NAME = "input.txt"

CYCLES = 1000000000

FIXED = '#'
ROUND = 'O'
FREE = '.'


def collect_pos(field, count):
    result = [(-1, -1)] * count
    for i in range(len(field)):
        for j in range(len(field[i])):
            if isinstance(field[i][j], int):
                result[field[i][j]] = (i, j)
    return result


def do_cycle(field, do_debug = False):
    ground = [0] * len(field[0])
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[j] = i + 1
            elif isinstance(field[i][j], int):
                tmp = field[i][j]
                field[i][j] = FREE
                field[ground[j]][j] = tmp
                ground[j] = ground[j] + 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("NORTH:")
        for x in field:
            _logger.debug(''.join([ROUND if isinstance(obj, int) else obj for obj in x]))
    ground = [0] * len(field)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[i] = j + 1
            elif isinstance(field[i][j], int):
                tmp = field[i][j]
                field[i][j] = FREE
                field[i][ground[i]] = tmp
                ground[i] = ground[i] + 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("WEST:")
        for x in field:
            _logger.debug(''.join([ROUND if isinstance(obj, int) else obj for obj in x]))
    ground = [len(field)] * len(field[0])
    for i in range(len(field) - 1, -1, -1):
        for j in range(len(field[i]) - 1, -1, -1):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[j] = i
            elif isinstance(field[i][j], int):
                tmp = field[i][j]
                field[i][j] = FREE
                field[ground[j] - 1][j] = tmp
                ground[j] = ground[j] - 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("SOUTH:")
        for x in field:
            _logger.debug(''.join([ROUND if isinstance(obj, int) else obj for obj in x]))
    ground = [len(field[0])] * len(field)
    for i in range(len(field) - 1, -1, -1):
        for j in range(len(field[i]) - 1, -1, -1):
            if field[i][j] == FREE:
                pass
            elif field[i][j] == FIXED:
                ground[i] = j
            elif isinstance(field[i][j], int):
                tmp = field[i][j]
                field[i][j] = FREE
                field[i][ground[i] - 1] = tmp
                ground[i] = ground[i] - 1
            else:
                raise Exception("Wrong input")
    if do_debug:
        _logger.debug("EAST:")
        for x in field:
            _logger.debug(''.join([ROUND if isinstance(obj, int) else obj for obj in x]))


def solve(f):
    field = []
    for line in f:
        line = line.strip()
        field.append([line[i] for i in range(len(line))])
    count = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == ROUND:
                field[i][j] = count
                count = count + 1
    pos = [collect_pos(field, count)]
    period = [0] * count
    periods = 0
    wait_done = 0
    done = 0
    while done < CYCLES:
        do_cycle(field, done == 0)
        done = done + 1
        pos.append(collect_pos(field, count))
        for j in range(count):
            if period[j] > 0:
                if pos[-1][j] != pos[-1 - period[j]][j]:
                    period[j] = 0
                    periods = periods - 1
                else:
                    continue
            for k in range(1, done):
                if pos[-1][j] == pos[-1 - k][j]:
                    period[j] = k
                    wait_done = max(wait_done, done + period[j])
                    periods = periods + 1
                    break
        if periods == count and done > wait_done:
            break
    _logger.info(period)
    answer = 0
    for i in range(count):
        rem = (CYCLES - done) % period[i]
        p = pos[-1 - period[i] + rem][i]
        answer = answer + len(field) - p[0]
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
