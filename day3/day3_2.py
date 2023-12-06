import re

# NAME = "sample.in"
NAME = "input.txt"


def solve(f):
    answer = 0
    buf = []
    while True:
        line = f.readline().strip()
        if len(line) == 0:
            break
        buf.append(line)
    pns = []
    for i in range(len(buf)):
        pns_line = []
        for j in range(len(buf[i])):
            pns_line.append([])
        pns.append(pns_line)
    p = re.compile(r"\d+")
    for i in range(len(buf)):
        for m in p.finditer(buf[i]):
            pn = int(m.group())
            for y in range(max(0, i - 1), min(len(buf), i + 2)):
                for j in range(max(0, m.span()[0] - 1), min(len(buf[y]), m.span()[1] + 1)):
                    pns[y][j].append(pn)
    for i in range(len(buf)):
        for j in range(len(buf[i])):
            if buf[i][j] != '*':
                continue
            if len(pns[i][j]) != 2:
                continue
            answer = answer + pns[i][j][0] * pns[i][j][1]
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
