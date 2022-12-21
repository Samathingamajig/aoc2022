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


def with_number(original_monkeys, human_number) -> tuple[int, int]:
    monkeys = {k: v[:] for k, v in original_monkeys.items()}
    target1, _, target2 = monkeys["root"][1].split(" ")
    monkeys["humn"][0] = human_number

    def get_value(name: str) -> int:
        if monkeys[name][0] is not None:
            return monkeys[name][0]
        else:
            # print(name, monkeys[name][1])
            m1, op, m2 = monkeys[name][1].split(" ")
            monkeys[name][0] = eval(str(get_value(m1)) + op + str(get_value(m2)))
            return monkeys[name][0]

    return get_value(target1), get_value(target2)


def solution(inp: str) -> None:
    original_monkeys: dict[str, list[int, str]] = dict()
    x1, x2 = (
        1000000000000,
        2000000000000,
    )  # honestly no clue why these work, i started with 1 and 2 and just continuously multiplied by 10 until it worked. one more or less 0 and it doesn't work. something to do with floating point shenanigans
    for line in inp.split("\n"):
        # print(line)
        name, command = line.split(": ")
        if len(command.split(" ")) == 1:
            original_monkeys[name] = [int(command), ""]
        else:
            original_monkeys[name] = [None, command]
    one, two, three = (
        with_number(original_monkeys, x1),
        with_number(original_monkeys, x2),
        with_number(original_monkeys, 3),
    )
    d_y = two[0] - one[0]
    d_x = x2 - x1
    delta_y = one[0] - one[1]
    print(one)
    print(two)
    print(three)
    print(d_y, d_x, delta_y)
    # new = -(delta_y / d_y) + 1
    # new = (one[1] - one[0]) / ((two[0] - one[0]) / (2 - 1)) + 1
    # f = lambda x: (d_y / d_x) * (x - 1) + one[0]
    # slope = (f(2) - f(1)) / (2 - 1)

    # new = (one[1] - one[0]) / slope + 1
    # slope*(new - 1) + one[0]
    new = (one[1] - one[0]) / ((two[0] - one[0]) / (x2 - x1)) + x1
    # new = 3247317268284
    # new = 3246683150479.1724
    print(new)

    # while True:
    #     print(eval(input("> ")))
    # new = int(new)
    # new = int(new)
    print(
        "diff",
        with_number(original_monkeys, new)[0] - with_number(original_monkeys, new)[1],
    )
    if with_number(original_monkeys, new)[0] == with_number(original_monkeys, new)[1]:
        print(int(new))
    # else:
    #     i = 0
    #     while True:
    #         i += 1
    #         print(
    #             "+diff",
    #             with_number(original_monkeys, new + i)[0]
    #             - with_number(original_monkeys, new + i)[1],
    #         )
    #         print(
    #             "-diff",
    #             with_number(original_monkeys, new - i)[0]
    #             - with_number(original_monkeys, new - i)[1],
    #         )
    #         if (
    #             with_number(original_monkeys, new + i)[0]
    #             == with_number(original_monkeys, new + i)[1]
    #         ):
    #             print(new + i)
    #             break
    #         elif (
    #             with_number(original_monkeys, new - i)[0]
    #             == with_number(original_monkeys, new - i)[1]
    #         ):
    #             print(new - i)
    #             break

    # print(one, two, three)
    # print(i)


def graph(inp: str) -> None:
    original_monkeys: dict[str, list[int, str]] = dict()
    output = ""
    for line in inp.split("\n"):
        # print(line)
        name, command = line.split(": ")
        if len(command.split(" ")) == 1:
            original_monkeys[name] = [int(command), ""]
            output += name + "\n"
        else:
            original_monkeys[name] = [None, command]
            output += name + " " + command.split(" ")[0] + "\n"
            output += name + " " + command.split(" ")[2] + "\n"
    with open(os.path.join(os.path.dirname(__file__), "graph.txt"), "w") as output_file:
        output_file.write(output)


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    #     # graph(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)
        # graph(input)


if __name__ == "__main__":
    main()
