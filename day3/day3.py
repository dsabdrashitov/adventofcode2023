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
    active = []
    for i in range(len(buf)):
        active.append([False] * len(buf[i]))
    for i in range(len(buf)):
        for j in range(len(buf[i])):
            if '0' <= buf[i][j] <= '9':
                continue
            if buf[i][j] == '.':
                continue
            for u in range(max(0, i - 1), min(i + 2, len(buf))):
                for v in range(max(0, j - 1), min(j + 2, len(buf[u]))):
                    active[u][v] = True
    p = re.compile(r"\d+")
    for i in range(len(buf)):
        for m in p.finditer(buf[i]):
            price = False
            for j in range(m.span()[0], m.span()[1]):
                if active[i][j]:
                    price = True
                    break
            if price:
                answer = answer + int(m.group())

    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
