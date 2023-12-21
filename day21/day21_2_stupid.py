NAME = "sample.in"
# NAME = "input.txt"

STEPS = 5
# STEPS = 26501365

START = 'S'
ROCK = '#'
PLOT = '.'

D = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def do_precalc(fence):
    n = len(fence)
    m = len(fence[0])
    result = []
    cur = set()
    cur.add((0, 0))
    while len(result) < 3 or result[-1] != result[-3]:
        result.append(len(cur))
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
    return result[:-1]


def count(fence, steps):
    # print(fence)
    precalc = do_precalc(fence)
    # print(f"precalc = {precalc}")
    full = [0] * 2
    full[(len(precalc) - 1) % 2] = precalc[-1]
    full[(len(precalc) - 2) % 2] = precalc[-2]
    answer = 0
    n = len(fence)
    m = len(fence[0])
    for i in range((steps // n) + 1):
        j = (steps - i * n) // m
        while j >= 0:
            # print(i, j)
            remsteps = steps - i * n - j * m
            if remsteps >= len(precalc):
                answer = answer + ((j + 1 + 1) // 2) * full[0]
                answer = answer + ((j + 1) // 2) * full[1]
                break
            answer = answer + precalc[remsteps]
            j = j - 1
    # print(answer)
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
        inp.append(line.strip() * 5)
    inpcopy = list(inp)
    for i in range(4):
        inp.extend(inpcopy)
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
    main()
