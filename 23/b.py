from __future__ import annotations
import os
import math

# import pprint
# import itertools
# import re
# import functools
import dataclasses

# import collections
# import operator
from typing import Literal  # , Callable

# import time

Direction = Literal["north", "south", "west", "east"]


@dataclasses.dataclass
class Elf:
    pos: complex  # row * 1j + col
    north: complex | None = None
    south: complex | None = None
    west: complex | None = None
    east: complex | None = None
    proposed: Direction = None

    def __hash__(self):
        return hash(self.pos)

    def get(self, direction: Direction) -> complex | None:
        return getattr(self, direction)


def solution(inp: str) -> None:
    elves: dict[complex, Elf] = {}
    proposals: dict[complex, int] = {}
    order: list[Direction] = ["north", "south", "west", "east"]

    lines = inp.split("\n")
    rows_num = len(lines)
    cols_num = len(lines[0])

    min_row, max_row = math.inf, -math.inf
    min_col, max_col = math.inf, -math.inf

    for row_idx, row in enumerate(lines):
        for col_idx, col in enumerate(row):
            if col == "#":
                min_row = min(min_row, row_idx)
                max_row = max(max_row, row_idx)
                min_col = min(min_col, col_idx)
                max_col = max(max_col, col_idx)
                elves[row_idx * 1j + col_idx] = Elf(row_idx * 1j + col_idx)
    round_num = 0
    while True:
        proposals = {}
        round_num += 1
        moved = False

        for elf in elves.values():
            pos = elf.pos
            added = 0
            elf.north = elf.south = elf.west = elf.east = elf.proposed = None
            if (
                # north
                pos - 1j not in elves
                and pos - 1j - 1 not in elves
                and pos - 1j + 1 not in elves
            ):
                elf.north = pos - 1j
                added += 1
            if (
                # south
                pos + 1j not in elves
                and pos + 1j - 1 not in elves
                and pos + 1j + 1 not in elves
            ):
                elf.south = pos + 1j
                added += 1
            if (
                # west
                pos - 1 not in elves
                and pos - 1 + 1j not in elves
                and pos - 1 - 1j not in elves
            ):
                elf.west = pos - 1
                added += 1
            if (
                # east
                pos + 1 not in elves
                and pos + 1 + 1j not in elves
                and pos + 1 - 1j not in elves
            ):
                elf.east = pos + 1
                added += 1

            if added == 4:
                elf.north = elf.south = elf.west = elf.east = None

            for direction in order:
                if elf.get(direction) is not None:
                    proposals[elf.get(direction)] = (
                        proposals.get(elf.get(direction), 0) + 1
                    )
                    elf.proposed = direction
                    break
            # if elf.north is not None:
            #     proposals[elf.north] = proposals.get(elf.north, 0) + 1
            # if elf.south is not None:
            #     proposals[elf.south] = proposals.get(elf.south, 0) + 1
            # if elf.west is not None:
            #     proposals[elf.west] = proposals.get(elf.west, 0) + 1
            # if elf.east is not None:
            #     proposals[elf.east] = proposals.get(elf.east, 0) + 1

        next_elves: dict[complex, Elf] = {}
        for elf in elves.values():
            # move = True
            # for direction in order:
            #     if elf.get(direction) is not None:
            #         if proposals.get(elf.get(direction), 0) > 1:
            #             move = False
            if elf.proposed == None or proposals.get(elf.get(elf.proposed), 0) > 1:
                next_elves[elf.pos] = elf
                continue

            moved = True
            elf.pos = elf.get(elf.proposed)
            min_row = min(min_row, elf.pos.imag)
            max_row = max(max_row, elf.pos.imag)
            min_col = min(min_col, elf.pos.real)
            max_col = max(max_col, elf.pos.real)
            next_elves[elf.pos] = elf
            # for direction in order:
            #     # if not move:
            #     #     break
            #     if elf.get(direction) is not None and elf.proposed == direction:
            #         if proposals.get(elf.get(direction), 0) == 1:
            #             elf.pos = elf.get(direction)
            #             min_row = min(min_row, elf.pos.imag)
            #             max_row = max(max_row, elf.pos.imag)
            #             min_col = min(min_col, elf.pos.real)
            #             max_col = max(max_col, elf.pos.real)
            #             next_elves[elf.pos] = elf
            #             break
            #         else:
            #             next_elves[elf.pos] = elf
            #             break
            # else:
            #     next_elves[elf.pos] = elf
        elves = next_elves
        # print(min_row, max_row, min_col, max_col)
        # area = (max_row - min_row + 1) * (max_col - min_col + 1)
        # unfilled_area = area - len(elves)
        # print(area, unfilled_area)
        # print(len(elves))
        if not moved:
            break

        order = order[1:] + order[:1]
    # print(int(unfilled_area))
    print(round_num)

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
