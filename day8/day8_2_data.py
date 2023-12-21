import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

START_PAT = re.compile(r'[0-9A-Z]*A')
FINISH_PAT = re.compile(r'[0-9A-Z]*Z')


def go_precycle(node, done, g, p, finish):
    while node not in finish:
        node = g[node][p[done % len(p)]]
        done = done + 1
    return node, done


def remove_precycle(g, p, start, finish):
    started = set()
    for node in start:
        nxt = go_precycle(node, 0, g, p, finish)
        _logger.info(f"{node} -> {nxt}")
        started.add(nxt)
    return started


def find_next(node, done, min_dist, g, p, finish, graph_cache):
    if (node, done % len(p)) not in graph_cache:
        graph_cache[(node, done % len(p))] = [(node, 0)]
    gc: list = graph_cache[(node, done % len(p))]
    if gc[-1][1] < min_dist:
        u = gc[-1][0]
        d = gc[-1][1]
        while True:
            u = g[u][p[(done + d) % len(p)]]
            d = d + 1
            if u in finish:
                gc.append((u, d))
                if d >= min_dist:
                    break
    left = -1
    right = len(gc) - 1
    while left + 1 < right:
        mid = (left + right) // 2
        if gc[mid][1] < min_dist:
            left = mid
        else:
            right = mid
    return gc[right]


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


def find_path(g, p, start: set, finish: set):
    graph_cache = {}
    current: set = remove_precycle(g, p, start, finish)
    values = []
    for node, done in current:
        nxt, dist = find_next(node, done, 1, g, p, finish, graph_cache)
        assert nxt == node
        assert done == dist
        _logger.info(f"({node}, {done}) = {dist}")
        values.append(dist)
    return lcm(values)


def solve(f):
    program_str = f.readline().strip()
    program = [0] * len(program_str)
    for i in range(len(program)):
        if program_str[i] == 'L':
            program[i] = 0
        elif program_str[i] == 'R':
            program[i] = 1
        else:
            raise Exception("Botva!")
    f.readline()
    node_pat = re.compile(r"([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)")
    g = {}
    start = set()
    finish = set()
    for line in f:
        match = node_pat.match(line)
        node = match.group(1)
        left = match.group(2)
        right = match.group(3)
        g[node] = [left, right]
        if START_PAT.match(node):
            start.add(node)
        if FINISH_PAT.match(node):
            finish.add(node)
    answer = find_path(g, program, start, finish)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    main()
