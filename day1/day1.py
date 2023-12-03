import re

# NAME = "sample.in"
NAME = "input.txt"


def solve(f):
    num_sum = 0
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        digits = re.findall(r'\d', line)
        first = digits[0]
        last = digits[-1]
        num = int(first + last)
        num_sum = num_sum + num
    return num_sum


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
