import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

FOREST = '#'
TRAIL = '.'

D = {
    '>': (0, +1),
    'v': (+1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def go(cur, prev, done, field, cross, cl):
    if field[cur[0]][cur[1]] == FOREST:
        return
    if (prev is not None) and cross[cur[0]][cur[1]]:
        cl.append((cur, done))
        return
    for d in D.values():
        p = add(cur, d)
        if p != prev:
            go(p, cur, done + 1, field, cross, cl)


def build_graph(n, m, field, start, end):
    cross = [[False] * m for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            if field[i][j] == FOREST:
                continue
            cnt = 0
            for d in D.values():
                p = add((i, j), d)
                if field[p[0]][p[1]] != FOREST:
                    cnt = cnt + 1
            if cnt > 2:
                cross[i][j] = True
    cross[start[0]][start[1]] = True
    cross[end[0]][end[1]] = True
    g = {}
    for i in range(1, n):
        for j in range(1, m):
            if cross[i][j]:
                cl = []
                g[(i, j)] = cl
                go((i, j), None, 0, field, cross, cl)
    return g


def rename_nodes(g, start, end):
    names = {}
    for k in g:
        names[k] = len(names)
    result = {}
    for node, clist in g.items():
        result[names[node]] = [(names[cp[0]], cp[1]) for cp in clist]
    return result, names[start], names[end]


def go_graph(cur, walked, g, used, finish, cache):
    if cur == finish:
        return walked
    if (used & (1 << cur)) != 0:
        return -1
    if ((cur, used) in cache) and (cache[(cur, used)] >= walked):
        return -1
    else:
        cache[(cur, used)] = walked
    used = used | (1 << cur)
    result = -1
    for cp in g[cur]:
        ret = go_graph(cp[0], walked + cp[1], g, used, finish, cache)
        if ret != -1:
            result = max(result, ret)
    return result


def find_longest(src, dst, g):
    return go_graph(src, 0, g, 0, dst, {})


def solve(f):
    field = []
    for line in f:
        field.append(FOREST + line.strip() + FOREST)
    m = len(field[0])
    field.append(FOREST * m)
    field.insert(0, FOREST * m)
    n = len(field)
    start = (1, field[1].index(TRAIL))
    end = (n - 2, field[n - 2].index(TRAIL))
    _logger.info(f"{start} -> {end}")
    g = build_graph(n, m, field, start, end)
    g, start, end = rename_nodes(g, start, end)
    answer = find_longest(start, end, g)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    main()
