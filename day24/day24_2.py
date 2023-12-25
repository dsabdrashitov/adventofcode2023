import re
from scipy.optimize import fsolve
import logging

_logger = logging.getLogger(__name__)

NAME = "sample.in"
# NAME = "input.txt"


def hit_all(lines):
    n = len(lines)
    i0 = 2
    i1 = 39
    i2 = 63
    x1 = lines[i0][0][0]
    y1 = lines[i0][0][1]
    z1 = lines[i0][0][2]
    x2 = lines[i1][0][0]
    y2 = lines[i1][0][1]
    z2 = lines[i1][0][2]
    x3 = lines[i2][0][0]
    y3 = lines[i2][0][1]
    z3 = lines[i2][0][2]
    vx1 = lines[i0][1][0]
    vy1 = lines[i0][1][1]
    vz1 = lines[i0][1][2]
    vx2 = lines[i1][1][0]
    vy2 = lines[i1][1][1]
    vz2 = lines[i1][1][2]
    vx3 = lines[i2][1][0]
    vy3 = lines[i2][1][1]
    vz3 = lines[i2][1][2]

    def f(p):
        x0, y0, z0, vx0, vy0, vz0, t1, t2, t3 = p
        return (
                x1 + vx1 * t1 - x0 - vx0 * t1,
                y1 + vy1 * t1 - y0 - vy0 * t1,
                z1 + vz1 * t1 - z0 - vz0 * t1,
                x2 + vx2 * t2 - x0 - vx0 * t2,
                y2 + vy2 * t2 - y0 - vy0 * t2,
                z2 + vz2 * t2 - z0 - vz0 * t2,
                x3 + vx3 * t3 - x0 - vx0 * t3,
                y3 + vy3 * t3 - y0 - vy0 * t3,
                z3 + vz3 * t3 - z0 - vz0 * t3
        )

    x0, y0, z0, vx0, vy0, vz0, t1, t2, t3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(100):
        x0, y0, z0, vx0, vy0, vz0, t1, t2, t3 = fsolve(f, (x0, y0, z0, vx0, vy0, vz0, t1, t2, t3))
    print(x0, y0, z0)
    answer = (x0, y0, z0), (vx0, vy0, vz0)
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
    answer = hit_all(lines)
    return answer[0][0] + answer[0][1] + answer[0][2]


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
