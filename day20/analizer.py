import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

BROADCASTER = "broadcaster"
MACHINE = "rx"


def solve(f):
    line_pat = re.compile(r"([%&]?[a-z]+) -> (.*)")
    part_pat = re.compile(r"[a-z]+")
    children = {}
    action = {}
    for line in f:
        match = line_pat.match(line)
        head = match.group(1)
        tail = part_pat.findall(match.group(2))
        if head.startswith("%"):
            name = head[1:]
            a = "%"
        elif head.startswith("&"):
            name = head[1:]
            a = "&"
        else:
            name = head
            a = ""
        action[name] = a
        children[name] = tail
    fake_nodes = set()
    for name, clist in children.items():
        for c in clist:
            if c not in children:
                fake_nodes.add(c)
    for c in fake_nodes:
        action[c] = ""
        children[c] = []
    last_signal = {}
    switch_state = {}
    for name in children:
        last_signal[name] = {}
        switch_state[name] = False
    for name, lst in children.items():
        for child in lst:
            last_signal[child][name] = False
    names = []
    for name in children:
        names.append(name)
    names.sort()

    depends = {}
    for name in children:
        depends[name] = {name}
    while True:
        done = False
        for name, clist in children.items():
            dep = depends[name]
            for c in clist:
                for g in dep:
                    if g not in depends[c]:
                        depends[c].add(g)
                        done = True
        if not done:
            break
    for name in names:
        print(name, list(last_signal[name].keys()))

    return 0


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
