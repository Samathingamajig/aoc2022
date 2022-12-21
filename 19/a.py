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
import time


@dataclasses.dataclass
class Blueprint:
    ident: int
    ore_cost_ore: int
    clay_cost_ore: int
    obsidian_cost_ore: int
    obsidian_cost_clay: int
    geode_cost_ore: int
    geode_cost_obsidian: int

    def __hash__(self) -> int:
        return self.ident


@dataclasses.dataclass
class Data:
    time_remaining: int
    ore: int
    ore_robots: int
    clay: int
    clay_robots: int
    obsidian: int
    obsidian_robots: int
    geode: int
    geode_robots: int
    log: list[Purchase]

    def sash(self) -> tuple:
        return (
            self.ore,
            self.ore_robots,
            self.clay,
            self.clay_robots,
            self.obsidian,
            self.obsidian_robots,
            self.geode,
            self.geode_robots,
        )

    def sash_no_geode(self) -> tuple:
        return (
            self.ore,
            self.ore_robots,
            self.clay,
            self.clay_robots,
            self.obsidian,
            self.obsidian_robots,
            self.geode_robots,
        )


@dataclasses.dataclass()
class Purchase:
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int

    def __str__(self):
        if self.ore_robots > 0:
            return f"ore"
        if self.clay_robots > 0:
            return f"clay"
        if self.obsidian_robots > 0:
            return f"obsidian"
        if self.geode_robots > 0:
            return f"geode"
        return f"nothing"

    def __hash__(self) -> int:
        return hash(
            (self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots)
        )


# @functools.cache
# def possibilities(
#     ore: int, clay: int, obsidian: int, blueprint: Blueprint, first: bool = False
# ) -> set[Purchase]:
#     t = time.time()
#     output = set()
#     if ore >= blueprint.ore_cost_ore:
#         options = possibilities(ore - blueprint.ore_cost_ore, clay, obsidian, blueprint)
#         for option in options:
#             output.add(
#                 Purchase(
#                     option.ore_robots + 1,
#                     option.clay_robots,
#                     option.obsidian_robots,
#                     option.geode_robots,
#                 )
#             )
#     if ore >= blueprint.clay_cost_ore:
#         options = possibilities(
#             ore - blueprint.clay_cost_ore, clay, obsidian, blueprint
#         )
#         for option in options:
#             output.add(
#                 Purchase(
#                     option.ore_robots,
#                     option.clay_robots + 1,
#                     option.obsidian_robots,
#                     option.geode_robots,
#                 )
#             )
#     if ore >= blueprint.obsidian_cost_ore and clay >= blueprint.obsidian_cost_clay:
#         options = possibilities(
#             ore - blueprint.obsidian_cost_ore,
#             clay - blueprint.obsidian_cost_clay,
#             obsidian,
#             blueprint,
#         )
#         for option in options:
#             output.add(
#                 Purchase(
#                     option.ore_robots,
#                     option.clay_robots,
#                     option.obsidian_robots + 1,
#                     option.geode_robots,
#                 )
#             )
#     if ore >= blueprint.geode_cost_ore and obsidian >= blueprint.geode_cost_obsidian:
#         options = possibilities(
#             ore - blueprint.geode_cost_ore,
#             clay,
#             obsidian - blueprint.geode_cost_obsidian,
#             blueprint,
#         )
#         for option in options:
#             output.add(
#                 Purchase(
#                     option.ore_robots,
#                     option.clay_robots,
#                     option.obsidian_robots,
#                     option.geode_robots + 1,
#                 )
#             )
#     # if len(output) == 0 or first:
#     output.add(Purchase(0, 0, 0, 0))
#     if first:
#         # print(time.time() - t)
#         pass
#     return output


def possibilities(
    data: Data, blueprint: Blueprint, first: bool = False
) -> set[Purchase]:
    t = time.time()
    output = set()
    # print("ore", data.ore)
    # print("clay", data.clay)
    # print("obsidian", data.obsidian)
    # print("geode", data.geode)
    # print()
    if data.ore >= blueprint.ore_cost_ore:
        output.add(Purchase(1, 0, 0, 0))
    if data.ore >= blueprint.clay_cost_ore:
        output.add(Purchase(0, 1, 0, 0))
    if (
        data.ore >= blueprint.obsidian_cost_ore
        and data.clay >= blueprint.obsidian_cost_clay
    ):
        output.add(Purchase(0, 0, 1, 0))
    if (
        data.ore >= blueprint.geode_cost_ore
        and data.obsidian >= blueprint.geode_cost_obsidian
    ):
        output.add(Purchase(0, 0, 0, 1))
    output.add(Purchase(0, 0, 0, 0))
    if first:
        # print(time.time() - t)
        pass
    # print(len(output))
    return output


def calc_score(blueprint: Blueprint, initial_data: Data) -> int:

    # pprint.pprint(initial_data)
    queue: collections.deque[Data] = collections.deque()
    next_queue: collections.deque[Data] = collections.deque()
    queue.append(dataclasses.replace(initial_data))

    best_geodes = -1
    best_log = []
    # best_path = []
    count = 0

    # position_time_score: dict[str, dict[int, int]] = {}

    max_cost_ore = max(
        blueprint.ore_cost_ore,
        blueprint.clay_cost_ore,
        blueprint.obsidian_cost_ore,
        blueprint.geode_cost_ore,
    )

    max_other_cost_ore = max(
        blueprint.ore_cost_ore,
        blueprint.clay_cost_ore,
    )

    all_same_best_day: dict[tuple, int] = {}
    all_others_same_best_geodes: dict[tuple, int] = {}

    for day in range(1, 2):
        while len(queue):
            current_data = queue.pop()
            count += 1

            current_data.time_remaining -= 1
            # input()
            # print(current_data.time_remaining, current_data.geode)
            if (
                all_same_best_day.get(current_data.sash(), -1)
                >= current_data.time_remaining
            ):
                continue
            all_same_best_day[current_data.sash()] = current_data.time_remaining

            # if (
            #     all_others_same_best_geodes.get(current_data.sash_no_geode(), -1)
            #     >= current_data.geode
            #     + current_data.time_remaining * current_data.geode_robots
            # ):
            #     continue
            # all_others_same_best_geodes[current_data.sash_no_geode()] = (
            #     current_data.geode
            #     + current_data.time_remaining * current_data.geode_robots
            # )

            if current_data.time_remaining <= 0:
                p = best_geodes
                best_geodes = max(best_geodes, current_data.geode)
                if p < best_geodes:
                    # print("\33[2K\r" + str(best_score), end="")
                    print("best", best_geodes)
                    best_log = current_data.log
                # print(best_score, best_path)
                # else:
                #     print(" ", current_data.running_score, current_data.path)
                continue

            # print(
            #     current_data.time_remaining,
            #     current_data.ore,
            #     current_data.clay,
            #     current_data.obsidian,
            #     current_data.geode,
            #     current_data.ore_robots,
            #     current_data.clay_robots,
            #     current_data.obsidian_robots,
            #     current_data.geode_robots,
            # )
            # input()

            # added = []
            enqueued = False
            for purchase in possibilities(current_data, blueprint, True):
                # print(current_data, purchase)
                new_data = dataclasses.replace(current_data)
                new_data.ore_robots += purchase.ore_robots
                new_data.clay_robots += purchase.clay_robots
                new_data.obsidian_robots += purchase.obsidian_robots
                new_data.geode_robots += purchase.geode_robots

                new_data.ore -= (
                    purchase.ore_robots * blueprint.ore_cost_ore
                    + purchase.clay_robots * blueprint.clay_cost_ore
                    + purchase.obsidian_robots * blueprint.obsidian_cost_ore
                    + purchase.geode_robots * blueprint.geode_cost_ore
                )
                new_data.clay -= purchase.obsidian_robots * blueprint.obsidian_cost_clay
                new_data.obsidian -= (
                    purchase.geode_robots * blueprint.geode_cost_obsidian
                )

                if (
                    new_data.ore_robots > max_cost_ore
                    or new_data.clay_robots > blueprint.obsidian_cost_clay
                    or new_data.obsidian_robots > blueprint.geode_cost_obsidian
                ):
                    continue

                if (
                    new_data.ore >= max_other_cost_ore
                    and (
                        new_data.ore >= blueprint.obsidian_cost_ore
                        and new_data.clay >= blueprint.obsidian_cost_clay
                    )
                    and (
                        new_data.ore >= blueprint.geode_cost_ore
                        and new_data.obsidian >= blueprint.geode_cost_obsidian
                    )
                ):
                    # print("passed")
                    continue

                new_data.ore += current_data.ore_robots
                new_data.clay += current_data.clay_robots
                new_data.obsidian += current_data.obsidian_robots
                new_data.geode += current_data.geode_robots

                new_data.log = current_data.log + [
                    current_data.time_remaining,
                    current_data.sash(),
                ]
                if purchase != Purchase(0, 0, 0, 0):
                    new_data.log.append(purchase)
                enqueued = True
                queue.append(new_data)
                # added += [purchase]
            if not enqueued:
                p = best_geodes
                best_geodes = max(best_geodes, current_data.geode)
                if p < best_geodes:
                    # print("\33[2K\r" + str(best_score), end="")
                    print("best", best_geodes)
                    best_log = current_data.log
                # print(best_score, best_path)
                # else:
                #     print(" ", current_data.running_score, current_data.path)
                continue
            # pprint.pprint(added)
            # print(added)
        # queue, next_queue = next_queue, queue
        print("next queue len", len(queue))

    print(count)

    print(best_log)

    return best_geodes


def solution(inp: str) -> None:
    blueprints_dict: dict[str, Blueprint] = {}

    for group in inp.split("\n"):
        parts = group.split(".")
        ident = int(parts[0].split("Blueprint ")[1].split(":")[0])
        ore_cost = int(parts[0].split(" costs ")[1].split(" ")[0])
        clay_cost = int(parts[1].split(" costs ")[1].split(" ")[0])
        obsidian_cost = int(parts[2].split(" costs ")[1].split(" ")[0])
        obsidian_cost_clay = int(parts[2].split(" costs ")[1].split(" ")[3])
        geode_cost = int(parts[3].split(" costs ")[1].split(" ")[0])
        geode_cost_obsidian = int(parts[3].split(" costs ")[1].split(" ")[3])
        blueprints_dict[ident] = Blueprint(
            ident,
            ore_cost,
            clay_cost,
            obsidian_cost,
            obsidian_cost_clay,
            geode_cost,
            geode_cost_obsidian,
        )

    # pprint.pprint(blueprints_dict)

    initial_data = Data(25, 0, 1, 0, 0, 0, 0, 0, 0, [])

    quality_level_total = 0

    # pprint.pprint(possibilities(12, 10, 0, list(blueprints_dict.values())[1]))

    for blueprint in blueprints_dict.values():
        # if blueprint.ident != 1:
        #     continue
        score = calc_score(blueprint, initial_data)
        print(score)
        quality_level_total += score * blueprint.ident

    print(quality_level_total)

    return

    # print()
    print(best_score)
    # print(best_path)


def main():
    # with open(os.path.join(os.path.dirname(__file__), "test.txt"), "r") as input_file:
    #     test = input_file.read().rstrip()
    #     solution(test)
    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as input_file:
        input = input_file.read().rstrip()
        solution(input)


if __name__ == "__main__":
    main()
