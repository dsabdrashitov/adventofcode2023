import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"


def normal(block):
    a1 = block[0]
    a2 = block[1]
    b1 = (min(a1[0], a2[0]), min(a1[1], a2[1]), min(a1[2], a2[2]))
    b2 = (max(a1[0], a2[0]), max(a1[1], a2[1]), max(a1[2], a2[2]))
    return b1, b2, block[2]


def inters_plane(block1, block2):
    a1 = block1[0]
    a2 = block1[1]
    b1 = block2[0]
    b2 = block2[1]
    if b2[0] < a1[0] or b1[0] > a2[0]:
        return False
    if b2[1] < a1[1] or b1[1] > a2[1]:
        return False
    return True


def solve(f):
    block_pat = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
    blocks = []
    for line in f:
        match = block_pat.match(line)
        p1 = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        p2 = (int(match.group(4)), int(match.group(5)), int(match.group(6)))
        blocks.append(normal((p1, p2, len(blocks))))
    blocks.sort(key=lambda block: block[0][2])
    supports = {}
    for i in range(len(blocks)):
        list_of_inters = []
        for j in range(i):
            if inters_plane(blocks[i], blocks[j]):
                list_of_inters.append(blocks[j])
        base = 0
        for b in list_of_inters:
            base = max(base, b[1][2])
        blocks[i] = ((blocks[i][0][0], blocks[i][0][1], base + 1),
                     (blocks[i][1][0], blocks[i][1][1], base + 1 + blocks[i][1][2] - blocks[i][0][2]),
                     blocks[i][2])
        suplist = []
        for b in list_of_inters:
            if b[1][2] == base:
                suplist.append(b[2])
        supports[blocks[i][2]] = suplist
    only_support = set()
    for name, suplist in supports.items():
        if len(suplist) == 1:
            only_support.add(suplist[0])
    answer = len(blocks) - len(only_support)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
