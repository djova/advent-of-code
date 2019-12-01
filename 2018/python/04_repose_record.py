#!/usr/bin/env python

import re
from collections import namedtuple, defaultdict, Counter
from os.path import join, realpath, dirname
from datetime import datetime
from itertools import chain

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '04.txt')

Event = namedtuple('Event', ['datetime', 'guard', 'action'])


def load_events():
    def _parse(line):
        time, guard, action = re.match("\[(?P<time>.*)\] (?P<guard>Guard #\d+)?\s?([\w\s]+)\s*", line).groups()
        event = Event(datetime.strptime(time, "%Y-%m-%d %H:%M"),
                      int(guard[len("Guard #"):]) if guard else None,
                      action.strip())
        return event

    return [_parse(line) for line in open(input_file)]


def main():
    events = sorted(load_events(), key=lambda e: e.datetime)

    sleep_ranges = defaultdict(list)
    current_guard, sleep_start = None, None
    for e in events:
        if e.action == 'begins shift':
            current_guard = e.guard
        elif e.action == 'falls asleep':
            sleep_start = e.datetime
        elif e.action == 'wakes up':
            sleep_ranges[current_guard].append((sleep_start, e.datetime))
        else:
            raise Exception("bad action " + e.action)

    guard_minute_counts = {guard: Counter(chain(*[range(start.minute, end.minute) for start, end in sleeps])) for
                           guard, sleeps in sleep_ranges.items()}

    # part 1
    guard, minute_counts = max(guard_minute_counts.items(), key=lambda x: sum(x[1].values()))
    minute, _ = max(minute_counts.items(), key=lambda x: x[1])
    print guard * minute

    # part 2
    guard, minute_counts = max(guard_minute_counts.items(), key=lambda x: max(x[1].values()))
    minute, _ = max(minute_counts.items(), key=lambda x: x[1])
    print guard * minute


main()
