from heapq import heappush, heappop
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

STREIGHT_LIMIT = 3
D_R = (0, +1)
D_D = (+1, 0)
D_L = (0, -1)
D_U = (-1, 0)
DIR = (D_R, D_D, D_L, D_U)
REDIRECT = {
    D_R: (D_U, D_D, ),
    D_D: (D_L, D_R, ),
    D_L: (D_U, D_D, ),
    D_U: (D_L, D_R, ),
}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def relax(d, s, p, old_dist, field, que, dist):
    if p[0] < 0 or p[0] >= len(field) or p[1] < 0 or p[1] >= len(field[0]):
        return
    nxt_d = old_dist + field[p[0]][p[1]]
    nxt = ((d, s), p)
    if nxt in dist and dist[nxt] <= nxt_d:
        return
    dist[nxt] = nxt_d
    heappush(que, (dist[nxt], nxt))


def solve(f):
    field = []
    for line in f:
        line = line.strip()
        field.append([int(c) for c in line])
    start = ((D_R, 0), (0, 0))
    dist = {start: 0}
    que = []
    heappush(que, (dist[start], start))
    while len(que) > 0:
        cur = heappop(que)
        curdist = cur[0]
        if curdist > dist[cur[1]]:
            continue
        curdir = cur[1][0]
        curp = cur[1][1]
        curd = curdir[0]
        curs = curdir[1]
        if curs < STREIGHT_LIMIT:
            relax(curd, curs + 1, add(curp, curd), curdist, field, que, dist)
        for nd in REDIRECT[curd]:
            relax(nd, 1, add(curp, nd), curdist, field, que, dist)
    answer = 9 * len(field) * 4 + 1
    for d in DIR:
        for s in range(1, STREIGHT_LIMIT + 1):
            finish = ((d, s), (len(field) - 1, len(field[0]) - 1))
            if finish in dist:
                answer = min(answer, dist[finish])
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
