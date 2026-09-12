from __future__ import annotations
import os

# import math
# import pprint
# import itertools
import re
from typing import Literal, Callable

# import functools
# import dataclasses
# import collections
# import operator
# import time

Side = Literal["top", "front", "left", "right", "back", "bottom"]


def safe_index_of(s: str, c: str, start: int = 0) -> int:
    try:
        return s.index(c, start)
    except ValueError:
        return -1


def safe_rindex_of(s: str, c: str, end: int = None) -> int:
    try:
        if end is not None:
            return s.rindex(c, 0, end)
        else:
            return s.rindex(c)
    except ValueError:
        return -1


def solution(inp: str) -> None:
    maze_str, commands_str = inp.split("\n\n")
    rows_num = len(maze_str.splitlines())
    cols_num = max(len(row) for row in maze_str.splitlines())
    edge_size = min(len(row.replace(" ", "")) for row in maze_str.splitlines())

    commands = re.findall(r"\d+|L|R", commands_str)

    print(f"{rows_num=}, {cols_num=}, {edge_size=}, {commands=}")


def main():
    with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
        test = input_file.read().rstrip()
        solution(test)
    # with open(os.path.join(os.path.dirname(__file__), "inputb.txt"), "r") as input_file:
    #     input = input_file.read().rstrip()
    #     solution(input)


if __name__ == "__main__":
    main()
