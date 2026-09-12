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

Side = (
    Literal["top"]
    | Literal["front"]
    | Literal["left"]
    | Literal["right"]
    | Literal["back"]
    | Literal["bottom"]
)


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


def solution(
    inp: str,
    inp_b: str,
    labeled_zones: list[list[str | None]],
    labeled_zones_b: list[list[str | None]],
    zone_rotations: Callable[[str, complex], complex],
    get_line: Callable[
        [
            Side,
            complex,
            complex,
            int,
            dict[Side, list[list[str]]],
            dict[Side, list[list[str]]],
        ],
        tuple[int, str, bool],
    ],
    index_to_pos: Callable[
        [int, Side, complex, complex, int, int, list[list[str | None]]],
        tuple[int, str, bool],
    ],
) -> None:

    maze_str, commands_str = inp_b.split("\n\n")
    rows_num = len(maze_str.splitlines())
    cols_num = max(len(row) for row in maze_str.splitlines())
    edge_size = min(len(row.replace(" ", "")) for row in maze_str.splitlines())
    # print(edge_size)

    maze_str = "".join(f"{row:<{cols_num}}" for row in maze_str.splitlines())

    maze_row_first = [
        [maze_str[row * cols_num + col] for col in range(cols_num)]
        for row in range(rows_num)
    ]

    maze_col_first = [
        [maze_str[row * cols_num + col] for row in range(rows_num)]
        for col in range(cols_num)
    ]

    faces_row_first: dict[
        Side,
        list[list[str]],
    ] = {}
    faces_col_first: dict[Side, list[list[str]]] = {}
    for i, labeled_zones_row in enumerate(labeled_zones_b):
        for j, labeled_zone in enumerate(labeled_zones_row):
            if labeled_zone is None:
                continue
            faces_row_first[labeled_zone] = [
                [
                    maze_str[row * cols_num + col]
                    for col in range(j * edge_size, j * edge_size + edge_size)
                ]
                for row in range(i * edge_size, i * edge_size + edge_size)
            ]
            faces_col_first[labeled_zone] = [
                [
                    maze_str[row * cols_num + col]
                    for row in range(i * edge_size, i * edge_size + edge_size)
                ]
                for col in range(j * edge_size, j * edge_size + edge_size)
            ]

    # print("\n".join("".join(row) for row in faces_row_first["right"]))

    commands = re.findall(r"\d+|L|R", commands_str)

    def pos_to_face(pos: complex) -> str:
        return labeled_zones_b[int(pos.imag) // edge_size][int(pos.real) // edge_size]

    # real, imag = x, yj
    pos = maze_row_first[0].index(".") + 0j
    dir = 1 + 0j  # right
    # right = 1 + 0j
    # down = 0 + 1j

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
        print(count)
        # print("start", pos, dir, command)

        # def get_lines_example(
        #     starting_face: Side,
        #     starting_pos: complex,
        #     dir: complex,
        #     side_length: int,
        #     faces_row_first: dict[Side, list[list[str]]],
        #     faces_col_first: dict[Side, list[list[str]]],
        # ) -> str:
        index, line, should_reverse = get_line(
            pos_to_face(pos), pos, dir, edge_size, faces_row_first, faces_col_first
        )
        print(index, line, dir)
        # input()

        real_dir = int(dir.real) or int(dir.imag) * (-1 if should_reverse else 1)
        print(f"{real_dir=}")
        # real_pos = int(pos.real) if dir.real else int(pos.imag)
        real_pos = index
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
                print("infinitely safe")
                new = (
                    real_pos - min_i + int(command) * real_dir + diff * 2
                ) % diff + min_i
                return new
            if real_dir > 0:
                next_unsafe = safe_index_of(line, "#", real_pos + 1)
                if next_unsafe != -1:  # if theres a wall before looping
                    print("wall before looping", next_unsafe)
                    return min(next_unsafe - 1, real_pos + int(command))
                # theres no wall before looping
                print("no wall before looping", next_unsafe)
                # if we don't need to loop
                if real_pos + int(command) <= max_i:
                    print("no need to loop")
                    return real_pos + int(command)

                print("need to loop")
                # if theres a barrier at the beginning of the loop
                print("check if theres a barrier at the beginning of the loop")
                if first_unsafe == min_i:
                    print("barrier at the beginning of the loop")
                    return max_i

                print("no barrier at the beginning of the loop, need to loop")
                # no barrier at the beginning of the loop, need to loop
                return min(
                    min_i + (int(command) - (max_i - real_pos) - 1),
                    first_unsafe - 1,
                )
            else:
                next_unsafe = safe_rindex_of(line, "#", real_pos)
                if next_unsafe != -1:
                    print("else wall before looping", next_unsafe)
                    return max(next_unsafe + 1, real_pos - int(command))
                # theres no wall before looping
                print("no wall before looping", next_unsafe)

                # if we don't need to loop
                if real_pos - int(command) >= min_i:
                    print("no need to loop")
                    return real_pos - int(command)

                print("need to loop")
                # if theres a barrier at the beginning of the loop
                print("check if theres a barrier at the beginning of the loop")
                if last_unsafe == max_i:
                    print("barrier at the beginning of the loop")
                    return min_i

                print("no barrier at the beginning of the loop, need to loop")

                # no barrier at the beginning of the loop, need to loop
                return max(
                    max_i - (int(command) - (real_pos - min_i) - 1),
                    last_unsafe + 1,
                )

        new_index = move()
        print(line)
        print(" " * (index) + "^")
        print(line)
        print(" " * (new_index) + "^")
        print("new_index", new_index)
        pos, dir = index_to_pos(
            new_index, pos_to_face(pos), pos, dir, real_dir, edge_size, labeled_zones_b
        )
        print("new pos", pos)
        input()
        # new_real_pos = int(pos.real) if dir.real else int(pos.imag)
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
    print(pos_to_face(pos), pos, dir, score)
    print(score)

    pass


def get_lines(
    starting_face: Side,
    starting_pos: complex,
    dir: complex,
    side_length: int,
    faces_row_first: dict[Side, list[list[str]]],
    faces_col_first: dict[Side, list[list[str]]],
) -> str:
    x, y = int(starting_pos.real % side_length), int(starting_pos.imag % side_length)

    def flip(n):
        return side_length - 1 - n

    r = faces_row_first
    c = faces_col_first

    line_list = []

    index = -1

    should_reverse = False

    if dir.imag and starting_face in ("top", "front", "bottom", "back"):
        if starting_face == "top":
            index = y
        elif starting_face == "front":
            index = y + side_length
        elif starting_face == "bottom":
            index = y + side_length * 2
        elif starting_face == "back":
            index = y + side_length * 3
        line_list = c["top"][x], c["front"][x], c["bottom"][x], c["back"][x]
        pass
    elif dir.real and starting_face in ("left", "front", "right", "back"):
        if starting_face == "left":
            index = x
        elif starting_face == "front":
            index = x + side_length
        elif starting_face == "right":
            index = x + side_length * 2
        elif starting_face == "back":
            print(f"{x=}, {y=}")
            x = flip(x)
            y = flip(y)
            print(f"{x=}, {y=}")
            should_reverse = True
            index = x + side_length * 3
        line_list = r["left"][y], r["front"][y], r["right"][y], r["back"][flip(y)][::-1]
        pass
    elif (dir.real and starting_face in ("top", "bottom")) or (
        dir.imag and starting_face in ("left", "right")
    ):
        if starting_face == "top":
            index = x
        elif starting_face == "right":
            x, y = y, flip(x)
            index = x + side_length
        elif starting_face == "bottom":
            x, y = flip(x), flip(y)
            index = x + side_length * 2
            should_reverse = True
        elif starting_face == "left":
            x, y = flip(y), x
            index = x + side_length * 3
            should_reverse = True
        line_list = (
            r["top"][y],
            c["right"][flip(y)],
            r["bottom"][flip(y)][::-1],
            c["left"][y][::-1],
        )
        pass

    output = "".join("".join(part) for part in line_list)

    # print(output)
    # print(" " * (index) + "^")
    # if should_reverse:
    #     output = output[::-1]
    #     index = len(output) - 1 - index
    print(output)
    print(" " * (index) + "^")
    return index, output, should_reverse


def index_to_pos(
    index: int,
    starting_face: Side,
    starting_pos: complex,
    dir: complex,
    move_dir: int,
    side_length: int,
    labeled_zones: list[list[str | None]],
) -> complex:
    def flip(n):
        return side_length - 1 - n

    x, y = int(starting_pos.real % side_length), int(starting_pos.imag % side_length)
    col, row = -1, -1
    i_offset = index % side_length
    face_i = index // side_length
    face: Side = ""
    print("x,y,o", x, y, i_offset)

    new_dir = dir

    if dir.imag and starting_face in ("top", "front", "bottom", "back"):
        face = ["top", "front", "bottom", "back"][face_i]
        col = x
        row = i_offset
        pass
    elif dir.real and starting_face in ("left", "front", "right", "back"):
        face = ["left", "front", "right", "back"][face_i]
        if starting_face == "back":
            x, y = flip(x), flip(y)

        row = y
        col = i_offset
        if face == "back":
            row = flip(y)
            col = flip(i_offset)
            pass

        if (face == "back") ^ (starting_face == "back"):
            new_dir = -dir

        pass
    elif (dir.real and starting_face in ("top", "bottom")) or (
        dir.imag and starting_face in ("left", "right")
    ):
        faces = ["top", "right", "bottom", "left"]
        face = faces[face_i]
        if starting_face == "right":
            x, y = y, flip(x)
        elif starting_face == "bottom":
            x, y = flip(x), flip(y)
        elif starting_face == "left":
            x, y = flip(y), x

        if face == "top":
            row = y
            col = i_offset
        elif face == "right":
            row = x
            col = i_offset
        elif face == "bottom":
            row = flip(y)
            col = flip(i_offset)
        elif face == "left":
            row = flip(x)
            col = flip(i_offset)

        diff = (face_i - faces.index(starting_face) + 4 * 2) % 4
        for _ in range(diff):
            new_dir = new_dir * 1j

        pass

    pass
    top_left = -1 + -1j
    for labeled_zone_row_index, labeled_zone_row in enumerate(labeled_zones):
        found = False
        for labeled_zone_col_index, labeled_zone in enumerate(labeled_zone_row):
            if labeled_zone == face:
                top_left = (
                    labeled_zone_col_index * side_length
                    + labeled_zone_row_index * side_length * 1j
                )
                found = True
                break
        if found:
            break
    else:
        print(f"not found {face}")
    print("f,tl,c,r", face, top_left, col, row)
    return (top_left.real + col) + (top_left.imag + row) * 1j, new_dir


def main():
    with (
        open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file,
        open(
            os.path.join(os.path.dirname(__file__), "test_b.txt"), "r"
        ) as input_file_b,
    ):
        test = input_file.read().rstrip()
        test_b = input_file_b.read().rstrip()
        solution(
            test,
            test_b,
            [
                [None, None, "top", None],
                ["back", "left", "front", None],
                [None, None, "bottom", "right"],
            ],
            [
                [None, "top", None],
                ["left", "front", "right"],
                [None, "bottom", None],
                [None, "back", None],
            ],
            lambda a, b: None,
            get_lines,
            index_to_pos,
        )
    # with open(os.path.join(os.path.dirname(__file__), "inputb.txt"), "r") as input_file:
    #     input = input_file.read().rstrip()
    #     solution(input)


if __name__ == "__main__":
    main()
