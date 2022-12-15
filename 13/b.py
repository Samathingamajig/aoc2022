import os
import math
import pprint
import functools


def compare(left, right) -> int:
    # print("compare: " + str(left) + " | " + str(right))
    if len(left) == 0 and len(right) == 0:
        return 0
    if len(left) == 0:
        return 1
    if len(right) == 0:
        return -1

    l, r = left[0], right[0]

    if isinstance(l, int) and isinstance(r, int):
        # print("  int compare: " + str(l) + " | " + str(r))
        if l < r:
            return 1
        if l > r:
            return -1
    elif isinstance(l, list) and isinstance(r, list):
        # print("  list compare: " + str(l) + " | " + str(r))
        c = compare(l, r)
        if c == -1:
            return -1
        if c == 1:
            return 1
    elif not isinstance(l, list):
        # print("  list compare: [" + str(l) + "] | " + str(r))
        c = compare([l], r)
        if c == -1:
            return -1
        if c == 1:
            return 1
    else:
        # print("  list compare: " + str(l) + " | [" + str(r) + "]")
        c = compare(l, [r])
        if c == -1:
            return -1
        if c == 1:
            return 1

    return compare(left[1:], right[1:])


def solution(input: str) -> None:
    # pairs = [[eval(side) for side in pair.split("\n")] for pair in input.split("\n\n")]
    lists = [eval(l) for l in input.split("\n") if len(l) > 0]
    lists.append([[6]])
    lists.append([[2]])
    print("\n".join(str(l) for l in lists))

    # rights = []
    # for i, [left, right] in enumerate(pairs, start=1):
    #     print(i)
    #     # if i != 3:
    #     #     continue
    #     c = compare(left, right)
    #     if c == 1 or c == 0:
    #         rights.append(i)
    #     print(i, c)
    #     print()
    #     print()

    sort = list(sorted(lists, key=functools.cmp_to_key(lambda a, b: compare(b, a))))
    print(sort)
    idx1 = sort.index([[2]]) + 1
    idx2 = sort.index([[6]]) + 1
    print((idx1) * idx2)

    # print(rights)
    # print(sum(rights))
    # # print("l", len(pairs))

    # pprint.pprint(pairs)

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
