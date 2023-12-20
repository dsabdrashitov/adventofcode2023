import re

# NAME = "sample.in"
NAME = "input.txt"

START_PAT = re.compile(r'[0-9A-Z]*A')
FINISH_PAT = re.compile(r'[0-9A-Z]*Z')


def find_path(g, p, start: set, finish: set):
    curs = start
    curi = 0
    done = 0
    while not curs.issubset(finish):
        nexts = set()
        for s in curs:
            nexts.add(g[s][p[curi]])
        curs = nexts
        curi = (curi + 1) % len(p)
        done = done + 1
    return done


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
    main()
