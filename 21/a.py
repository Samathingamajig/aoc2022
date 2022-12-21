from __future__ import annotations
import os
import math
import pprint
import itertools
import re
import functools
import dataclasses
import collections
import operator
import time


def solution(inp: str) -> None:
    monkeys: dict[str, list[int, str]] = dict()
    for line in inp.split("\n"):
        # print(line)
        name, command = line.split(": ")
        if len(command.split(" ")) == 1:
            monkeys[name] = [int(command), ""]
        else:
            monkeys[name] = [None, command]

    def get_value(name: str) -> int:
        if monkeys[name][0] is not None:
            return monkeys[name][0]
        else:
            # print(name, monkeys[name][1])
            m1, op, m2 = monkeys[name][1].split(" ")
            monkeys[name][0] = eval(str(get_value(m1)) + op + str(get_value(m2)))
            return monkeys[name][0]

    print(get_value("root"))


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)


if __name__ == "__main__":
    main()
