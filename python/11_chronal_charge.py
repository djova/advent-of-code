#!/usr/bin/env python
import re

grid_width = 300


def point_power_level(x, y, grid_serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += grid_serial_number
    power_level *= rack_id
    power_level = power_level % 1000 / 100
    power_level -= 5
    return power_level


def test_power_level_calculations():
    test_examples = """
Fuel cell at 122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4.
"""

    for x, y, grid_serial_number, power_level in [[int(i) for i in re.findall(r'-?\d+', l)] for l in
                                                  test_examples.split('\n') if l]:
        _level = point_power_level(x, y, grid_serial_number)
        if _level != power_level:
            print "validation failed '({},{}), serial: {}', calculated power level {} != expected {}".format(
                x, y, grid_serial_number, _level, power_level
            )


def precompute_window_sums(grid):
    pre_grid = [list(l) for l in grid]
    # sum rows

    for x in range(1, grid_width):
        for y in range(0, grid_width):
            pre_grid[x][y] += pre_grid[x - 1][y]

    for y in range(1, grid_width):
        for x in range(0, grid_width):
            pre_grid[x][y] += pre_grid[x][y - 1]

    # sum columns
    return pre_grid


def get_window_sums(grid_serial_number):
    grid = [[point_power_level(x, y, grid_serial_number) for y in range(0, grid_width)] for x in range(0, grid_width)]
    return precompute_window_sums(grid)


def find_largest_power_window(window_sums, window_size):
    max_point = None
    max_power = None
    for x in range(0, grid_width - window_size):
        for y in range(0, grid_width - window_size):
            x2, y2 = x + window_size, y + window_size
            power = window_sums[x2][y2] - window_sums[x2][y] - window_sums[x][y2] + window_sums[x][y]
            if power is None or power > max_power:
                max_power = power
                max_point = (x, y)
    # 1 indexed instead of zero
    max_point = tuple(i + 1 for i in max_point)
    return max_point, max_power


def find_largest_window_any_size(window_sums):
    window, ((x, y), power) = max([(w, find_largest_power_window(window_sums, w)) for w in range(0, grid_width)],
                                  key=lambda x: x[1][1])
    return (x, y, window, power)


def run_tests():
    test_power_level_calculations()

    print "testing finding largest specific window"
    for grid_serial_number, window_size, largest_point, total_power in [
        (18, 3, (33, 45), 29),
        (42, 3, (21, 61), 30)
    ]:
        point, power = find_largest_power_window(get_window_sums(grid_serial_number), window_size)
        if point != largest_point:
            print "wrong point: {} != {}".format(point, largest_point)
        else:
            print "correct point: {}".format(point)
        if power != total_power:
            print "wrong power: {} != {}".format(power, total_power)
        else:
            print "correct power: {}".format(power)

    print "testing finding largest window any size"
    for grid_serial_number, window_size, largest_point, total_power in [
        (18, 16, (90, 269), 113),
        (42, 12, (232, 251), 119)
    ]:
        x, y, window, power = find_largest_window_any_size(get_window_sums(grid_serial_number))
        if (x, y) != largest_point:
            print "wrong point: {} != {}".format((x, y), largest_point)
        else:
            print "correct point: {}".format(point)
        if power != total_power:
            print "wrong power: {} != {}".format(power, total_power)
        else:
            print "correct power: {}".format(power)
        if window != window_size:
            print "wrong window size: {} != {}".format(window, window_size)
        else:
            print "correct window size: {}".format(window)


def main():
    grid_serial_number = 6303
    window_sums = get_window_sums(grid_serial_number)

    # part 1
    point, _ = find_largest_power_window(window_sums, 3)
    print ",".join(map(str, point))

    # part 2
    x, y, window, _ = find_largest_window_any_size(window_sums)
    print ",".join(map(str, (x, y, window)))


# run_tests()
main()
