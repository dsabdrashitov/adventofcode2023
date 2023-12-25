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
            x0 * (v1 - v4) + y0 * (u4 - u1) + u0 * (y4 - y1) + v0 * (x1 - x4) + y1 * u1 - v1 * x1 - y4 * u4 + v4 * x4,
            x0 * (v2 - v4) + y0 * (u4 - u2) + u0 * (y4 - y2) + v0 * (x2 - x4) + y2 * u2 - v2 * x2 - y4 * u4 + v4 * x4,
            x0 * (v3 - v4) + y0 * (u4 - u3) + u0 * (y4 - y3) + v0 * (x3 - x4) + y3 * u3 - v3 * x3 - y4 * u4 + v4 * x4,
            x0 * (w1 - w4) + z0 * (u4 - u1) + u0 * (z4 - z1) + w0 * (x1 - x4) + z1 * u1 - w1 * x1 - z4 * u4 + w4 * x4,
            x0 * (w2 - w4) + z0 * (u4 - u2) + u0 * (z4 - z2) + w0 * (x2 - x4) + z2 * u2 - w2 * x2 - z4 * u4 + w4 * x4,
            x0 * (w3 - w4) + z0 * (u4 - u3) + u0 * (z4 - z3) + w0 * (x3 - x4) + z3 * u3 - w3 * x3 - z4 * u4 + w4 * x4,
        )

    x0, y0, z0, u0, v0, w0 = 0, 0, 0, 0, 0, 0
    for i in range(100):
        x0, y0, z0, u0, v0, w0 = fsolve(f, (x0, y0, z0, u0, v0, w0))
    print(x0, y0, z0, "@", u0, v0, w0)
    print(f((x0, y0, z0, u0, v0, w0)))
    answer = (x0, y0, z0), (u0, v0, w0)
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
