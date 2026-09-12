from dataclasses import dataclass
from b_attempt_3 import transform_rotate, Position2


@dataclass
class TestResult:
    successes: int
    failures: int


def test_transform_rotate() -> TestResult:
    table: list[tuple[tuple[int, Position2, int], Position2]] = [
        # 0
        ((0, Position2(0, 0), 5), Position2(0, 0)),
        ((0, Position2(0, 1), 5), Position2(0, 1)),
        ((0, Position2(0, 2), 5), Position2(0, 2)),
        ((0, Position2(0, 3), 5), Position2(0, 3)),
        # 1
        ((1, Position2(0, 0), 5), Position2(0, 4)),
        ((1, Position2(0, 1), 5), Position2(1, 4)),
        ((1, Position2(0, 2), 5), Position2(2, 4)),
        ((1, Position2(0, 3), 5), Position2(3, 4)),
        # 2
        ((2, Position2(0, 0), 5), Position2(4, 4)),
        ((2, Position2(0, 1), 5), Position2(4, 3)),
        ((2, Position2(0, 2), 5), Position2(4, 2)),
        ((2, Position2(0, 3), 5), Position2(4, 1)),
        # 3
        ((3, Position2(0, 0), 5), Position2(4, 0)),
        ((3, Position2(0, 1), 5), Position2(3, 0)),
        ((3, Position2(0, 2), 5), Position2(2, 0)),
        ((3, Position2(0, 3), 5), Position2(1, 0)),
        # 4
        ((4, Position2(0, 0), 5), Position2(0, 0)),
        ((4, Position2(0, 1), 5), Position2(0, 1)),
        ((4, Position2(0, 2), 5), Position2(0, 2)),
        ((4, Position2(0, 3), 5), Position2(0, 3)),
    ]

    test_result = TestResult(0, 0)
    for params, expected_result in table:
        result = transform_rotate(*params)
        if result == expected_result:
            test_result.successes += 1
        else:
            test_result.failures += 1

    return test_result


def main() -> int:
    results_raw: list[TestResult] = [test_transform_rotate()]

    total_successes = 0
    total_failures = 0
    for result in results_raw:
        total_successes += result.successes
        total_failures += result.failures

    print(f"Summary: {total_successes = }, {total_failures = }")

    return total_failures != 0  # returning 0 is success


if __name__ == "__main__":
    raise SystemExit(main())
