import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

INSTRUCTION_PAT = re.compile(r"([^-=,]+)([-=])(\d*)")
REMOVE = '-'
ADD = '='


def hash17(s):
    result = 0
    for c in s:
        result = ((result + ord(c)) * 17) % 256
    return result


def solve(f):
    instructions = []
    for line in f:
        line = line.strip()
        instructions.extend(INSTRUCTION_PAT.findall(line))
    buckets = [{} for _ in range(256)]
    buckets_counters = [0] * 256
    for inst in instructions:
        h = hash17(inst[0])
        if inst[1] == REMOVE:
            if inst[0] in buckets[h]:
                del buckets[h][inst[0]]
        elif inst[1] == ADD:
            if inst[0] in buckets[h]:
                buckets[h][inst[0]] = (buckets[h][inst[0]][0], int(inst[2]))
            else:
                buckets[h][inst[0]] = (buckets_counters[h], int(inst[2]))
                buckets_counters[h] = buckets_counters[h] + 1
        else:
            raise Exception("Unknown instruction")
    answer = 0
    for b in range(len(buckets)):
        bucket = buckets[b]
        if len(bucket) > 0:
            _logger.debug(bucket)
        lenses = list(bucket.values())
        lenses.sort(key=lambda x: x[0])
        for i in range(len(lenses)):
            power = (b + 1) * (i + 1) * lenses[i][1]
            _logger.debug(f"{b + 1} * {i + 1} * {lenses[i][1]} = {power}")
            answer = answer + power
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
