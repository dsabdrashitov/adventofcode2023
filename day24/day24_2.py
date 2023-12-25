import re
from scipy.optimize import fsolve
from scipy import linalg
import numpy as np
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"


def mydiv(a, b):
    a = int(a)
    b = int(b)
    if a * b < 0:
        sign = -1
    else:
        sign = 1
    a = abs(a)
    b = abs(b)
    left = 0
    right = a + 1
    while left + 1 < right:
        mid = (left + right) // 2
        if b * mid < a:
            left = mid
        else:
            right = mid
    return sign * right


def solve_eq(a, c):
    a = [[int(a[i][j]) for j in range(len(a[i]))] for i in range(len(a))]
    c = [int(c[i]) for i in range(len(c))]
    for i in range(len(c)):
        nonzero = -1
        for j in range(i, len(c)):
            if a[j][i] != 0:
                nonzero = j
                break
        tmp = list(a[i])
        a[i] = a[nonzero]
        a[nonzero] = tmp
        tmp = c[i]
        c[i] = c[nonzero]
        c[nonzero] = tmp
        for j in range(i + 1, len(c)):
            aii = a[i][i]
            aji = a[j][i]
            for k in range(len(a[i])):
                a[j][k] = a[j][k] * aii - a[i][k] * aji
            c[j] = c[j] * aii - c[i] * aji
    x = [0] * len(a[0])
    for i in range(len(c) - 1, -1, -1):
        cc = c[i]
        for j in range(i + 1, len(a[i])):
            cc = cc - a[i][j] * x[j]
        x[i] = mydiv(cc, a[i][i])
    return x


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

    # def f(p):
    #     x0, y0, z0, u0, v0, w0 = p
    #     return (
    #         x0 * (v1 - v4) + y0 * (u4 - u1) + u0 * (y4 - y1) + v0 * (x1 - x4) + y1 * u1 - v1 * x1 - y4 * u4 + v4 * x4,
    #         x0 * (v2 - v4) + y0 * (u4 - u2) + u0 * (y4 - y2) + v0 * (x2 - x4) + y2 * u2 - v2 * x2 - y4 * u4 + v4 * x4,
    #         x0 * (v3 - v4) + y0 * (u4 - u3) + u0 * (y4 - y3) + v0 * (x3 - x4) + y3 * u3 - v3 * x3 - y4 * u4 + v4 * x4,
    #         x0 * (w1 - w4) + z0 * (u4 - u1) + u0 * (z4 - z1) + w0 * (x1 - x4) + z1 * u1 - w1 * x1 - z4 * u4 + w4 * x4,
    #         x0 * (w2 - w4) + z0 * (u4 - u2) + u0 * (z4 - z2) + w0 * (x2 - x4) + z2 * u2 - w2 * x2 - z4 * u4 + w4 * x4,
    #         x0 * (w3 - w4) + z0 * (u4 - u3) + u0 * (z4 - z3) + w0 * (x3 - x4) + z3 * u3 - w3 * x3 - z4 * u4 + w4 * x4,
    #     )

    a = [
        [(v1 - v4), (u4 - u1), 0, (y4 - y1), (x1 - x4), 0, ],
        [(v2 - v4), (u4 - u2), 0, (y4 - y2), (x2 - x4), 0, ],
        [(v3 - v4), (u4 - u3), 0, (y4 - y3), (x3 - x4), 0, ],
        [(w1 - w4), 0, (u4 - u1), (z4 - z1), 0, (x1 - x4), ],
        [(w2 - w4), 0, (u4 - u2), (z4 - z2), 0, (x2 - x4), ],
        [(w3 - w4), 0, (u4 - u3), (z4 - z3), 0, (x3 - x4), ],
    ]
    c = [
        y1 * u1 - v1 * x1 - y4 * u4 + v4 * x4,
        y2 * u2 - v2 * x2 - y4 * u4 + v4 * x4,
        y3 * u3 - v3 * x3 - y4 * u4 + v4 * x4,
        z1 * u1 - w1 * x1 - z4 * u4 + w4 * x4,
        z2 * u2 - w2 * x2 - z4 * u4 + w4 * x4,
        z3 * u3 - w3 * x3 - z4 * u4 + w4 * x4,
    ]
    a = np.array(a)
    c = -np.array(c)
    x = solve_eq(a, c)
    # x = linalg.solve(a, c)
    print(x)

    # x0, y0, z0, u0, v0, w0 = 0, 0, 0, 0, 0, 0
    # for i in range(100):
    #     x0, y0, z0, u0, v0, w0 = fsolve(f, (x0, y0, z0, u0, v0, w0))
    # print(x0, y0, z0, "@", u0, v0, w0)
    # print(f((x0, y0, z0, u0, v0, w0)))
    answer = (x[0], x[1], x[2]), (x[3], x[4], x[5])
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
