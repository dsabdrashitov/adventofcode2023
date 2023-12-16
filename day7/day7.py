import re

# NAME = "sample.in"
NAME = "input.txt"


def decode(c):
    if '2' <= c <= '9':
        return int(c) - 2
    if c == 'T':
        return 8
    if c == 'J':
        return 9
    if c == 'Q':
        return 10
    if c == 'K':
        return 11
    if c == 'A':
        return 12
    raise Exception("Botva!")


def add_rank(bet):
    h = bet[0]
    # nothing
    rank = 0
    # pair
    s = sorted(h)
    for i in range(4):
        if s[i] == s[i + 1]:
            rank = 1
            break
    # two pair
    if (s[0] == s[1] and s[2] == s[3]) or (s[0] == s[1] and s[3] == s[4]) or (s[1] == s[2] and s[3] == s[4]):
        rank = 2
    # three
    if (s[0] == s[1] == s[2]) or (s[1] == s[2] == s[3]) or (s[2] == s[3] == s[4]):
        rank = 3
    # fh
    if (s[0] == s[1] == s[2] and s[3] == s[4]) or (s[0] == s[1] and s[2] == s[3] == s[4]):
        rank = 4
    # four
    if (s[0] == s[1] == s[2] == s[3]) or (s[1] == s[2] == s[3] == s[4]):
        rank = 5
    if s[0] == s[1] == s[2] == s[3] == s[4]:
        rank = 6
    result = [rank]
    result.extend(h)
    return result


def solve(f):
    cards = []
    for s in f:
        line = s.split()
        cards.append(([decode(c) for c in line[0]], int(line[1])))
    cards.sort(key=add_rank)
    print(cards)
    answer = 0
    for i in range(len(cards)):
        answer = answer + (i + 1) * cards[i][1]
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
