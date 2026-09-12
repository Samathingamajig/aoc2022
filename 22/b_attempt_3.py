from os import path
import re
from dataclasses import dataclass
from colorama import init as colorama_init, Back, Style
from typing import Literal, Optional, Union

Instruction = Union[int, Literal["L"], Literal["R"]]


@dataclass(frozen=True)
class Direction:
    dr: int
    dc: int


DIRECTION_UP = Direction(-1, 0)
DIRECTION_RIGHT = Direction(0, 1)
DIRECTION_DOWN = Direction(1, 0)
DIRECTION_LEFT = Direction(0, -1)


@dataclass(frozen=True)
class Position2:
    row: int
    col: int


@dataclass(frozen=True)
class Position3:
    face: int
    row: int
    col: int


@dataclass(frozen=True)
class Transformation:
    direction: Direction
    destination_face: int
    clockwise_rotations: int


def get_input() -> str:
    with open(path.join(path.dirname(__file__), "input.txt")) as f:
        return f.read()


def parse_input(text: str) -> tuple[list[str], list[Instruction]]:
    map_raw, instructions_raw = text.split("\n\n")
    map_lines = map_raw.splitlines()

    instruction_regex = re.compile(r"\d+|[LR]")
    instructions: list[Instruction] = [
        instruction if instruction in ("L", "R") else int(instruction)
        for instruction in instruction_regex.findall(instructions_raw)
    ]

    return map_lines, instructions


def extract_face(
    map_lines: list[str], row: int, col: int, size: int, used_size: Optional[int] = None
) -> list[str]:
    if used_size is None:
        used_size = size

    return [
        line[col * size : col * size + used_size]
        for line in map_lines[row * size : row * size + used_size]
    ]


def extract_faces(
    map_lines: list[str], size: int, used_size: Optional[int] = None
) -> list[list[str]]:
    return [
        extract_face(map_lines, row, col, size, used_size)
        for row, line in enumerate(map_lines[::size])
        for col, corner in enumerate(line[::size])
        if corner != " "
    ]


def transform_shift(direction: Direction, pos: Position2, size: int) -> Position2:
    if direction == DIRECTION_UP:
        return Position2(size - 1, pos.col)
    if direction == DIRECTION_RIGHT:
        return Position2(pos.row, 0)
    if direction == DIRECTION_DOWN:
        return Position2(0, pos.col)
    if direction == DIRECTION_LEFT:
        return Position2(pos.row, size - 1)

    raise ValueError(f"Direction {direction} invalid")


def transform_rotate(clockwise_rotations: int, pos: Position2, size: int) -> Position2:
    edge = size - 1
    for _ in range(clockwise_rotations):
        if pos.row == 0 and pos.col < edge:
            pos = Position2(pos.col, edge)
        elif pos.col == edge and pos.row < edge:
            pos = Position2(edge, edge - pos.row)
        elif pos.row == edge and pos.col != 0:
            pos = Position2(pos.col, 0)
        elif pos.col == 0:
            pos = Position2(0, edge - pos.row)
        else:
            AssertionError("this position state should be impossible")

    return pos


TRANSFORMATIONS: list[dict[Direction, Transformation]] = [
    # 0
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 5, 1),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 1, 0),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 2, 0),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 3, 2),
    },
    # 1
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 5, 0),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 4, 2),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 2, 1),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 0, 0),
    },
    # 2
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 0, 0),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 1, 3),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 4, 0),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 3, 3),
    },
    # 3
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 2, 1),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 4, 0),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 5, 0),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 0, 2),
    },
    # 4
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 2, 0),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 1, 2),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 5, 1),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 3, 0),
    },
    # 5
    {
        DIRECTION_UP: Transformation(DIRECTION_UP, 3, 0),
        DIRECTION_RIGHT: Transformation(DIRECTION_RIGHT, 4, 3),
        DIRECTION_DOWN: Transformation(DIRECTION_DOWN, 1, 0),
        DIRECTION_LEFT: Transformation(DIRECTION_LEFT, 0, 3),
    },
]

DIRECTION_ROTATE_LEFT = {
    DIRECTION_UP: DIRECTION_LEFT,
    DIRECTION_RIGHT: DIRECTION_UP,
    DIRECTION_DOWN: DIRECTION_RIGHT,
    DIRECTION_LEFT: DIRECTION_DOWN,
}

DIRECTION_ROTATE_RIGHT = {
    DIRECTION_UP: DIRECTION_RIGHT,
    DIRECTION_RIGHT: DIRECTION_DOWN,
    DIRECTION_DOWN: DIRECTION_LEFT,
    DIRECTION_LEFT: DIRECTION_UP,
}

DIRECTION_TO_FACING_INT = {
    DIRECTION_UP: 3,
    DIRECTION_RIGHT: 0,
    DIRECTION_DOWN: 1,
    DIRECTION_LEFT: 2,
}

DIRECTION_TO_CHAR = {
    DIRECTION_UP: "^",
    DIRECTION_RIGHT: ">",
    DIRECTION_DOWN: "v",
    DIRECTION_LEFT: "<",
}

TEMPLATE: list[list[Optional[int]]] = [
    [None, 0, 1],
    [None, 2],
    [3, 4],
    [5],
]

COLORS = [
    Back.RED,
    Back.MAGENTA,
    Back.YELLOW,
    Back.CYAN,
    Back.GREEN,
    Back.BLUE,
]


def print_board(
    template: list[list[Optional[int]]],
    faces: list[list[str]],
    pos: Position3,
    direction: Direction,
) -> None:
    size = len(faces[0])
    empty = " " * size
    output: list[str] = []
    for template_row in template:
        for row_idx in range(size):
            for face_id in template_row:
                if face_id is None:
                    output.append(f"{Style.RESET_ALL}{empty}")
                else:
                    if pos.face == face_id and pos.row == row_idx:
                        output.append(
                            f"{COLORS[face_id]}{faces[face_id][row_idx][:pos.col]}{Back.BLACK}{DIRECTION_TO_CHAR[direction]}{COLORS[face_id]}{faces[face_id][row_idx][pos.col+1:]}"
                        )
                    else:
                        output.append(f"{COLORS[face_id]}{faces[face_id][row_idx]}")
            output.append(f"{Style.RESET_ALL}\n")

    print("".join(output))


def process_instruction(
    instruction: Instruction,
    faces: list[list[str]],
    position: Position3,
    direction: Direction,
    size: int,
) -> tuple[Position3, Direction]:
    if instruction == "L":
        direction = DIRECTION_ROTATE_LEFT[direction]
    elif instruction == "R":
        direction = DIRECTION_ROTATE_RIGHT[direction]
    else:
        for _ in range(instruction):
            npos = Position3(
                position.face,
                position.row + direction.dr,
                position.col + direction.dc,
            )
            ndir = direction
            if npos.row < 0 or npos.row >= size or npos.col < 0 or npos.col >= size:
                transformation = TRANSFORMATIONS[position.face][direction]
                assert transformation is not None
                shifted = transform_shift(
                    direction, Position2(position.row, position.col), size
                )
                rotated = transform_rotate(
                    transformation.clockwise_rotations, shifted, size
                )
                ndir = direction
                for _ in range(transformation.clockwise_rotations):
                    ndir = DIRECTION_ROTATE_RIGHT[ndir]
                npos = Position3(
                    transformation.destination_face, rotated.row, rotated.col
                )

            if faces[npos.face][npos.row][npos.col] == "#":
                break

            position = npos
            direction = ndir

    return position, direction


def position3_to_absolute_position2(pos3: Position3, size: int) -> Position2:
    for template_row_idx, template_row in enumerate(TEMPLATE):
        for template_col_idx, face_id in enumerate(template_row):
            if face_id == pos3.face:
                return Position2(
                    pos3.row + template_row_idx * size,
                    pos3.col + template_col_idx * size,
                )

    raise ValueError("pos3 face id does not exist in TEMPLATE")


def calculate_password(position: Position3, direction: Direction, size: int) -> int:
    absolute_position = position3_to_absolute_position2(position, size)
    row = absolute_position.row + 1
    col = absolute_position.col + 1

    password = 1000 * row + 4 * col + DIRECTION_TO_FACING_INT[direction]

    return password


def solve(text: str, size: int = 50, test_size: Optional[int] = None):
    real_size = size
    if test_size is not None:
        size = test_size
    map_lines, instructions = parse_input(text)

    faces = extract_faces(map_lines, real_size, test_size)

    assert len(faces) == 6

    position = Position3(0, 0, 0)
    direction = DIRECTION_RIGHT

    # print_board(TEMPLATE, faces, position, direction)

    for instruction in instructions:
        position, direction = process_instruction(
            instruction, faces, position, direction, size
        )

    password = calculate_password(position, direction, size)

    return password


def main():
    colorama_init()
    text = get_input()
    result = solve(text, 50)

    print(f"{result = }")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
