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
    times_remaining: list[int, int]  # (me, elephant)
    open_valves: int  # bitmap
    current_valves: list[Valve, Valve]
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
            for next_node in valves_dict[node].neighbors:
                cost = 1
                valve_valve_cost[valve.name][next_node] = min(
                    valve_valve_cost[valve.name][next_node],
                    valve_valve_cost[valve.name][node] + cost,
                )
                if (next_node not in visited_nodes) and (
                    next_node not in unvisited_touched_nodes
                ):
                    unvisited_touched_nodes.append(next_node)
    print(valve_valve_cost)

    original_time = 26
    queue: collections.deque[Data] = collections.deque()
    queue.append(
        Data(
            0,
            [original_time, original_time],
            0,
            [valves_dict["AA"], valves_dict["AA"]],
            [],
        )
    )
    queue.append(
        Data(
            valves_dict["AA"].rate * (original_time - 1),
            [original_time - 1, original_time],
            valves_index_bitmap["AA"],
            [valves_dict["AA"], valves_dict["AA"]],
            [],
        )
    )

    best_score = -1
    best_path = []
    count = 0

    position_time_score: dict[tuple[str, str], dict[tuple[int, int], int]] = {}

    while len(queue):
        count += 1
        current_data = queue.pop()
        if (
            max(current_data.times_remaining) <= 0
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

        navigator = (
            0
            if current_data.times_remaining[0] >= current_data.times_remaining[1]
            else 1
        )
        enqueued = False
        for valve in valves_dict:
            if (
                valves_index_bitmap[valve] & current_data.open_valves
                or valve == current_data.current_valves[navigator].name
            ):
                # print("skip", valve)
                # print("open", current_data.open_valves)
                # print("current", current_data.current_valve.name == valve)
                continue
            cost = valve_valve_cost[current_data.current_valves[navigator].name][valve]
            if cost >= current_data.times_remaining[navigator]:
                continue

            data = dataclasses.replace(current_data)
            data.times_remaining = current_data.times_remaining.copy()
            data.times_remaining[navigator] = (
                current_data.times_remaining[navigator] - cost - 1
            )
            # print("time", data.time_remaining)
            data.running_score = (
                current_data.running_score
                + max(data.times_remaining[navigator], 0) * valves_dict[valve].rate
            )
            if data.running_score == current_data.running_score:
                # print("no score change")
                continue
            data.open_valves += valves_index_bitmap[valve]
            data.current_valves = current_data.current_valves.copy()
            data.current_valves[navigator] = valves_dict[valve]
            data.path = data.path + [valve, data.times_remaining]
            pos_names_sorted = tuple(sorted(data.current_valves, key=lambda x: x.name))
            times_remaining_sorted = tuple(sorted(data.times_remaining))
            if (
                position_time_score.get(pos_names_sorted) is not None
                and position_time_score[pos_names_sorted].get(times_remaining_sorted)
                is not None
                and position_time_score[pos_names_sorted][times_remaining_sorted]
                >= data.running_score
            ):
                continue
            position_time_score.setdefault(pos_names_sorted, {})
            position_time_score[pos_names_sorted][
                times_remaining_sorted
            ] = data.running_score

            queue.append(data)
            enqueued = True

        if not enqueued:
            p = best_score
            best_score = max(best_score, current_data.running_score)
            if p < best_score:
                best_path = current_data.path
                print(best_score, best_path)
            continue
    print()
    print(count)
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
