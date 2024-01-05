import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

D_R = (0, +1)
D_D = (+1, 0)
D_L = (0, -1)
D_U = (-1, 0)
DIR = {
    'R': D_R,
    'D': D_D,
    'L': D_L,
    'U': D_U,
}
DIRS = (D_R, D_D, D_L, D_U)
COM_PAT = re.compile(r"([RDUL]) (\d+) \(#([0-9a-f]+)\)")


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def solve(f):
    commands = []
    for line in f:
        match = COM_PAT.match(line.strip())
        commands.append((match.group(1), int(match.group(2)), match.group(3)))
    pos = (0, 0)
    color = {pos: 'start'}
    ul = pos
    dr = pos
    for command in commands:
        for i in range(1, command[1] + 1):
            pos = add(pos, DIR[command[0]])
            color[pos] = command[2]
            ul = (min(ul[0], pos[0]), min(ul[1], pos[1]))
            dr = (max(dr[0], pos[0]), max(dr[1], pos[1]))
    for i in range(ul[0] - 2, dr[0] + 2 + 1):
        color[(i, ul[1] - 2)] = None
        color[(i, dr[1] + 2)] = None
    for i in range(ul[1] - 2, dr[1] + 2 + 1):
        color[(ul[0] - 2), i] = None
        color[(dr[0] + 2), i] = None
    que = [(ul[0] - 1, ul[1] - 1)]
    quer = 0
    while quer < len(que):
        cur = que[quer]
        quer = quer + 1
        for d in DIRS:
            nxt = add(cur, d)
            if nxt not in color:
                color[nxt] = None
                que.append(nxt)
    answer = 0
    for i in range(ul[0], dr[0] + 1):
        for j in range(ul[1], dr[1] + 1):
            if (i, j) not in color or color[(i, j)] is not None:
                answer = answer + 1
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
