import re

# NAME = "sample.in"
NAME = "input.txt"

RED = "red"
GREEN = "green"
BLUE = "blue"
LIMIT = {RED: 12, GREEN: 13, BLUE: 14}


def all_le(s1: dict, s2: dict) -> bool:
    for k, v in s1.items():
        if v > s2[k]:
            return False
    return True


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
        game_id = int(match1.group(1))
        gg = True
        sets_matches = pat2.findall(match1.group(2))
        for sm in sets_matches:
            balls_matches = pat3.findall(sm)
            ball_set = {"red": 0, "green": 0, "blue": 0}
            for bm in balls_matches:
                ball = pat4.match(bm)
                g = ball.groups()
                if g[1] in ball_set:
                    ball_set[g[1]] = ball_set[g[1]] + int(g[0])
            if not all_le(ball_set, LIMIT):
                gg = False
        if gg:
            num_sum = num_sum + game_id
    return num_sum


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
