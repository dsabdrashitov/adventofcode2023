import re

# NAME = "sample.in"
NAME = "input.txt"

START = 'AAA'
FINISH = 'ZZZ'


def find_path(g, p):
    curs = START
    curi = 0
    done = 0
    while curs != FINISH:
        curs = g[curs][p[curi]]
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
    node_pat = re.compile(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)")
    g = {}
    for line in f:
        match = node_pat.match(line)
        g[match.group(1)] = [match.group(2), match.group(3)]
    answer = find_path(g, program)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
