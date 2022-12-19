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


@dataclasses.dataclass
class Valve:
    name: str
    rate: int
    neighbors: list[str]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


@dataclasses.dataclass
class Data:
    running_score: int
    time_remaining: int
    open_valves: int  # bitmap
    current_valve: Valve
    unopened_path: set[str]
    path: list[str]


def solution(inp: str) -> None:
    valves_dict: dict[str, Valve] = {}

    for line in inp.split("\n"):
        name = line[6:8]
        rate = int(re.findall("(-?\d+)", line)[0])
        neighbors = re.split("valves? ", line)[1].split(", ")
        valves_dict[name] = Valve(name, rate, neighbors)

    valves_index_bitmap = {valve: (1 << i) for i, valve in enumerate(valves_dict)}

    all_valves_open = 0
    for v in valves_dict.values():
        if v.rate > 0:
            all_valves_open += valves_index_bitmap[v.name]

    valve_valve_cost: dict[str, dict[str, int]] = {}

    for valve in valves_dict.values():
        valve_valve_cost[valve.name] = {}
        for other in valves_dict:
            valve_valve_cost[valve.name][other] = math.inf
        valve_valve_cost[valve.name][valve.name] = 0
        unvisited_touched_nodes = [valve.name]
        visited_nodes = set()

        while len(unvisited_touched_nodes) > 0:
            node = unvisited_touched_nodes[0]
            del unvisited_touched_nodes[0]
            visited_nodes.add(node)
            # print(node)
            for next_node in valves_dict[node].neighbors:
                cost = 1
                # print(next_node, node, cost)
                # print(valve_valve_cost[valve.name])
                valve_valve_cost[valve.name][next_node] = min(
                    valve_valve_cost[valve.name][next_node],
                    valve_valve_cost[valve.name][node] + cost,
                )
                if (next_node not in visited_nodes) and (
                    next_node not in unvisited_touched_nodes
                ):
                    unvisited_touched_nodes.append(next_node)
    print(valve_valve_cost)

    queue: collections.deque[Data] = collections.deque()
    queue.append(Data(0, 30, 0, valves_dict["AA"], set(), []))
    queue.append(
        Data(
            valves_dict["AA"].rate * 29,
            29,
            valves_index_bitmap["AA"],
            valves_dict["AA"],
            set(),
            [],
        )
    )

    best_score = -1
    best_path = []
    count = 0
    # score = 0
    # visited_nodes = 0
    # time_remaining = 30
    # current_valve = "AA"
    # while time_remaining > 0:
    #     best_next_valve = None
    #     best_cost_score_ratio = 0
    #     for v in valves_dict:
    #         if valves_dict[v].rate == 0 or valves_index_bitmap[v] & visited_nodes:
    #             continue
    #         v = valves_dict[v]
    #         temp_score = v.rate * (time_remaining - valve_valve_cost[current_valve][v.name] - 1)

    # score += valves_dict[valve].rate * time_remaining
    # time_remaining -= 1
    # visited_nodes += 1
    while len(queue):
        current_data = queue.pop()
        # count += 1
        # print(count)
        # print(current_data)
        # if count > 10:
        #     break
        # print()
        # print(
        #     "!! at "
        #     + current_data.current_valve.name
        #     + " with "
        #     + str(current_data.time_remaining)
        #     + " time left and "
        #     + str(current_data.running_score)
        #     + " pressure released"
        # )
        # print()
        if (
            current_data.time_remaining <= 0
            or current_data.open_valves == all_valves_open
        ):
            p = best_score
            best_score = max(best_score, current_data.running_score)
            if p < best_score:
                best_path = current_data.path
                # print("\33[2K\r" + str(best_score), end="")
                # best_path = current_data.path
                print(best_score, best_path)
            # else:
            #     print(" ", current_data.running_score, current_data.path)
            continue

        enqueued = False
        for valve in valves_dict:
            # input()
            # print("considering " + valve)
            # print("opened: ", valves_index_bitmap[valve] & current_data.open_valves)
            # print("current: ", valve == current_data.current_valve.name)
            if (
                valves_index_bitmap[valve] & current_data.open_valves
                or valve == current_data.current_valve.name
            ):
                continue
            cost = valve_valve_cost[current_data.current_valve.name][valve]
            # print("cost: ", cost)
            # print("possible: ", cost < current_data.time_remaining)
            if cost >= current_data.time_remaining:
                continue
            # print(
            #     "rate: ",
            #     valves_dict[valve].rate,
            #     "worthless: ",
            #     valves_dict[valve].rate == 0,
            # )
            # if (
            #     valves_dict[valve].rate
            #     == 0
            #     # and valve != current_data.current_valve.name
            # ):
            #     # print(valve)
            #     continue

            data = dataclasses.replace(current_data)

            data.time_remaining = current_data.time_remaining - cost - 1
            data.running_score = (
                current_data.running_score
                + max(data.time_remaining, 0) * valves_dict[valve].rate
            )
            if data.running_score == current_data.running_score:
                continue
            # print("same")
            data.open_valves += valves_index_bitmap[valve]
            data.current_valve = valves_dict[valve]
            data.path = data.path + [valve, data.time_remaining]
            # print("")
            queue.append(data)
            enqueued = True
        if not enqueued:
            p = best_score
            best_score = max(best_score, current_data.running_score)
            if p < best_score:
                best_path = current_data.path
                # print("\33[2K\r" + str(best_score), end="")
                # best_path = current_data.path
                print(best_score, best_path)
            # else:
            #     print(" ", current_data.running_score, current_data.path)
            continue
    print()
    print(best_score)
    print(best_path)


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)


if __name__ == "__main__":
    main()
