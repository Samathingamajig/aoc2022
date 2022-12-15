import os
import math
import pprint
import itertools
import re
import tqdm
import numpy as np


def distance(x1, y1, x2, y2) -> tuple[int, int]:
    return abs(x2 - x1) + abs(y2 - y1)


def det(a, b):
    if isinstance(a, complex):
        return det((a.real, a.imag), b)
    if isinstance(b, complex):
        return det(a, (b.real, b.imag))
    return a[0] * b[1] - a[1] * b[0]


def line_intersection(
    line1: tuple[complex, complex], line2: tuple[complex, complex]
) -> complex:
    xdiff = (line1[0].real - line1[1].real, line2[0].real - line2[1].real)
    ydiff = (line1[0].imag - line1[1].imag, line2[0].imag - line2[1].imag)

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x + y * 1j


# def in_bounds(search_space: int, position: complex) -> bool:


def solution(input: str, search_space: int) -> None:
    positions_list = [
        tuple(map(int, re.findall("(-?\d+)", line))) for line in input.split("\n")
    ]
    # sensor_beacon = {a + b * 1j: c + d * 1j for a, b, c, d in positions_list}
    sensor_distance = {
        a + b * 1j: distance(a, b, c, d) for a, b, c, d in positions_list
    }
    # pprint.pprint(sensor_beacon)
    # pprint.pprint(sensor_distance)
    min_x = int(min(sensor.real - dist for sensor, dist in sensor_distance.items()))
    max_x = int(max(sensor.real + dist for sensor, dist in sensor_distance.items()))

    positive_slope_lines = []
    negative_slope_lines = []
    edges: set[complex] = set()
    intersections: set[complex] = set()

    # for sensor, dist in tqdm.tqdm(sensor_distance.items()):
    #     top, bottom = map(int, (sensor.imag - dist, sensor.imag + dist))
    #     left, right = map(int, (sensor.real - dist, sensor.real + dist))

    #     top = max(-1, top)
    #     left = max(-1, left)
    #     bottom = min(search_space + 1, bottom)
    #     right = min(search_space + 1, right)

    for sensor, dist in sensor_distance.items():
        top, bottom = sensor - dist * 1j, sensor + dist * 1j
        left, right = sensor - dist, sensor + dist
        # if sensor == 8 + 7j:
        # print(top, left, bottom, right)
        positive_slope_lines += [(left, top), (bottom, right)]
        negative_slope_lines += [(left, bottom), (top, right)]

    for pos, neg in itertools.product(positive_slope_lines, negative_slope_lines):
        isect = line_intersection(pos, neg)
        if (
            -1 <= isect.real <= search_space + 1
            and -1 <= isect.imag <= search_space + 1
            and int(isect.real) == isect.real
            and int(isect.imag) == isect.imag
        ):
            intersections.add(isect)
        pass

    whole_points: set[complex] = set()

    for isect in intersections:
        # if (
        #     isect + 1 + 1j in intersections
        #     and isect + 2 in intersections
        #     and isect + 1 - 1j in intersections
        # ):
        #     # print(isect + 1)
        #     whole_points.add(isect + 1)

        # if (
        #     isect + 1 + 1j in intersections
        #     and isect + 2j in intersections
        #     and isect - 1 + 1j in intersections
        # ):
        #     # print(isect + 1j)
        #     whole_points.add(isect + 1j)
        # if (
        #     isect - 1 - 1j in intersections
        #     and isect - 2 in intersections
        #     and isect - 1 + 1j in intersections
        # ):
        #     # print(isect - 1)
        #     whole_points.add(isect - 1)
        # if (
        #     isect - 1 - 1j in intersections
        #     and isect - 2j in intersections
        #     and isect + 1 - 1j in intersections
        # ):
        #     # print(isect - 1j)
        #     whole_points.add(isect - 1j)
        whole_points.add(isect + 1)
        whole_points.add(isect - 1)
        whole_points.add(isect + 1j)
        whole_points.add(isect - 1j)

    answer = None

    for point in whole_points:
        if 0 <= point.real <= search_space and -1 <= point.imag <= search_space + 1:
            for sensor, dist in sensor_distance.items():
                if distance(point.real, point.imag, sensor.real, sensor.imag) <= dist:
                    break
            else:
                answer = point
                break

    # pprint.pprint(positive_slope_lines)
    # print()
    # print()
    # pprint.pprint(negative_slope_lines)
    # pprint.pprint(intersections)
    print(len(intersections))
    print(answer)
    print(int(4_000_000 * answer.real + answer.imag))
    # print(sum(sensor_distance.values()))
    # print()
    # print(len(positive_slope_lines))

    # print(min_x, max_x)
    pass


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test, search_space=20)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input, search_space=4_000_000)


if __name__ == "__main__":
    main()

"""
               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################...e.....
 7 .#########9##F####5#.e#.....
 8 ..############F####.e.#.....
 9 ...############F###e..#.....
10 ....B#########f#F#e...#.....
11 ..S.###########f.G....#.....
12 ....############g#F...#.....
13 ....#############f....#.....
14 ....##########4####...8.....
15 B...##############..........
16 ....#######SB####...........
17 ....#######..###S..........B
18 ....S#######..#.............
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

e + f = g
e + F = G
"""
