#!/usr/bin/python3

import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta

# [1518-04-22 00:00] Guard #2467 begins shift


def parse():
    with open("aoc04.txt", "r") as infile:
        for line in infile:
            line = line.strip()
            m = re.match(r".(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d).\s+(.*)$", line)
            datetime_args = list(map(int, m.groups()[:5]))
            timestamp = datetime(*datetime_args)
            event = m.group(6)
            param = None
            if event == "wakes up":
                event = "wake"
            elif event == "falls asleep":
                event = "sleep"
            else:
                m = re.match(r"Guard #(\d+) begins shift", event)
                event = "start"
                param = int(m.group(1))

            yield (timestamp, event, param)


guard_id = None
start_to_sleep = None
guards = defaultdict(Counter)
guards_sleeping = defaultdict(int)

for timestamp, event, param in sorted(parse(), key=lambda row: row[0]):
    print(timestamp, event, param)
    if event == "start":
        guard_id = param
        start_to_sleep = None
        continue

    if event == "sleep":
        start_to_sleep = timestamp
    elif event == "wake":
        sleeping = start_to_sleep
        while sleeping < timestamp:
            guards[guard_id].update([sleeping.minute])
            guards_sleeping[guard_id] += 1
            sleeping = sleeping + timedelta(seconds=60)
        start_to_sleep = None
        del sleeping

guards_most_common = [(guard_id, counter.most_common(1)[0]) for guard_id, counter in guards.items()]

print(guards_most_common)
guard_most_common = max(guards_most_common, key=lambda x: x[1][1])
print(guard_most_common)
print(guard_most_common[0] * guard_most_common[1][0])
