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
    open_valves: set[str]
    current_valve: Valve
    unopened_path: set[str]
    path: list[str]


def solution(input: str) -> None:
    valves_dict: dict[str, Valve] = {}

    for line in input.split("\n"):
        name = line[6:8]
        rate = int(re.findall("(-?\d+)", line)[0])
        neighbors = re.split("valves? ", line)[1].split(", ")
        valves_dict[name] = Valve(name, rate, neighbors)

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

    queue: collections.deque[Data] = collections.deque()
    queue.append(Data(0, 30, set(), valves_dict["AA"], set(), []))

    best_score = -1
    best_path = []
    count = 0
    while len(queue):
        current_data = queue.pop()
        # count += 1
        # print(count)
        # print(current_data)
        # if count > 10:
        #     break
        if current_data.time_remaining <= 0:
            p = best_score
            best_score = max(best_score, current_data.running_score)
            if p < best_score:
                print("\33[2K\r" + str(best_score), end="")
                best_path = current_data.path
            continue
        # if current_data.current_valve in current_data.unopened_path:
        #     continue
        # if_open: Data | None = None
        # print(current_data)
        # if current_data.current_valve.name not in current_data.open_valves:
        #     running_score = (
        #         current_data.running_score
        #         + max((current_data.time_remaining - 1), 0)
        #         * current_data.current_valve.rate
        #     )
        #     time_remaining = current_data.time_remaining - 1
        #     open_nodes = current_data.open_valves.copy()
        #     open_nodes.add(current_data.current_valve.name)
        #     if_open = Data(
        #         running_score,
        #         time_remaining,
        #         open_nodes,
        #         current_data.current_valve,
        #         set(),
        #         current_data.path + [f"open {current_data.current_valve}"],
        #     )
        for valve in valves_dict:
            if valve in current_data.open_valves:
                continue
            cost = valve_valve_cost[current_data.current_valve.name][valve]
            if cost >= current_data.time_remaining:
                continue

            data = dataclasses.replace(current_data)

            data.time_remaining = current_data.time_remaining - cost - 1
            data.running_score = (
                current_data.running_score
                + max(data.time_remaining, 0) * valves_dict[valve].rate
            )
            data.open_valves = current_data.open_valves.copy()
            data.open_valves.add(valve)
            data.current_valve = valves_dict[valve]
            data.path = data.path + [f"move {valve}", data.time_remaining]
            queue.append(data)

        # for neighbor_valve in current_data.current_valve.neighbors:
        #     if current_data.current_valve.name not in current_data.open_valves:
        #         data = dataclasses.replace(if_open)
        #         data.time_remaining -= 1
        #         data.current_valve = valves_dict[neighbor_valve]
        #         # data.path = data.path + [f"move {neighbor_valve}"]
        #         # print("  adding n_o", data)
        #         queue.append(data)

        #     if neighbor_valve not in current_data.unopened_path:
        #         data = dataclasses.replace(current_data)
        #         data.time_remaining -= 1
        #         data.current_valve = valves_dict[neighbor_valve]
        #         data.unopened_path = data.unopened_path.copy()
        #         data.unopened_path.add(neighbor_valve)
        #         # data.path = data.path + [f"move {neighbor_valve}", data.time_remaining]
        #         # print("  adding", data)
        #         queue.append(data)
        # else:
        #     print("hit")
    print()
    print(best_score)
    print(best_path)

    # if current cell not open
    # calculate score
    # create copy with current cell added to set of open
    # for each neighbor
    # if current cell not open
    # enqueue version with it open + score, moving to next node afterwards
    # enqueue a version going to next node


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)


if __name__ == "__main__":
    main()
