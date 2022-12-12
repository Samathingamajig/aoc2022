import os
import math
import pprint


def solution(input: str) -> None:
    print(input)
    rows = input.split("\n")
    num_rows = len(rows)
    num_cols = len(rows[0])
    # start = input.replace("\n", "").index("S")
    # start_row = start // num_cols
    # start_col = start % num_cols

    end = input.replace("\n", "").index("E")
    end_row = end // num_cols
    end_col = end % num_cols
    # print(end_row, end_col)

    rows = [row.replace("S", "a").replace("E", "z") for row in rows]

    cons = {}
    for i in range(0, num_rows * num_cols):
        cons[(i // num_cols, i % num_cols)] = {}
    # pprint.pprint(cons)
    # for A, B, T in connections:
    #     cons[A][B] = T
    #     cons[B][A] = T
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if i > 0:
                up = rows[i - 1][j]
                if (
                    ord(up) - ord(char)
                    <= 1
                    # or (i == start_row and j == start_col)
                    # or (i - 1 == end_row and j == end_col)
                ):
                    cons[(i - 1, j)][(i, j)] = 1
            if i < len(rows) - 1:
                down = rows[i + 1][j]
                if (
                    ord(down) - ord(char)
                    <= 1
                    # or (i == start_row and j == start_col)
                    # or (i + 1 == end_row and j == end_col)
                ):
                    cons[(i + 1, j)][(i, j)] = 1
            if j > 0:
                left = rows[i][j - 1]
                if (
                    ord(left) - ord(char)
                    <= 1
                    # or (i == start_row and j == start_col)
                    # or (i == end_row and j - 1 == end_col)
                ):
                    cons[(i, j - 1)][(i, j)] = 1
            if j < len(row) - 1:
                right = rows[i][j + 1]
                if (
                    ord(right) - ord(char)
                    <= 1
                    # or (i == start_row and j == start_col)
                    # or (i == end_row and j + 1 == end_col)
                ):
                    cons[(i, j + 1)][(i, j)] = 1
    # pprint.pprint(cons)
    # return
    # Dijkstra's algorithm
    distances = {}
    for i in range(0, num_rows * num_cols):
        distances[(i // num_cols, i % num_cols)] = math.inf
    distances[(end_row, end_col)] = 0
    unvisited_touched_nodes = [(end_row, end_col)]
    visited_nodes = set()

    while len(unvisited_touched_nodes) > 0:
        node = unvisited_touched_nodes[0]
        del unvisited_touched_nodes[0]
        visited_nodes.add(node)
        # print(node)
        for next_node in cons[node]:
            cost = cons[node][next_node]
            # print(next_node, node, cost)
            distances[next_node] = min(distances[next_node], distances[node] + cost)
            if (next_node not in visited_nodes) and (
                next_node not in unvisited_touched_nodes
            ):
                unvisited_touched_nodes.append(next_node)

    # print(distances)
    print(distances[(end_row, end_col)])
    valid = []
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char == "a":
                valid.append(distances[(i, j)])
    print(min(valid))
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
