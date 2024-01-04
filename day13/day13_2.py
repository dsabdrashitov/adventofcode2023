import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

MULT = 100
ROCKS = '#'
ASH = '.'
LINE_PAT = re.compile(r"[#.]+")


def vertical(note):
    rotated = []
    for i in range(len(note[0])):
        line = [note[j][i] for j in range(len(note))]
        rotated.append(''.join(line))
    return horizontal(rotated)


def near(n1, n2):
    cnt = 0
    for i in range(len(n1)):
        if n1[i] != n2[i]:
            cnt = cnt + 1
            if cnt > 1:
                return False
    return True


def horizontal(note):
    h = [hash(note[i]) for i in range(len(note))]
    for i in range(1, len(note)):
        bad = 0
        for j in range(min(i, len(note) - i)):
            if h[i - 1 - j] != h[i + j]:
                if near(note[i - 1 - j], note[i + j]):
                    bad = bad + 1
                else:
                    bad = 2
                if bad > 1:
                    break
        if bad > 1:
            continue
        bad = 0
        for j in range(min(i, len(note) - i)):
            if note[i - 1 - j] != note[i + j]:
                if near(note[i - 1 - j], note[i + j]):
                    bad = bad + 1
                else:
                    bad = 2
                if bad > 1:
                    break
        if bad == 1:
            return i
    return 0


def solve(f):
    notes = []
    current_note = []
    for line in f:
        match = LINE_PAT.match(line)
        if match:
            current_note.append(line.strip())
        else:
            notes.append(current_note)
            current_note = []
    notes.append(current_note)
    answer = 0
    for note in notes:
        _logger.debug(answer)
        answer = answer + vertical(note)
        _logger.debug(f"-> {answer}")
        answer = answer + MULT * horizontal(note)
        _logger.debug(f"-> {answer}")
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
