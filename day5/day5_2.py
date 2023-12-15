import re
from typing import Match

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


def intersect(s, m):
    return max(s[0], m[1]), min(s[0] + s[1], m[1] + m[2]) - max(s[0], m[1])


def solve(f):
    seeds_match = find_match(f, r"seeds: ([\s\d]+)")
    seeds = [int(s.group()) for s in re.compile(r"\d+").finditer(seeds_match.group(1))]
    print(seeds)
    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
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
            mappings.append((int(mapping_match.group(1)), int(mapping_match.group(2)), int(mapping_match.group(3))))
        print(mappings)
        mappings.sort(key=lambda m: m[1])
        print(mappings)
        seeds.sort(key=lambda s: s[0])
        i = 0
        j = 0
        mapped = []
        while i < len(seeds):
            if j == len(mappings):
                mapped.append(seeds[i])
                i = i + 1
            elif mappings[j][1] > seeds[i][0]:
                mapped.append((seeds[i][0], min(seeds[i][0] + seeds[i][1], mappings[j][1]) - seeds[i][0]))
                seeds[i] = (mappings[j][1], seeds[i][0] + seeds[i][1] - mappings[j][1])
                if seeds[i][1] <= 0:
                    i = i + 1
            else:
                inter = intersect(seeds[i], mappings[j])
                if inter[1] > 0:
                    mapped.append((inter[0] - mappings[j][1] + mappings[j][0], inter[1]))
                    seeds[i] = (mappings[j][1] + mappings[j][2],
                                seeds[i][0] + seeds[i][1] - mappings[j][1] - mappings[j][2])
                    if seeds[i][1] <= 0:
                        i = i + 1
                else:
                    j = j + 1
        print(f"{seeds}\n->\n{mapped}")
        seeds = mapped
    answer = min(seeds)

    return answer[0]


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    main()
