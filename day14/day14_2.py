import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

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


def gcd(a, b):
    while a > 0:
        tmp = b % a
        b = a
        a = tmp
    return b


def lcm(a):
    result = a[0]
    for x in a:
        result = result * x // gcd(result, x)
    return result


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
    period = None
    done = 0
    while done < CYCLES:
        two_power = 2 ** (len(pos) - 1)
        for i in range(min(two_power, CYCLES - done)):
            do_cycle(field, done == 0)
            done = done + 1
            cur_pos = collect_pos(field, count)
            good = True
            for j in range(count):
                if pos[-1][j] != cur_pos[j]:
                    good = False
                    break
            if good:
                period = i + 1
                break
        if period is not None:
            break
        pos.append(collect_pos(field, count))
    _logger.info(period)
    done = done + ((CYCLES - done) // period) * period
    while done < CYCLES:
        do_cycle(field)
        done = done + 1
    answer = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if isinstance(field[i][j], int):
                answer = answer + len(field) - i
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
