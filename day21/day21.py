# NAME = "sample.in"
NAME = "input.txt"

# STEPS = 6
STEPS = 64

START = 'S'
ROCK = '#'
PLOT = '.'

D = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def count(start, fence, steps):
    n = len(fence)
    m = len(fence[0])
    cur = set()
    cur.add(start)
    for step in range(steps):
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
    return len(cur)


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
    answer = count(start, fence, STEPS)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
