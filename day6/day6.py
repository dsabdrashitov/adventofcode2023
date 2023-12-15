import re

# NAME = "sample.in"
NAME = "input.txt"


def solve(f):
    times = [int(s) for s in re.compile(r"\d+").findall(f.readline())]
    dists = [int(s) for s in re.compile(r"\d+").findall(f.readline())]
    print(times)
    print(dists)
    answer = 1
    for i in range(len(times)):
        t = times[i]
        d = dists[i]
        left = t // 2
        right = t
        while left + 1 < right:
            mid = (left + right) // 2
            f = mid * (t - mid)
            if f > d:
                left = mid
            else:
                right = mid
        good2 = left
        left = 0
        right = (t + 1) // 2
        while left + 1 < right:
            mid = (left + right) // 2
            f = mid * (t - mid)
            if f > d:
                right = mid
            else:
                left = mid
        good1 = right
        if good1 == good2 and good1 * (t - good1) <= d:
            answer = 0
        answer = answer * (good2 - good1 + 1)
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
