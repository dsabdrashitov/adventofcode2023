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
    answer = 0
    for part in parts:
        out = outcome(part, workflows)
        if out == ACCEPT:
            answer = answer + sum(part.values())
        elif out == REJECT:
            pass
        else:
            raise Exception(f"Unknown result: {out}")
    return answer


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
