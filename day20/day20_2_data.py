import re
import logging

_logger = logging.getLogger(__name__)


def gcd(a, b):
    while a > 0:
        tmp = b % a
        b = a
        a = tmp
    return b


def lcm(a):
    result = a[0]
    for x in a:
        result = result * x // gcd(result, x)
    return result


def main():
    values = [3739, 3761, 3797, 3889]
    answer = lcm(values)
    print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    main()
