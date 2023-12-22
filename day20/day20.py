import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

# PRESSES = 1
PRESSES = 1000

BROADCASTER = "broadcaster"


def send(name, children, signal, que, answer):
    for dst in children[name]:
        _logger.debug(f"{name} -> {dst}, {signal}")
        que.append((dst, signal, name))
        if signal:
            answer[1] = answer[1] + 1
        else:
            answer[0] = answer[0] + 1


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
    answer = [0, 0]
    last_signal = {}
    switch_state = {}
    for name in children:
        last_signal[name] = {}
        switch_state[name] = False
    for name, lst in children.items():
        for child in lst:
            last_signal[child][name] = False
    for i in range(PRESSES):
        que = [(BROADCASTER, False, None)]
        quer = 0
        answer[0] = answer[0] + 1
        while quer < len(que):
            name, signal, src = que[quer]
            quer = quer + 1
            if action[name] == '':
                send(name, children, signal, que, answer)
            elif action[name] == '&':
                last_signal[name][src] = signal
                res = True
                for _, val in last_signal[name].items():
                    if not val:
                        res = False
                        break
                send(name, children, not res, que, answer)
            elif action[name] == '%':
                if not signal:
                    switch_state[name] = not switch_state[name]
                    send(name, children, switch_state[name], que, answer)
            else:
                raise Exception("Unknown command.")
    return answer[0] * answer[1]


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
