import os
import math
import pprint
import itertools


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def solution(input: str) -> None:
    paths = [
        # (int(a), int(b))
        [[int(a) for a in point.split(",")] for point in p.split(" -> ")]
        for p in input.split("\n")
        # for a, b in point.split(",")
    ]
    # paths = [(int(a), int(b)) for a, b in paths.]
    # pprint.pprint(paths, indent=2, width=20)
    min_x = min(min(point[0] for p in paths for point in p), 500)
    max_x = max(point[0] for p in paths for point in p)
    max_y = max(point[1] for p in paths for point in p)
    print(min_x, max_x, max_y)
    grid = [["." for x in range(max_x - min_x + 1)] for y in range(max_y + 1)]
    paths = [
        # (int(a), int(b))
        [(x - min_x, y) for x, y in p]
        for p in paths
        # for a, b in point.split(",")
    ]

    for path in paths:
        for (x1, y1), (x2, y2) in window(path, n=2):
            # print(x1, y1, x2, y2)

            if x1 != x2:
                x1, x2 = min(x1, x2), max(x1, x2)
                print(y1, x1, x2)
                grid[y1][x1 : x2 + 1] = ["#"] * (x2 - x1 + 1)
            else:
                y1, y2 = min(y1, y2), max(y1, y2)
                for i in range(y1, y2 + 1):
                    grid[i][x1] = "#"

    # x, y = 500 - min_x, 0
    grid[0][500 - min_x] = "x"

    print("\n".join("".join(row) for row in grid))
    print("\n\n")

    sand_count = 0
    try:
        while True:
            sand_count += 1

            x, y = 500 - min_x, 0
            # print("outer")
            while True:
                # print(sand_count, (y, x), grid[y + 1][x])
                # print(grid[y + 1])
                if grid[y + 1][x] == ".":
                    y += 1
                    # print("down")
                    continue
                elif grid[y + 1][x - 1] == ".":
                    y += 1
                    x -= 1
                    # print("down  left")
                    continue
                elif grid[y + 1][x + 1] == ".":
                    y += 1
                    x += 1
                    # print("down right")
                    continue
                else:
                    grid[y][x] = "o"
                    break
            # if sand_count > 20:
            # break
            # print(sand_count)
    except IndexError:
        pass

    # pprint.pprint(grid)
    print("\n".join("".join(row) for row in grid))
    print(sand_count - 1)
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
