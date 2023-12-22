import re
import logging

_logger = logging.getLogger(__name__)

# NAME = "sample.in"
NAME = "input.txt"

BROADCASTER = "broadcaster"
MACHINE = "rx"
IMPORTANT = "dh"


def send(name, children, signal, que):
    for dst in children[name]:
        _logger.debug(f"{name} -> {dst}, {signal}")
        que.append((dst, signal, name))


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
    pressed = 0
    names = []
    for name in children:
        names.append(name)
    names.sort()
    while True:
        que = [(BROADCASTER, False, None)]
        quer = 0
        pressed = pressed + 1
        while quer < len(que):
            name, signal, src = que[quer]
            if name == MACHINE and not signal:
                return pressed
            if name == IMPORTANT and signal:
                _logger.info(f"{pressed}: {src}")
            quer = quer + 1
            if action[name] == '':
                send(name, children, signal, que)
            elif action[name] == '&':
                last_signal[name][src] = signal
                res = True
                for _, val in last_signal[name].items():
                    if not val:
                        res = False
                        break
                send(name, children, not res, que)
            elif action[name] == '%':
                if not signal:
                    switch_state[name] = not switch_state[name]
                    send(name, children, switch_state[name], que)
            else:
                raise Exception("Unknown command.")


def main():
    with open(NAME, "r") as f:
        answer = solve(f)
        print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
