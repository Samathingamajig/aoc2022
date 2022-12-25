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
from typing import Literal, Callable
import time


@dataclasses.dataclass
class Blizzard:
    position: complex
    direction: complex


def solution(inp: str) -> None:
    start_col = inp.index(".")
    end_col = inp.split("\n")[-1].index(".")

    max_col = inp.index("\n") - 1
    max_row = inp.count("\n")
    # print(max_col, max_row)
    # print(complex(end_col, max_row))
    # input()

    arrow_to_direction = {
        ">": complex(1, 0),
        "<": complex(-1, 0),
        "^": complex(0, -1),
        "v": complex(0, 1),
    }

    blizzards = []

    for row_index, row in enumerate(inp.split("\n")):
        for col_index, char in enumerate(row):
            if char in arrow_to_direction:
                blizzard = Blizzard(
                    complex(col_index, row_index), arrow_to_direction[char]
                )
                blizzards.append(blizzard)

    queue = set([complex(start_col, 0)])
    next_queue = set()

    directions = [
        0 + 0j,
        1 + 0j,
        -1 + 0j,
        0 + 1j,
        0 - 1j,
    ]

    moves = 0

    while True:
        moves += 1
        blizzard_positions = set()
        for blizzard in blizzards:
            blizzard.position += blizzard.direction
            if blizzard.position.real <= 0:
                blizzard.position = complex(max_col - 1, blizzard.position.imag)
            elif blizzard.position.real >= max_col:
                blizzard.position = complex(1, blizzard.position.imag)
            elif blizzard.position.imag <= 0:
                blizzard.position = complex(blizzard.position.real, max_row - 1)
            elif blizzard.position.imag >= max_row:
                blizzard.position = complex(blizzard.position.real, 1)
            blizzard_positions.add(blizzard.position)

        solved = False
        # print("queue len", len(queue))
        for position in queue:
            if solved:
                break
            for direction in directions:
                # print(position + direction)
                new_position = position + direction
                if new_position == complex(end_col, max_row):
                    solved = True
                    break
                if new_position in blizzard_positions:
                    continue
                if (
                    new_position.real <= 0
                    or new_position.real >= max_col
                    or new_position.imag <= 0
                    or new_position.imag >= max_row
                ) and not (new_position == complex(start_col, 0)):
                    continue
                next_queue.add(new_position)
        # input()
        queue = next_queue
        next_queue = set()
        # print(moves)
        if solved:
            break

    print(moves)

    pass


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)


if __name__ == "__main__":
    main()
