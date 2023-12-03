# NAME = "sample.in"
NAME = "input.txt"

DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def solve(f):
    num_sum = 0
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        first_pos = len(line)
        last_pos = -1
        first_str = None
        last_str = None
        for k in DIGITS:
            fpos = line.find(k)
            if fpos != -1:
                if first_pos > fpos:
                    first_pos = fpos
                    first_str = k
                lpos = line.rfind(k) + len(k)
                if last_pos < lpos:
                    last_pos = lpos
                    last_str = k
        first = DIGITS[first_str]
        last = DIGITS[last_str]
        num = int(10 * first + last)
        num_sum = num_sum + num
    return num_sum


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
