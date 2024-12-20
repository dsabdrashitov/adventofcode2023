import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

# STEPS = 7
STEPS = 26501365

START = 'S'
ROCK = '#'
PLOT = '.'

D = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def inside(cur, n, m):
    result = 0
    for p in cur:
        if p[0] < n - 1 and p[1] < m - 1:
            result = result + 1
        # result = result + 1
    return result


def do_precalc(fence):
    n = len(fence)
    m = len(fence[0])
    fence_copy = []
    for i in range(n):
        fence_copy.append(fence[i] + [False])
    fence_copy.append([False] * (m + 1))
    fence = fence_copy
    n = len(fence)
    m = len(fence[0])
    result = []
    log = []
    cur = set()
    cur.add((0, 0))
    while len(log) < 4 or log[-1] != log[-3] or log[-2] != log[-4]:
        result.append(inside(cur, n, m))
        log.append(len(cur))
        nxt = set()
        for p0 in cur:
            for d in D:
                p1 = add(p0, d)
                if p1[0] < 0 or p1[0] >= n or p1[1] < 0 or p1[1] >= m:
                    continue
                if fence[p1[0]][p1[1]]:
                    continue
                nxt.add(p1)
        cur = nxt
    return result[:-2]


def count(fence, steps):
    _logger.debug(fence)
    precalc = do_precalc(fence)
    _logger.debug(f"precalc = {precalc}")
    full = [0] * 2
    full[(len(precalc) - 1) % 2] = precalc[-1]
    full[(len(precalc) - 2) % 2] = precalc[-2]
    _logger.debug(f"full={full}")
    answer = 0
    n = len(fence)
    m = len(fence[0])
    for i in range((steps // n) + 1):
        j = (steps - i * n) // m
        while j >= 0:
            remsteps = steps - i * n - j * m
            _logger.debug(f"{i}, {j}: remsteps = {remsteps}")
            if remsteps >= len(precalc):
                answer = answer + ((j + 1 + 1) // 2) * full[remsteps % 2]
                answer = answer + ((j + 1) // 2) * full[(remsteps + 1) % 2]
                _logger.debug(f"skipped to {answer}")
                break
            answer = answer + precalc[remsteps]
            _logger.debug(f"increase to {answer}")
            j = j - 1
    _logger.debug(f"answer = {answer}")
    return answer


def remap(fence, start, d1, d2):
    n = len(fence)
    m = len(fence[0])
    result = []
    for i in range(n):
        u = (start[0] + d1 * i) % n
        resultline = [False] * m
        for j in range(m):
            v = (start[1] + d2 * j) % m
            resultline[j] = fence[u][v]
        result.append(resultline)
    return result


def solve(f):
    inp = []
    for line in f:
        inp.append(line.strip())

    n = len(inp)
    m = len(inp[0])
    fence = []
    start = ()
    for i in range(n):
        fenceline = []
        for j in range(m):
            if inp[i][j] == ROCK:
                fenceline.append(True)
            else:
                fenceline.append(False)
                if inp[i][j] == START:
                    start = (i, j)
                elif inp[i][j] == PLOT:
                    pass
                else:
                    raise Exception("Botva!")
        fence.append(fenceline)
    for i in range(n):
        if fence[i][start[1]]:
            raise Exception("Too hard :)")
    for i in range(m):
        if fence[start[0]][i]:
            raise Exception("Too hard :)")
    if (n % 2) != 1 or (m % 2) != 1:
        raise Exception("I'm not ready.")
    answer = 0
    for d1 in range(-1, 2, 2):
        for d2 in range(-1, 2, 2):
            answer = answer + count(remap(fence, start, d1, d2), STEPS)
    answer = answer - 4 * (1 + (STEPS // 2))
    if (STEPS % 2) == 0:
        answer = answer + 1
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
