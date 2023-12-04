import re

# NAME = "sample.in"
NAME = "input.txt"

RED = "red"
GREEN = "green"
BLUE = "blue"
DEF = {RED: 0, GREEN: 0, BLUE: 0}


def max_set(s1: dict, s2: dict) -> dict:
    result = {}
    for k, v in s1.items():
        if k not in result or v > result[k]:
            result[k] = v
    for k, v in s2.items():
        if k not in result or v > result[k]:
            result[k] = v
    return result


def solve(f):
    pat1 = re.compile(r"Game (\d+):(.*)$")
    pat2 = re.compile(r"[^;]+")
    pat3 = re.compile(r"[^,]+")
    pat4 = re.compile(r"\s*(\d+)\s+(.*)")
    num_sum = 0
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        match1 = pat1.match(line)
        # game_id = int(match1.group(1))
        needed = DEF
        sets_matches = pat2.findall(match1.group(2))
        for sm in sets_matches:
            balls_matches = pat3.findall(sm)
            ball_set = {}
            for bm in balls_matches:
                ball = pat4.match(bm)
                g = ball.groups()
                if g[1] in ball_set:
                    ball_set[g[1]] = ball_set[g[1]] + int(g[0])
                else:
                    ball_set[g[1]] = int(g[0])
            needed = max_set(needed, ball_set)
        num_sum = num_sum + needed[RED] * needed[GREEN] * needed[BLUE]
    return num_sum


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
