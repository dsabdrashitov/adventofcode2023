import heapq
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
    line_pat = re.compile(f"Card\s* (\d+): ([\s\d]*)\|([\d\s]*)")
    count = [0] * len(buf)
    current = 0
    for i in range(len(buf)):
        line = buf[i]
        match = line_pat.match(line)
        our = match.groups()[1].split()
        winning = set(match.groups()[2].split())
        cnt = 0
        for our_card in our:
            if our_card in winning:
                cnt = cnt + 1
        answer = answer + 1 + current
        count[i + cnt] = count[i + cnt] + 1 + current
        current = current + current + 1 - count[i]
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
