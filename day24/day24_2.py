import re
from scipy.optimize import fsolve
import logging

_logger = logging.getLogger(__name__)

NAME = "sample.in"
# NAME = "input.txt"


def hit_all(lines):
    i0 = 0
    i1 = 1
    i2 = 2
    i3 = 3
    x1 = lines[i0][0][0]
    y1 = lines[i0][0][1]
    z1 = lines[i0][0][2]
    x2 = lines[i1][0][0]
    y2 = lines[i1][0][1]
    z2 = lines[i1][0][2]
    x3 = lines[i2][0][0]
    y3 = lines[i2][0][1]
    z3 = lines[i2][0][2]
    x4 = lines[i3][0][0]
    y4 = lines[i3][0][1]
    z4 = lines[i3][0][2]
    u1 = lines[i0][1][0]
    v1 = lines[i0][1][1]
    w1 = lines[i0][1][2]
    u2 = lines[i1][1][0]
    v2 = lines[i1][1][1]
    w2 = lines[i1][1][2]
    u3 = lines[i2][1][0]
    v3 = lines[i2][1][1]
    w3 = lines[i2][1][2]
    u4 = lines[i3][1][0]
    v4 = lines[i3][1][1]
    w4 = lines[i3][1][2]

    def f(p):
        x0, y0, z0, u0, v0, w0 = p
        return (
            y1 * vx1 - y1 * vx0 + vy1 * x0 - vy1 * x1 - y0 * vx1 + y0 * vx0 - vy0 * x0 + vy0 * x1,
            y2 * vx2 - y2 * vx0 + vy2 * x0 - vy2 * x2 - y0 * vx2 + y0 * vx0 - vy0 * x0 + vy0 * x2,
            y3 * vx3 - y3 * vx0 + vy3 * x0 - vy3 * x3 - y0 * vx3 + y0 * vx0 - vy0 * x0 + vy0 * x3,
            z1 * vx1 - z1 * vx0 + vz1 * x0 - vz1 * x1 - z0 * vx1 + z0 * vx0 - vz0 * x0 + vz0 * x1,
            z2 * vx2 - z2 * vx0 + vz2 * x0 - vz2 * x2 - z0 * vx2 + z0 * vx0 - vz0 * x0 + vz0 * x2,
            z3 * vx3 - z3 * vx0 + vz3 * x0 - vz3 * x3 - z0 * vx3 + z0 * vx0 - vz0 * x0 + vz0 * x3,
        )

    x0, y0, z0, vx0, vy0, vz0 = 0, 0, 0, 0, 0, 0
    for i in range(100):
        x0, y0, z0, vx0, vy0, vz0 = fsolve(f, (x0, y0, z0, vx0, vy0, vz0))
    print(x0, y0, z0, "@", vx0, vy0, vz0)
    print(f((x0, y0, z0, vx0, vy0, vz0)))
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
