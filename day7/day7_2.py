import re

# NAME = "sample.in"
NAME = "input.txt"


def decode(c):
    if '2' <= c <= '9':
        return int(c) - 2
    if c == 'T':
        return 8
    if c == 'J':
        return -1
    if c == 'Q':
        return 10
    if c == 'K':
        return 11
    if c == 'A':
        return 12
    raise Exception("Botva!")


def add_rank(bet):
    h = bet[0]
    jcnt = 0
    others = []
    for c in h:
        if c == -1:
            jcnt = jcnt + 1
        else:
            others.append(c)
    cnts = []
    i = 0
    others.sort()
    while i < len(others):
        j = i
        while j < len(others) and others[j] == others[i]:
            j = j + 1
        cnts.append(j - i)
        i = j
    cnts.sort(reverse=True)
    if len(cnts) == 0:
        cnts.append(jcnt)
    else:
        cnts[0] = cnts[0] + jcnt
    # nothing
    rank = 0
    # pair
    if cnts[0] >= 2:
        rank = 1
    # two pairs
    if cnts[0] >= 2 and len(cnts) >= 2 and cnts[1] >= 2:
        rank = 2
    # three
    if cnts[0] >= 3:
        rank = 3
    # fh
    if cnts[0] >= 3 and len(cnts) >= 2 and cnts[1] >= 2:
        rank = 4
    # four
    if cnts[0] >= 4:
        rank = 5
    # five
    if cnts[0] >= 5:
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
