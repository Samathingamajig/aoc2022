import os
import math
import pprint
import itertools
import re


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def solution(input: str, y_level: int) -> None:
    pos = [tuple(map(int, re.findall("(-?\d+)", line))) for line in input.split("\n")]
    sensor_beacon = {a + b * 1j: c + d * 1j for a, b, c, d in pos}
    sensor_distance = {a + b * 1j: distance(a, b, c, d) for a, b, c, d in pos}
    # pprint.pprint(sensor_beacon)
    # pprint.pprint(sensor_distance)
    min_x = int(min(sensor.real - dist for sensor, dist in sensor_distance.items()))
    max_x = int(max(sensor.real + dist for sensor, dist in sensor_distance.items()))
    # min_x = int(
    #     min(min(sensor.real, beacon.real) for sensor, beacon in sensor_beacon.items())
    # )
    # max_x = int(
    #     max(max(sensor.real, beacon.real) for sensor, beacon in sensor_beacon.items())
    # )

    count = 0
    beacons = set(sensor_beacon.values())
    invalid = list(False for _ in range(min_x, max_x + 1))
    # for x in range(min_x, max_x + 1):
    #     if x % 10000 == 0:
    #         print(x)
    #     for sensor, dist in sensor_distance.items():
    #         if (
    #             x + y_level * 1j not in beacons
    #             and distance(x, y_level, sensor.real, sensor.imag) <= dist
    #         ):
    #             print(x)
    #             count += 1
    #             break
    for sensor, dist in sensor_distance.items():
        x = int(sensor.real) - min_x
        d = int(dist - abs(y_level - sensor.imag))
        # print("xd", sensor, dist, x, d)
        if d <= 0:
            continue
        # print("pass")
        # print("".join("X" if _ else "." for _ in invalid))
        left = max(0, x - d)
        right = min(max_x - min_x + 1, x + d + 1)
        # print("lr", left, right)
        invalid[left:right] = [True] * (right - left)
        # print("".join("X" if _ else "." for _ in invalid))

    for beacon in beacons:
        # print(beacon.imag)
        if int(beacon.imag) == y_level:
            invalid[int(beacon.real) + min_x] = False

    # print("".join("X" if _ else "." for _ in invalid))
    count = invalid.count(True)
    # print(min_x, max_x)
    # print(pos)
    # print(count, len(invalid))
    print(count)
    pass


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test, y_level=10)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input, y_level=2_000_000)


if __name__ == "__main__":
    main()
