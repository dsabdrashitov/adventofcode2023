import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

WF_PAT = re.compile(r"([^{]+)\{([^}]*)}")
RULE_PAT = re.compile(r"(([xmas])([><])(\d+):)?([a-zAR]+)")
PART_PAT = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
ACCEPT = 'A'
REJECT = 'R'
START = "in"
MINV = 1
MAXV = 4000


def match(part, cond):
    if cond is None:
        return True
    if cond[1] == '<':
        return part[cond[0]] < cond[2]
    elif cond[1] == '>':
        return part[cond[0]] > cond[2]
    else:
        raise Exception(f"Unknown condition: {cond[1]}")


def outcome(part, workflows):
    current_name = START
    while current_name != ACCEPT and current_name != REJECT:
        rules = workflows[current_name]
        for rule in rules:
            if match(part, rule[0]):
                current_name = rule[1]
                break
    return current_name


def mult(values):
    result = 1
    for v in values:
        result = result * (v[1] - v[0])
    return result


def split(part, cond):
    if cond is None:
        return part, None
    acc = dict(part)
    rej = dict(part)
    if cond[1] == '<':
        acc[cond[0]] = (part[cond[0]][0], cond[2])
        rej[cond[0]] = (cond[2], part[cond[0]][1])
    elif cond[1] == '>':
        acc[cond[0]] = (cond[2] + 1, part[cond[0]][1])
        rej[cond[0]] = (part[cond[0]][0], cond[2] + 1)
    else:
        raise Exception(f"Unknown condition: {cond[1]}")
    if acc[cond[0]][0] >= acc[cond[0]][1]:
        acc = None
    if rej[cond[0]][0] >= rej[cond[0]][1]:
        rej = None
    return acc, rej


def solve(f):
    workflows = {}
    parts = []
    for line in f:
        line = line.strip()
        wf_match = WF_PAT.match(line)
        if wf_match:
            wf_name = wf_match.group(1)
            rms = RULE_PAT.findall(wf_match.group(2))
            rules = []
            for r in rms:
                if r[0]:
                    rules.append(((r[1], r[2], int(r[3])), r[4]))
                else:
                    rules.append((None, r[4]))
            workflows[wf_name] = rules
        part_match = PART_PAT.match(line)
        if part_match:
            parts.append({
                'x': int(part_match.group(1)),
                'm': int(part_match.group(2)),
                'a': int(part_match.group(3)),
                's': int(part_match.group(4)),
            })
    start_part = {'x': (MINV, MAXV + 1), 'm': (MINV, MAXV + 1), 'a': (MINV, MAXV + 1), 's': (MINV, MAXV + 1), }
    start_pos = (START, start_part)
    stack = [start_pos]
    answer = 0
    while len(stack) > 0:
        wf_name, part = stack.pop()
        if wf_name == REJECT:
            continue
        if wf_name == ACCEPT:
            _logger.debug(part.values())
            answer = answer + mult(part.values())
            continue
        for rule in workflows[wf_name]:
            acc, rej = split(part, rule[0])
            if acc is not None:
                stack.append((rule[1], acc))
            part = rej
            if part is None:
                break
        assert part is None
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
