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
    # print(cols_num)

    maze_str = "".join(f"{row:<{cols_num}}" for row in maze_str.splitlines())

    maze_row_first = [
        [maze_str[row * cols_num + col] for col in range(cols_num)]
        for row in range(rows_num)
    ]

    maze_col_first = [
        [maze_str[row * cols_num + col] for row in range(rows_num)]
        for col in range(cols_num)
    ]

    commands = re.findall(r"\d+|L|R", commands_str)

    # real, imag = x, yj
    pos = maze_row_first[0].index(".") + 0j
    dir = 1 + 0j  # right

    count = 0
    # print(count, pos, dir)
    # input()

    log = ""

    for command in commands:
        if command == "L":
            dir *= -1j
            # print("L", dir)
            log += "L"
            continue
        elif command == "R":
            dir *= 1j
            # print("R", dir)
            log += "R"
            continue
        # print("start", pos, dir, command)

        line = "".join(
            maze_col_first[int(pos.real)]
            if dir.real == 0
            else maze_row_first[int(pos.imag)]
        )

        real_dir = int(dir.real) or int(dir.imag)
        real_pos = int(pos.real) if dir.real else int(pos.imag)
        # print("".join("X" if idx == real_pos else c for idx, c in enumerate(line)))

        min_i = min(safe_index_of(line, "#"), safe_index_of(line, "."))
        if min_i == -1:
            min_i = safe_index_of(line, "#")
            if min_i == -1:
                min_i = safe_index_of(line, ".")
        max_i = max(safe_rindex_of(line, "#"), safe_rindex_of(line, "."))
        width = max_i - min_i + 1
        diff = max_i - min_i
        count += 1
        infinitely_safe = "#" not in line
        first_unsafe = safe_index_of(line, "#")
        last_unsafe = safe_rindex_of(line, "#")
        first_safe = safe_index_of(line, ".")
        last_safe = safe_rindex_of(line, ".")
        # print(log)
        # print("attempt to move", command, "blocks")
        if maze_col_first[int(pos.real)][int(pos.imag)] == " ":
            # print("what")
            break

        def move():
            if infinitely_safe:
                # print("infinitely safe")
                new = (
                    real_pos - min_i + int(command) * real_dir + diff * 2
                ) % diff + min_i
                if dir.real:
                    return new + pos.imag * 1j
                else:
                    return new * 1j + pos.real
            if real_dir > 0:
                next_unsafe = safe_index_of(line, "#", real_pos + 1)
                if next_unsafe != -1:  # if theres a wall before looping
                    # print("wall before looping", next_unsafe)
                    if dir.real:
                        return (
                            min(next_unsafe - 1, pos.real + int(command))
                            + pos.imag * 1j
                        )
                    else:
                        return (
                            min(next_unsafe - 1, pos.imag + int(command)) * 1j
                            + pos.real
                        )
                # theres no wall before looping
                # print("no wall before looping", next_unsafe)
                # if we don't need to loop
                if dir.real and pos.real + int(command) <= max_i:
                    # print("no need to loop")
                    return (pos.real + int(command)) + pos.imag * 1j
                elif dir.imag and pos.imag + int(command) <= max_i:
                    # print("no need to loop")
                    return (pos.imag + int(command)) * 1j + pos.real

                # print("need to loop")
                # if theres a barrier at the beginning of the loop
                # print("check if theres a barrier at the beginning of the loop")
                if first_unsafe == min_i:
                    # print("barrier at the beginning of the loop")
                    if dir.real:

                        return max_i + pos.imag * 1j
                    else:
                        return max_i * 1j + pos.real

                # print("no barrier at the beginning of the loop, need to loop")
                # no barrier at the beginning of the loop, need to loop
                new = min(
                    min_i + (int(command) - (max_i - real_pos) - 1),
                    first_unsafe - 1,
                )
                if dir.real:
                    return new + pos.imag * 1j
                else:
                    return new * 1j + pos.real
            else:
                next_unsafe = safe_rindex_of(line, "#", real_pos)
                if next_unsafe != -1:
                    # print("else wall before looping", next_unsafe)
                    if dir.real:
                        return (
                            max(next_unsafe + 1, pos.real - int(command))
                            + pos.imag * 1j
                        )
                    else:
                        return (
                            max(next_unsafe + 1, pos.imag - int(command)) * 1j
                            + pos.real
                        )
                # theres no wall before looping
                # print("no wall before looping", next_unsafe)

                # if we don't need to loop
                if dir.real and pos.real - int(command) >= min_i:
                    # print("no need to loop")
                    return (pos.real - int(command)) + pos.imag * 1j
                elif dir.imag and pos.imag - int(command) >= min_i:
                    # print("no need to loop")
                    return (pos.imag - int(command)) * 1j + pos.real

                # print("need to loop")
                # if theres a barrier at the beginning of the loop
                # print("check if theres a barrier at the beginning of the loop")
                if last_unsafe == max_i:
                    # print("barrier at the beginning of the loop")
                    if dir.real:
                        return min_i + pos.imag * 1j
                    else:
                        return min_i * 1j + pos.real

                # print("no barrier at the beginning of the loop, need to loop")

                # no barrier at the beginning of the loop, need to loop
                new = max(
                    max_i - (int(command) - (real_pos - min_i) - 1),
                    last_unsafe + 1,
                )
                if dir.real:
                    return new + pos.imag * 1j
                else:
                    return new * 1j + pos.real

        pos = move()
        new_real_pos = int(pos.real) if dir.real else int(pos.imag)
        # print("".join("X" if idx == real_pos else c for idx, c in enumerate(line)))
        # print("".join("X" if idx == new_real_pos else c for idx, c in enumerate(line)))
        # print("<" if real_dir < 0 else ">", command, real_dir, dir)
        # print(count, pos, dir)
        # print()
        # print()
        # input()
        # print("end", pos)
        # print()
        # print()

    pos += 1 + 1j
    facing_score = {
        1: 0,
        1j: 1,
        -1: 2,
        -1j: 3,
    }
    score = int((pos.imag * 1000) + (pos.real * 4) + facing_score[dir])
    print(score)

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
