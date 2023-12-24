import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

# TEST_AREA = ((7, 7), (27, 27))
TEST_AREA = ((200000000000000, 200000000000000), (400000000000000, 400000000000000))


def intersect_box(line):
    raise Exception("Don't like it")
    return True


def intersect(line1, line2):
    x1 = line1[0][0]
    y1 = line1[0][1]
    vx1 = line1[1][0]
    vy1 = line1[1][1]
    x2 = line2[0][0]
    y2 = line2[0][1]
    vx2 = line2[1][0]
    vy2 = line2[1][1]
    d = - vx1 * vy2 + vx2 * vy1
    if d == 0:
        if (vx1 * (y2 - y1) - vy1 * (x2 - x1)) == 0:
            _logger.info(f"Lines coincide")
            return intersect_box(line1)
        else:
            _logger.info(f"Lines parallel")
            return False
    d1 = -(x2 - x1) * vy2 + (y2 - y1) * vx2
    d2 = vx1 * (y2 - y1) - vy1 * (x2 - x1)
    t1 = d1 / d
    t2 = d2 / d
    if t1 < 0:
        _logger.info(f"Intersection 1 is in the past")
        return False
    if t2 < 0:
        _logger.info(f"Intersection 2 is in the past")
        return False
    x = x1 + vx1 * t1
    y = y1 + vy1 * t1
    return TEST_AREA[0][0] <= x <= TEST_AREA[1][0] and TEST_AREA[0][1] <= y <= TEST_AREA[1][1]


def find_intersections(lines):
    answer = 0
    for i in range(len(lines)):
        for j in range(i):
            if intersect(lines[i], lines[j]):
                answer = answer + 1
    return answer


def solve(f):
    line_pat = re.compile(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)")
    lines = []
    for line in f:
        line_match = line_pat.match(line)
        x = int(line_match.group(1))
        y = int(line_match.group(2))
        z = int(line_match.group(3))
        vx = int(line_match.group(4))
        vy = int(line_match.group(5))
        vz = int(line_match.group(6))
        lines.append(((x, y, z), (vx, vy, vz)))
    answer = find_intersections(lines)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
