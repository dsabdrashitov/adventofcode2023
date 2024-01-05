import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

EMPTY = '.'
HORIZONTAL = '-'
VERTICAL = '|'
RIGHT = '/'
LEFT = '\\'
D_R = (0, +1)
D_D = (+1, 0)
D_L = (0, -1)
D_U = (-1, 0)
DIR = (D_R, D_D, D_L, D_U)
REDIRECT = {
    (D_R, EMPTY): (D_R, ),
    (D_D, EMPTY): (D_D, ),
    (D_L, EMPTY): (D_L, ),
    (D_U, EMPTY): (D_U, ),
    (D_R, HORIZONTAL): (D_R, ),
    (D_D, HORIZONTAL): (D_R, D_L, ),
    (D_L, HORIZONTAL): (D_L, ),
    (D_U, HORIZONTAL): (D_R, D_L, ),
    (D_R, VERTICAL): (D_U, D_D, ),
    (D_D, VERTICAL): (D_D, ),
    (D_L, VERTICAL): (D_U, D_D, ),
    (D_U, VERTICAL): (D_U, ),
    (D_R, RIGHT): (D_U, ),
    (D_D, RIGHT): (D_L, ),
    (D_L, RIGHT): (D_D, ),
    (D_U, RIGHT): (D_R, ),
    (D_R, LEFT): (D_D, ),
    (D_D, LEFT): (D_R, ),
    (D_L, LEFT): (D_U, ),
    (D_U, LEFT): (D_L, ),
}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def solve(f):
    field = []
    for line in f:
        line = line.strip()
        field.append(line)
    start = (D_R, (0, 0))
    used = {start}
    que = [start]
    quer = 0
    while quer < len(que):
        cur = que[quer]
        quer = quer + 1
        curd, curp = cur
        for d in REDIRECT[(curd, field[curp[0]][curp[1]])]:
            nxt = (d, add(curp, d))
            nxtp = nxt[1]
            if nxtp[0] < 0 or nxtp[0] >= len(field) or nxtp[1] < 0 or nxtp[1] >= len(field[0]):
                continue
            if nxt not in used:
                used.add(nxt)
                que.append(nxt)
    heat = set()
    for pos in que:
        heat.add(pos[1])
    answer = len(heat)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
