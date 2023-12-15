import re
from typing import Match
from bisect import bisect_right

# NAME = "sample.in"
NAME = "input.txt"


def find_match(f, pat: str, skip=True) -> Match[str] | None:
    pattern = re.compile(pat)
    while True:
        line = f.readline()
        if len(line) == 0:
            return None
        line = line.strip()
        match = pattern.match(line)
        if match is not None:
            return match
        if not skip:
            return None


def solve(f):
    answer = 0

    seeds_match = find_match(f, r"seeds: ([\s\d]+)")
    seeds = [int(s.group()) for s in re.compile(r"\d+").finditer(seeds_match.group(1))]
    print(seeds)

    while True:
        header_match = find_match(f, r"([^\s]+)-to-([^\s]+) map:")
        if header_match is None:
            break
        print(header_match)
        mappings = []
        while True:
            mapping_match = find_match(f, r"(\d+)\s+(\d+)\s+(\d+)", skip=False)
            if mapping_match is None:
                break
            mappings.append([int(mapping_match.group(1)), int(mapping_match.group(2)), int(mapping_match.group(3))])
        print(mappings)
        mappings.sort(key=lambda m: m[1])
        print(mappings)
        for i in range(len(seeds)):
            s = seeds[i]
            ind = bisect_right(mappings, s, key=lambda m: m[1])
            if ind > 0 and s < mappings[ind - 1][1] + mappings[ind - 1][2]:
                seeds[i] = mappings[ind - 1][0] + s - mappings[ind - 1][1]
                print(f"{s} -> {seeds[i]}")
    answer = min(seeds)

    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
