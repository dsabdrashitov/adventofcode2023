import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"


def duplicate(g):
    result = {}
    for node, clist in g.items():
        result[node] = []
        for child in clist:
            result[child] = []
    for node, clist in g.items():
        for child in clist:
            result[node].append(child)
            result[child].append(node)
    return result


def find_dist(start, g, frbd):
    result = {start: (0, None)}
    que = [start]
    quer = 0
    while quer < len(que):
        node = que[quer]
        quer = quer + 1
        for child in g[node]:
            if (node, child) in frbd:
                continue
            if child not in result:
                result[child] = (result[node][0] + 1, node)
                que.append(child)
    return result


def find_furthest(dist):
    val = 0
    node = None
    for n, v in dist.items():
        if val < v[0]:
            val = v[0]
            node = n
    return node


def solve(f):
    line_pat = re.compile(r"([a-z]+): ([a-z ]*)")
    g = {}
    for line in f:
        line_match = line_pat.match(line)
        g[line_match.group(1)] = line_match.group(2).split()
    g = duplicate(g)
    n0 = next(iter(g))
    frbd = set()
    d0 = find_dist(n0, g, frbd)
    n1 = find_furthest(d0)

    ni = n1
    while d0[ni][1] is not None:
        frbd.add((d0[ni][1], ni))
        frbd.add((ni, d0[ni][1]))
        ni = d0[ni][1]
    d1 = find_dist(n0, g, frbd)

    ni = n1
    while d1[ni][1] is not None:
        frbd.add((d1[ni][1], ni))
        frbd.add((ni, d1[ni][1]))
        ni = d1[ni][1]
    d2 = find_dist(n0, g, frbd)

    ni = n1
    while d2[ni][1] is not None:
        frbd.add((d2[ni][1], ni))
        frbd.add((ni, d2[ni][1]))
        ni = d2[ni][1]
    d3 = find_dist(n0, g, frbd)

    _logger.info(len(d3))
    _logger.info(len(g) - len(d3))
    answer = len(d3) * (len(g) - len(d3))
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
