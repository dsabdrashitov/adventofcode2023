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
        started.add(go_precycle(node, 0, g, p, finish))
    return started


def find_next(node, done, min_dist, g, p, finish, graph_cache):
    mdp = 1
    while 2 * mdp <= min_dist:
        mdp = 2 * mdp
    if (node, done % len(p), mdp) in graph_cache:
        return graph_cache[(node, done % len(p), mdp)]
    node0 = node
    dist = 0
    prev_node = None
    prev_dist = None
    while True:
        node = g[node][p[(done + dist) % len(p)]]
        dist = dist + 1
        if node in finish:
            if prev_node is None:
                prev_node = node
                prev_dist = dist
            if dist > mdp:
                break
            prev_node = node
            prev_dist = dist
    graph_cache[(node0, done % len(p), mdp)] = prev_node, prev_dist
    return prev_node, prev_dist


def find_path(g, p, start: set, finish: set):
    graph_cache = {}
    current: set = remove_precycle(g, p, start, finish)
    while True:
        # _logger.debug(current)
        min_done = None
        max_done = None
        for node, done in current:
            if min_done is None or min_done >= done:
                min_done = done
            if max_done is None or max_done <= done:
                max_done = done
        if min_done == max_done:
            return min_done
        logging.debug(f"{min_done}, {max_done}")
        to_update = []
        for node, done in current:
            if done == min_done:
                to_update.append((node, done))
        for node, done in to_update:
            current.remove((node, done))
            nxt, dist = find_next(node, done, max_done - done, g, p, finish, graph_cache)
            current.add((nxt, done + dist))


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
